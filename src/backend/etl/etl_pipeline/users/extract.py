import logging
import time
import uuid
from collections import defaultdict
from multiprocessing import Pool, cpu_count

from .load import load_users_data
from .transform import transform_to_user_data
from src.backend.db.mongodb_handler import get_mongo_collection


def process_transactions_batch(transactions: list) -> dict:
    """
    Processes a batch of transactions and returns transformed user data.

    This function processes a list of transactions, aggregates user data, and
    returns a dictionary mapping user addresses to their corresponding transformed
    data. The data transformation includes transaction counts, amounts sent/received,
    and protocol usage.

    :param transactions: List of transaction records, where each record contains
                         transaction details such as 'from', 'to', 'value (ETH)', etc.
    :type transactions: list[dict]

    :return: A dictionary mapping user addresses to their corresponding user data.
    :rtype: dict

    :raises ValueError: If the transactions list is empty or contains invalid data.
    """
    batch_id = str(uuid.uuid4())
    start_time = time.time()
    user_data = {}

    transformed_data = transform_to_user_data(
        transactions
    )  # Transform the input transactions into user-specific data

    for (
        address,
        data,
    ) in (
        transformed_data.items()
    ):  # Update user data with the transformed data, aggregating by address
        if address not in user_data:
            user_data[address] = data
        else:
            user_data[address].update(data)

    processing_time = time.time() - start_time
    logging.info(
        f"Batch {batch_id}: Processed {len(transactions)} transactions in {processing_time:.2f} seconds."
    )
    return user_data


def extract_users() -> None:
    """
    Extracts user data from the transactions collection in MongoDB.

    This function fetches transaction data from a MongoDB collection, processes
    it in parallel batches, and aggregates user data. The user data is then
    loaded into the system for further analysis or storage.

    :raises Exception: If there is an error connecting to MongoDB or processing the transactions.
    """
    logging.info("Starting to extract user data from transactions collection.")
    transactions_collection = get_mongo_collection(
        db_name="defi_db", collection_name="transactions"
    )
    batch_size = 100000
    logging.info(f"Using batch_size: {batch_size}.")

    with transactions_collection.database.client.start_session() as session:
        logging.info("MongoDB session started.")
        with transactions_collection.find(
            {},  # All transactions
            {
                "from": 1,
                "transaction_hash": 1,
                "to": 1,
                "value (ETH)": 1,
                "gas_used": 1,
                "timestamp": 1,
                "metadata.protocol_name": 1,
                "metadata.type": 1,
                "metadata.blockchain": 1,
                "metadata.contract_id": 1,
            },
            no_cursor_timeout=True,
            session=session,
        ) as cursor:
            logging.info("Cursor initialized. Starting to fetch transactions.")
            transactions = list(cursor)

            num_processes = (
                cpu_count()
            )  # Determine the number of processes and the size of each batch
            batch_size = max(1, len(transactions) // num_processes)
            batches = [
                transactions[i : i + batch_size]
                for i in range(0, len(transactions), batch_size)
            ]

            logging.info(
                f"Total batches to process: {len(batches)}, each with {batch_size} transactions."
            )

            with Pool(
                processes=num_processes
            ) as pool:  # Use multiprocessing to process the batches in parallel
                results = pool.map(process_transactions_batch, batches)

            total_users_data = {}

            for result in results:  # Aggregate the user data from all batches
                for address, data in result.items():
                    if address not in total_users_data:
                        total_users_data[address] = data
                    else:
                        total_users_data[address].update(data)

            final_user_data = defaultdict(lambda: None, total_users_data)

        logging.info(
            f"User data extraction completed for {len(final_user_data)} users."
        )
        load_users_data(dict(final_user_data))
        logging.info("User data loading completed.")
