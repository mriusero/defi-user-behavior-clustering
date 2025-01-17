from datetime import datetime
import logging
from pymongo import UpdateOne

from ..mongodb_handler import get_mongo_collection

def upsert_transactions(protocol_name, contract_type, contract_id, blockchain, transactions):
    """
    Adds transactions to a time-series collection.
    Does not reinsert transactions that are already present.
    Uses a bulk approach for optimized performance.

    :param protocol_name: The name of the protocol for the contract. (str)
    :param contract_type: The type of the contract. (str)
    :param contract_id: The unique identifier for the contract. (str)
    :param blockchain: The blockchain platform (e.g., "ethereum"). (str)
    :param transactions: A list of transaction data to be inserted. (list)

    :return: None

    :raise Exception: If there is an error during the upsert operation in MongoDB.
    """
    transactions_collection = get_mongo_collection(db_name="defi_db", collection_name="transactions")
    transactions_collection.create_index([("transaction_hash", 1)])
    transactions_collection.create_index([("timestamp", 1)])

    bulk_operations = []

    for tx in transactions:
        # Retrieve additional fields
        value = float(tx["value"]) if "value" in tx else None
        gas = float(tx.get("gas", 0)) if "gas" in tx else None
        gas_price = float(tx.get("gasPrice", 0)) if "gasPrice" in tx else None
        ether_price = float(tx.get("etherPrice", 0)) if "etherPrice" in tx else None

        # Create the transaction document with additional info
        transaction_doc = {
            "timestamp": datetime.utcfromtimestamp(int(tx["timeStamp"])),
            "metadata": {
                "protocol_name": protocol_name,
                "type": contract_type,
                "blockchain": blockchain,
                "contract_id": contract_id
            },
            "from": tx["from"],
            "transaction_hash": tx["hash"],
            "to": tx["to"],
            "value (ETH)": value,
            "transaction_fee (ETH)": gas,
            "gas_price (Gwei)": gas_price,
            "ether_price ($)": ether_price,
        }
        # Add the upsert operation for the current transaction
        bulk_operations.append(
            UpdateOne(
                {"transaction_hash": tx["hash"]},
                {"$setOnInsert": transaction_doc},
                upsert=True
            )
        )
    # Perform the bulk operation if there are any
    if bulk_operations:
        try:
            result = transactions_collection.bulk_write(bulk_operations, ordered=False)
            logging.info(f"{result.upserted_count} new transactions added to MongoDB.")
        except Exception as e:
            logging.error(f"Error inserting transactions into MongoDB: {e}")