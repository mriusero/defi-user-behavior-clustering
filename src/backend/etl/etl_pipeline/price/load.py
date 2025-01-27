import logging
from pymongo import UpdateOne

from ..mongodb_handler import get_mongo_collection


def load_data_to_mongodb(data: list):
    """
    Loads the new data into a MongoDB collection, inserting only new transactions.

    :param data: The data to be inserted into the MongoDB collection, formatted as a list of dictionaries. (list)
    :raise Exception: If the data insertion fails, an error is logged.
    """
    prices_collection = get_mongo_collection(
        db_name="defi_db", collection_name="market"
    )

    prices_collection.create_index(
        [("timestamp", 1), ("symbol", 1), ("contract_address", 1)], unique=True
    )
    operations = []
    for record in data:
        query = {
            "timestamp": record["timestamp"],
            "symbol": record["symbol"],
            "contract_address": record["contract_address"],
        }
        operation = UpdateOne(query, {"$setOnInsert": record}, upsert=True)
        operations.append(operation)

    if operations:
        result = prices_collection.bulk_write(operations)
        logging.info(
            f"Inserted {result.upserted_count} new records into defi_db.market collection."
        )
    else:
        logging.info("No new records to insert.")
