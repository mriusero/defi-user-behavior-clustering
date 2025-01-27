import logging
from datetime import datetime

from pymongo import UpdateOne

from ..mongodb_handler import get_mongo_collection


def upsert_transactions(
    protocol_name, contract_type, contract_id, blockchain, transactions
):
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
    transactions_collection = get_mongo_collection(
        db_name="defi_db", collection_name="transactions"
    )
    transactions_collection.create_index(
        [("transaction_hash", 1)]
    )  # Index by transaction hash
    transactions_collection.create_index([("timestamp", 1)])  # Index by timestamp

    bulk_operations = []

    for tx in transactions:
        value = (
            float(tx["value"]) / 10**18 if "value" in tx else None
        )  # Convert from wei to ETH (1 ETH = 10^18 wei)
        gas = (
            float(tx.get("gas", 0)) if "gas" in tx else None
        )  # Gas used in the transaction
        gas_used = (
            float(tx.get("gasUsed", 0)) if "gasUsed" in tx else None
        )  # Gas actually used (0 if not available)
        is_error = tx.get(
            "isError", "0"
        )  # If the transaction failed, 'isError' is "1", otherwise "0"
        error_code = tx.get("errCode", "")  # Error code if the transaction failed
        trace_id = tx.get("traceId", "")  # Trace ID to identify the transaction trace

        transaction_doc = {
            "timestamp": datetime.utcfromtimestamp(
                int(tx["timeStamp"])
            ),  # Convert Unix timestamp to datetime object
            "metadata": {
                "protocol_name": protocol_name,
                "type": contract_type,
                "blockchain": blockchain,
                "contract_id": contract_id,
            },
            "from": tx["from"],  # The sender's address
            "tx_hash": tx["hash"],  # The unique hash of the transaction
            "to": tx["to"],  # The receiver's address
            "value (ETH)": value,  # Value of the transaction in ETH (converted from Wei)
            "gas": gas,  # Gas used in the transaction
            "gas_used": gas_used,  # The actual gas used in the transaction
            "is_error": is_error,  # Indicates if the transaction was an error (1) or not (0)
            "error_code": error_code,  # Error code if the transaction failed
            "trace_id": trace_id,  # Trace ID to identify transaction tracing
        }
        """
            * 'gas' represents the estimated amount of gas (in gas units) required for the transaction to execute.
            Gas is a measure of computational work on the Ethereum blockchain. Each operation (like an addition, state change, etc.)
            in a transaction or smart contract consumes a certain amount of gas. The gas limit is the maximum amount of gas that
            can be used for the transaction. Gas is priced in Gwei, but the 'gas' field itself is just a measure of the number of gas units.
            Example: If 'gas' is 2300, it means 2300 gas units were estimated for the transaction.
            
            * 'gas_used' represents the actual amount of gas (in gas units) used to execute the transaction.
            This value shows the real consumption of gas for completing the transaction. If 'gas_used' is less than the 'gas',
            it indicates that the transaction did not require as much gas as initially estimated.
            Example: If 'gas_used' is 2100, it means only 2100 gas units were actually consumed during the transaction execution.
        """
        bulk_operations.append(
            UpdateOne(
                {
                    "transaction_hash": tx["hash"]
                },  # Use the transaction hash to identify the document
                {
                    "$setOnInsert": transaction_doc
                },  # Insert if the transaction doesn't already exist
                upsert=True,  # Ensure this operation is upserted (insert if new, update if existing)
            )
        )
    if bulk_operations:
        try:
            result = transactions_collection.bulk_write(bulk_operations, ordered=False)
            logging.info(f"{result.upserted_count} new transactions added to MongoDB.")
        except Exception as e:
            logging.error(f"Error inserting transactions into MongoDB: {e}")
