import pandas as pd
from pymongo import UpdateOne, ASCENDING
import logging

from src.backend.db.mongodb_handler import get_mongo_collection

logger = logging.getLogger(__name__)


def load_df_to_mongo(df: pd.DataFrame):
    """
    Load a DataFrame to a MongoDB collection using bulk write operations.

    :param df: A Pandas DataFrame containing the data to be loaded into MongoDB.
    :return: The result of the bulk write operation.
    :raise: Exception: If an error occurs during the bulk write process.
    """
    collection = get_mongo_collection(
        db_name="defi_db", collection_name="market_enriched"
    )
    collection.create_index(
        [("timestamp", ASCENDING), ("protocol_name", ASCENDING)], unique=True
    )
    bulk_operations = []
    for index, row in df.iterrows():
        document = row.to_dict()
        if "_id" not in document:
            document["_id"] = str(row.name)
        bulk_operations.append(
            UpdateOne({"_id": document["_id"]}, {"$set": document}, upsert=True)
        )
    if bulk_operations:
        try:
            result = collection.bulk_write(bulk_operations)
            return result
        except Exception as e:
            logger.error(f"Error during bulk write operation: {e}")
            raise e
