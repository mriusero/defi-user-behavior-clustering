import logging
import multiprocessing
from multiprocessing import Manager
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from itertools import islice

from .wrapped_task import precompute_protocol_ranges, load_market_data, wrapped_tasks
from ..mongodb_handler import get_mongo_database

logger = logging.getLogger(__name__)


def batch_users(iterable, size):
    it = iter(iterable)
    while True:
        batch = list(islice(it, size))
        if not batch:
            break
        yield batch


def generate_dataset():
    """
    Main function to generate and enrich a dataset using MongoDB.

    This function retrieves user data from the MongoDB database, precomputes
    protocol ranges, loads market data into a cache, and processes user data
    in parallel using threading for better I/O performance.

    :raise Exception: If an error occurs during processing, it logs the error and continues with other tasks.
    """
    db = get_mongo_database(db_name="defi_db")
    users_cursor = db["users"].find({})
    users = list(users_cursor)

    if not users:
        logger.warning("No users found in the database.")
        return

    logger.info("Precomputing protocol ranges...")
    protocol_ranges = precompute_protocol_ranges(db)

    logger.info("Loading market data into cache...")
    market_data_cache = load_market_data(db)

    manager = Manager()
    counter = manager.Value("i", 0)
    lock = manager.Lock()

    batch_size = 100000

    with ThreadPoolExecutor(
        max_workers=min(8, multiprocessing.cpu_count())
    ) as executor:
        for users_batch in tqdm(
            batch_users(users, batch_size),
            total=len(users) // batch_size,
            desc="Processing batches",
        ):
            future = executor.submit(
                wrapped_tasks,
                (users_batch, counter, lock, protocol_ranges, market_data_cache),
            )
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error in thread: {e}", exc_info=True)

        logger.info(
            f"User enrichment completed. Total users processed: {counter.value}"
        )
