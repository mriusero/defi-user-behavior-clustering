import logging
import time
from multiprocessing import Pool, cpu_count

from pymongo import UpdateOne
from tqdm import tqdm

from src.backend.db.mongodb_handler import get_mongo_collection

# Configure logging
logging.basicConfig(level=logging.INFO)


def load_batch(batch_data: list, db_name: str, collection_name: str) -> None:
    """
    Processes a batch of user data and inserts it into MongoDB.

    :param batch_data: A list of tuples, where each tuple contains a user address
                       and their corresponding user data.
    :param db_name: The name of the MongoDB database.
    :param collection_name: The name of the MongoDB collection.
    """
    users_collection = get_mongo_collection(
        db_name=db_name, collection_name=collection_name
    )
    users_collection.create_index([("address", 1)])
    bulk_operations = [
        UpdateOne({"address": address}, {"$set": data}, upsert=True)
        for address, data in batch_data
    ]
    if bulk_operations:
        try:
            start_time = time.time()
            users_collection.bulk_write(bulk_operations, ordered=False)
            elapsed_time = time.time() - start_time
            # logging.info(f"Batch of {len(bulk_operations)} records processed in {elapsed_time:.2f} seconds.")
        except Exception as e:
            logging.error(f"Failed to insert batch: {e}")


def chunk_data(data: list, chunk_size: int) -> list:
    """
    Splits data into chunks of a specified size.
    """
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


def process_chunk(chunk_data_tuple):
    """
    This function processes each chunk in parallel by extracting db_name, collection_name, and chunk.
    :param chunk_data_tuple: A tuple containing (chunk, db_name, collection_name)
    """
    chunk, db_name, collection_name = chunk_data_tuple
    load_batch(chunk, db_name, collection_name)


def load_users_data(users_data: dict) -> None:
    """
    Loads user data into MongoDB with reduced multiprocessing.

    :param users_data: A dictionary where keys are user addresses and values are
                        the corresponding user data.
    """
    BATCH_SIZE = 10000
    user_data_list = list(users_data.items())
    data_chunks = list(chunk_data(user_data_list, BATCH_SIZE))

    logging.info(
        f"Preparing to load {len(users_data)} users in {len(data_chunks)} batches."
    )

    db_name = "defi_db"
    collection_name = "users"

    # Prepare the chunks as tuples (chunk, db_name, collection_name)
    chunk_data_tuples = [(chunk, db_name, collection_name) for chunk in data_chunks]

    # Multiprocessing - Process chunks in parallel
    with Pool(processes=cpu_count()) as pool:
        logging.info(f"Starting to process {len(data_chunks)} chunks in parallel...")
        for _ in tqdm(
            pool.imap(process_chunk, chunk_data_tuples),
            total=len(data_chunks),
            desc="Processing batches",
        ):
            pass

    logging.info("All user data has been processed and inserted into MongoDB.")
