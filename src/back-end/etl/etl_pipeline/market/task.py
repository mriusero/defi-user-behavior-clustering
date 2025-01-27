import logging
from datetime import datetime
import multiprocessing
from tqdm import tqdm

from .extract_market import get_market_data
from .aggregate import aggregate_transactions
from .load import load_df_to_mongo
from ..mongodb_handler import get_mongo_database

logger = logging.getLogger(__name__)

def wrapped_enrich(args):
    """
    Wrapper function to enrich a protocol and update the shared counter.

    :param args: A tuple containing the following elements:
        - protocol (str): The protocol name to enrich.
        - start_date (datetime): The start date for the enrichment.
        - end_date (datetime): The end date for the enrichment.
        - counter (multiprocessing.Value): A shared counter to track the progress.
        - lock (multiprocessing.Lock): A lock to ensure thread safety when updating the counter.
    :return: None
    :raise: Exception: If an error occurs during the enrichment process.
    """
    protocol, start_date, end_date, counter, lock = args
    try:
        df = get_market_data(protocol)
        df = aggregate_transactions(df, time_delta=1)
        df = aggregate_transactions(df, time_delta=24)
        load_df_to_mongo(df)
        logger.info(f"Enriched data for protocol {protocol}.\n {df.describe()}")
    except Exception as e:
        logger.error(f"Error enriching protocol {protocol}: {e}")


def aggregation_task(start_date, end_date):
    """
    Main function to enrich the old_market collection with aggregated metrics for all protocols
    within a given date range.

    :param start_date: The start date (string in 'YYYY-MM-DD' format) for the enrichment.
    :param end_date: The end date (string in 'YYYY-MM-DD' format) for the enrichment.
    :return: None
    :raise: Exception: If an error occurs during the database retrieval or task execution.
    """
    db = get_mongo_database(db_name='defi_db')
    protocols = db.transactions.distinct("metadata.protocol_name")
    logger.info(f"Found {len(protocols)} protocols to process: {protocols}")

    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    logger.info(f"Enriching old_market collection for the period `{start_date}` to `{end_date}`.")

    manager = multiprocessing.Manager()
    counter = manager.Value('i', 0)
    lock = manager.Lock()

    tasks = [(protocol, start_date, end_date, counter, lock) for protocol in protocols]
    #tasks = [(protocol, start_date, end_date, counter, lock) for protocol in protocols if protocol == "NFTFI"]

    logger.info("Launching multiprocessing pool...")

    with tqdm(total=len(protocols), desc="Processing protocols", unit="protocol") as pbar:
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            results = []

            for task in tasks:
                result = pool.apply_async(wrapped_enrich, (task,))
                results.append(result)

            for result in results:
                result.get()
                pbar.update(1)

            pool.close()
            pool.join()

    manager.shutdown()
    logger.info("Market enrichment completed for all protocols.")