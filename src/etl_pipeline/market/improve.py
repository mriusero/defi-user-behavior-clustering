import logging
from datetime import datetime
import multiprocessing

from .enrich import enrich_market_collection
from ..mongodb_handler import get_mongo_database


def improve_market(start_date, end_date):
    """
    Main function to enrich the market collection with aggregated metrics for all protocols
    within a given date range.

    :param start_date: The start date (string in 'YYYY-MM-DD' format) for the enrichment.
    :param end_date: The end date (string in 'YYYY-MM-DD' format) for the enrichment.
    """
    db = get_mongo_database(db_name='defi_db')
    protocols = db.transactions.distinct("metadata.protocol_name")
    logging.info(f"Found {len(protocols)} protocols to process : {protocols}")

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.starmap(enrich_market_collection, [(protocol, start_date, end_date) for protocol in protocols])

    logging.info("All protocols processed.")