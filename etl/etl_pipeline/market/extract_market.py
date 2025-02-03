import pandas as pd
import logging

from ..mongodb_handler import get_mongo_collection

logger = logging.getLogger(__name__)


def get_market_data(protocol_name):
    """
    Connects to a MongoDB collection, retrieves the data, and loads it into a Pandas DataFrame.
    Args:
        :param protocol_name: Name of the protocol to filter the data.
    Returns:
        pd.DataFrame: DataFrame containing the data from the MongoDB collection.
    """
    try:
        market_collection = get_mongo_collection(
            db_name="defi_db", collection_name="market"
        )
        query = {"protocol_name": protocol_name}
        data = list(market_collection.find(query))
        df = pd.DataFrame(data)
        return df

    except Exception as e:
        logger.error(f"An error occurred: {e}")
