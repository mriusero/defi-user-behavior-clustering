from pymongo import UpdateOne
import logging
from tqdm import tqdm
from sortedcontainers import SortedDict
import time
import json

from src.backend.db.mongodb_handler import get_mongo_database

logger = logging.getLogger(__name__)


def precompute_protocol_ranges(db):
    """
    Precomputes the minimum and maximum timestamp ranges for all protocols.

    :param db: MongoDB database instance.
    :return: A dictionary with protocol names as keys and (min_date, max_date) as values.
    """
    ranges = {}
    protocol_data = db["market_enriched"].aggregate(
        [
            {
                "$group": {
                    "_id": "$protocol_name",
                    "min_date": {"$min": "$timestamp"},
                    "max_date": {"$max": "$timestamp"},
                }
            }
        ]
    )
    for protocol in protocol_data:
        ranges[protocol["_id"]] = (protocol["min_date"], protocol["max_date"])
    return ranges


def load_market_data(db):
    """
    Loads all market data into a cache for efficient lookup.

    :param db: MongoDB database instance.
    :return: A dictionary with protocol names as keys and their respective market data.
    """
    market_data = {}
    cursor = db["market_enriched"].find({})
    for document in cursor:
        protocol_name = document["protocol_name"]
        timestamp = document["timestamp"]
        market_data.setdefault(protocol_name, SortedDict())[timestamp] = document
    return market_data


def find_closest_timestamp(sorted_dict, target_timestamp):
    pos = sorted_dict.bisect_left(target_timestamp)
    keys = list(sorted_dict.keys())

    # Trouver le plus proche entre les deux voisins
    if pos == 0:
        return keys[0]
    if pos == len(keys):
        return keys[-1]
    before = keys[pos - 1]
    after = keys[pos]
    return (
        before
        if abs(before - target_timestamp) <= abs(after - target_timestamp)
        else after
    )


def wrapped_tasks(args):
    """
    Processes a batch of users, enriching their data with additional information from the database
    and saves it into the 'dataset' collection.

    :param args: A tuple containing:
                 - users_batch: A batch of user documents to process.
                 - counter: A multiprocessing.Value object for tracking progress.
                 - lock: A multiprocessing.Lock object for thread-safe updates.
                 - protocol_ranges: Precomputed protocol timestamp ranges.
                 - market_data_cache: Cached market data for efficient lookups.
    """
    users_batch, counter, lock, protocol_ranges, market_data_cache = args
    db = get_mongo_database(db_name="defi_db")

    dataset_updates = []

    for user in tqdm(users_batch, desc="Processing users", leave=False):

        transactions_with_market_data = []

        for transaction in user.get("transactions", []):
            transaction_timestamp = transaction["timestamp"]
            protocol_name = transaction["protocol_name"]

            if protocol_name in protocol_ranges:
                min_date, max_date = protocol_ranges[protocol_name]

                if not (min_date <= transaction_timestamp <= max_date):
                    continue

                protocol_market_data = market_data_cache.get(
                    protocol_name, SortedDict()
                )
                closest_timestamp = find_closest_timestamp(
                    protocol_market_data, transaction_timestamp
                )
                market_data = protocol_market_data[closest_timestamp]
            else:
                market_data = {"market_data": "Protocol not found"}

            transaction_with_market_data = {
                "transaction_hash": transaction["transaction_hash"],
                "timestamp": transaction_timestamp,
                "value_eth": transaction["value (ETH)"],
                "protocol_name": protocol_name,
                "protocol_type": transaction["protocol_type"],
                "gas_used": transaction["gas_used"],
                "market_data": market_data,
            }

            transactions_with_market_data.append(transaction_with_market_data)

        dataset_document = {
            "user_id": user["_id"],
            "user_address": user["address"],
            "first_seen": user["first_seen"],
            "last_seen": user["last_seen"],
            "protocol_types": user["protocol_types"],
            "protocols_used": user["protocols_used"],
            "received_count": user["received_count"],
            "sent_count": user["sent_count"],
            "total_received (ETH)": user["total_received (ETH)"],
            "total_sent (ETH)": user["total_sent (ETH)"],
            "transactions": transactions_with_market_data,
        }

        dataset_updates.append(
            UpdateOne({"user_id": user["_id"]}, {"$set": dataset_document}, upsert=True)
        )

        with lock:
            counter.value += 1

    if dataset_updates:
        BATCH_SIZE = 5000
        for i in tqdm(
            range(0, len(dataset_updates), BATCH_SIZE), desc="Updating dataset"
        ):
            try:
                # Essayer d'effectuer un bulk_write sur tout le batch
                db["dataset"].bulk_write(
                    dataset_updates[i : i + BATCH_SIZE], ordered=False
                )
            except Exception as e:
                if "BSONObjectTooLarge" in str(e):
                    # L'erreur est liée à un document trop volumineux
                    # Nous devons identifier le document fautif
                    for update in dataset_updates[i : i + BATCH_SIZE]:
                        try:
                            # Essayer d'ajouter chaque document individuellement
                            db["dataset"].bulk_write([update], ordered=False)
                        except Exception as inner_e:
                            if "BSONObjectTooLarge" in str(inner_e):
                                # Créer un identifiant unique pour le fichier
                                unique_id = int(time.time() * 1000)
                                filename = f"data/ObjectTooLarge/BSONObjectTooLarge_{unique_id}.json"

                                # Extraire les données du document à partir de l'opération UpdateOne ou InsertOne
                                document_to_save = None
                                if hasattr(update, "update") and update.update:
                                    document_to_save = (
                                        update.update
                                    )  # C'est une mise à jour
                                elif hasattr(update, "document") and update.document:
                                    document_to_save = (
                                        update.document
                                    )  # C'est une insertion

                                if document_to_save:
                                    # Enregistrer le document fautif dans un fichier JSON
                                    with open(filename, "a") as f:
                                        json.dump(document_to_save, f, indent=4)
                                        f.write("\n")

                                    print(
                                        f"Document trop volumineux, enregistré dans '{filename}'."
                                    )
                            else:
                                # Si l'erreur n'est pas liée à la taille, la relancer
                                raise inner_e
                else:
                    # Si l'erreur n'est pas liée à la taille, relancer l'exception
                    raise e

        logger.info(f"Processed {counter.value} total users.")
