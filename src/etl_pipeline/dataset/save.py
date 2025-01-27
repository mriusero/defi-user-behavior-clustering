import os

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
        'contracts',
        'transactions',
        'users',
        'market_enriched',
    ]

    for collection_name in collections:
        output_file = f"data/defi_db/{collection_name}.parquet"
        try:
            logger.info(f"Exporting data from MongoDB collection `{collection_name}` to Parquet file: {output_file}")
            mongo_collection = get_mongo_collection(db_name='defi_db', collection_name=collection_name)
            data = list(mongo_collection.find())

            if not data:
                print("No data found in collection.")
                return

            df = pd.DataFrame(data)
            df = df.drop(columns=[col for col in ['_id'] if col in df.columns])

            if collection_name == 'contracts':
                df = df.drop(columns=[col for col in ['contract_id', 'protocol_id'] if col in df.columns])
                df = df[['contract_address', 'blockchain', 'type', 'protocol_name', 'protocol_symbol', 'description', 'website_url']]

            elif collection_name == 'transactions':
                df = df.drop(columns=[col for col in ['trace_id', 'tx_hash'] if col in df.columns])
                df = df[[
                    'timestamp', 'transaction_hash', 'from', 'to', 'value (ETH)', 'gas', 'gas_used', 'is_error',
                    'error_code', 'metadata'
                ]]

            elif collection_name == 'users':
                df = df.drop(columns=[col for col in ['user_id'] if col in df.columns])
                df = df[[
                    'address', 'first_seen', 'last_seen', 'protocol_types', 'protocols_used', 'received_count',
                    'total_received (ETH)', 'sent_count', 'total_sent (ETH)', 'transactions'
                ]]

            elif collection_name == 'market_enriched':
                df = df[[
                    'timestamp', 'blockchain', 'protocol_name', 'symbol', 'type', 'contract_address',
                    'open (usd)', 'high (usd)', 'low (usd)', 'close (usd)', 'volume', 'nb_tx_1h', 'nb_tx_24h',
                    'total_value_eth_1h', 'total_value_eth_24h', 'total_gas_used_1h', 'total_gas_used_24h',
                    'nb_unique_receivers_1h', 'nb_unique_receivers_24h', 'nb_unique_senders_1h',
                    'nb_unique_senders_24h',
                    'std_value_eth_1h', 'std_value_eth_24h', 'std_gas_used_1h', 'std_gas_used_24h',
                    'avg_gas_used_1h', 'avg_gas_used_24h', 'avg_value_eth_per_tx_1h', 'avg_value_eth_per_tx_24h',
                    'max_gas_used_1h', 'max_gas_used_24h', 'max_value_eth_1h', 'max_value_eth_24h',
                    'median_value_eth_1h', 'median_value_eth_24h', 'min_gas_used_1h', 'min_gas_used_24h',
                    'min_value_eth_1h', 'min_value_eth_24h', 'num_errors_1h', 'num_errors_24h', 'error_rate_1h',
                    'error_rate_24h'
                ]]

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

                logger.info(f"- column `{column}` is type {df[column].dtype}")

            table = pa.Table.from_pandas(df)
            pq.write_table(table, output_file)

            logger.info(f"Data has been saved to the Parquet file: {output_file}")

        except Exception as e:
            logger.error(f"Error during data export: {e}")

    client = get_mongo_client()
    client.close()