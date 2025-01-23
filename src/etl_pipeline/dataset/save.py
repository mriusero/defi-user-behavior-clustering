import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import logging
import json

from ..mongodb_handler import get_mongo_collection, get_mongo_client

logger = logging.getLogger(__name__)


def save_mongodb_to_parquet():
    """
    Saves data from a MongoDB collection into a Parquet file.

    :raise Exception: If any error occurs during data export.
    """
    collections = [
        'protocols',
        'contracts',
        'transactions',
        'users',
        'market_enriched',
    ]

    for collection in collections:
        output_file = f"data/defi_db/{collection}.parquet"
        try:
            logger.info(f"Exporting data from MongoDB collection `{collection}` to Parquet file: {output_file}")
            collection = get_mongo_collection(db_name='defi_db', collection_name=collection)
            data = list(collection.find())

            if not data:
                print("No data found in collection.")
                return

            df = pd.DataFrame(data)
            df = df.drop(columns=[col for col in ['_id', 'user_id'] if col in df.columns])

            for column in df.columns:
                if df[column].dtype == 'object':
                    try:
                        df[column] = df[column].apply(
                            lambda x: json.dumps(
                                x,
                                default=str
                            ) if isinstance(x, (dict, list)) else str(x)
                        )
                    except Exception as e:
                        logger.error(f"Erreur de conversion pour la colonne `{column}` : {e}")
                        raise

                elif pd.api.types.is_datetime64_any_dtype(df[column]):
                    logger.info(f"Converting datetime column `{column}` to ISO 8601 string format.")
                    df[column] = df[column].apply(lambda x: x.isoformat() if pd.notnull(x) else None)

                logger.info(f"- column `{column}` is type {df[column].dtype}")

            table = pa.Table.from_pandas(df)
            pq.write_table(table, output_file)

            logger.info(f"Data has been saved to the Parquet file: {output_file}")

        except Exception as e:
            logger.error(f"Error during data export: {e}")

    client = get_mongo_client()
    client.close()