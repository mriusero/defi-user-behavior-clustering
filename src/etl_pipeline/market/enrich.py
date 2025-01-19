import logging
import pymongo
from tqdm import tqdm

from ..mongodb_handler import get_mongo_database
from .aggregate import aggregate_transactions, aggregate_24h_data

def enrich_market_collection(protocol_name, start_date, end_date):
    """
    Enriches the market collection with aggregated transaction metrics for a given protocol
    between the specified start and end dates.

    :param protocol_name: The name of the protocol to be processed.
    :param start_date: The start date (datetime object) for filtering transactions.
    :param end_date: The end date (datetime object) for filtering transactions.
    """
    db = get_mongo_database(db_name='defi_db')
    logging.info(f"Starting enrichment for protocol: {protocol_name} from {start_date} to {end_date}")

    hourly_data_list = aggregate_transactions(db, protocol_name, start_date, end_date)
    enhanced_data_list = aggregate_24h_data(db, protocol_name, hourly_data_list)

    logging.info(f"Processing {len(enhanced_data_list)} hourly entries for protocol: {protocol_name}")

    bulk_operations = []
    for hourly_data in tqdm(enhanced_data_list, desc=f"Updating market collection for {protocol_name}", unit="entry", total=len(enhanced_data_list)):
        timestamp = hourly_data["original_timestamp"]

        if timestamp is None or protocol_name is None:
            logging.error(f"Missing timestamp or protocol name, hourly_data:{hourly_data}")
            break

        iso_timestamp = timestamp.replace(minute=0, second=0, microsecond=0)

        bulk_operations.append(
            pymongo.UpdateOne(
                {
                    "timestamp": iso_timestamp,
                    "protocol_name": protocol_name,
                },
                {
                    "$set": {
                        "total_transactions": hourly_data.get("total_transactions", 0),
                        "unique_users": hourly_data.get("unique_users", 0),
                        "unique_senders": hourly_data.get("unique_senders", 0),
                        "unique_receivers": hourly_data.get("unique_receivers", 0),
                        "total_volume_eth": hourly_data.get("total_volume_eth", 0),
                        "total_gas_used": hourly_data.get("total_gas_used", 0),
                        "total_transactions_24h": hourly_data.get("total_transactions_24h", 0),
                        "unique_users_24h": hourly_data.get("unique_users_24h", 0),
                        "unique_senders_24h": hourly_data.get("unique_senders_24h", 0),
                        "unique_receivers_24h": hourly_data.get("unique_receivers_24h", 0),
                        "total_volume_eth_24h": hourly_data.get("total_volume_eth_24h", 0),
                        "total_gas_used_24h": hourly_data.get("total_gas_used_24h", 0)
                    }
                },
                upsert=False,
            )
        )
    if bulk_operations:
        result = db.market.bulk_write(bulk_operations)
        logging.info(f"Bulk write result: {result.bulk_api_result}")
    else:
        logging.warning("No bulk operations to execute.")

    logging.info(f"Enrichment completed for protocol: {protocol_name}")