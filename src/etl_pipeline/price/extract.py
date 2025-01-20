import logging
import yfinance as yf
from rich.console import Console
from rich.table import Table

from ..mongodb_handler import get_mongo_collection
from .transform import transform_ohlc_data
from .load import load_data_to_mongodb


def display_arrays(df, symbol):
    console = Console()
    table = Table(title=f"----- OHLC Data for `{symbol}` -----")

    for column in df.columns:
        table.add_column(column, justify="right")

    for _, row in df.iterrows():
        table.add_row(*map(str, row))

    console.print(table)


def fetch_ohlc_data(symbol: str) -> yf.Ticker.history:
    """
    Fetches OHLC data for a specific contract from an API.

    :param symbol: The contract symbol (e.g., 'ETH'). (str)
    :return: OHLC data for the specified symbol in the form of a pandas DataFrame. (pd.DataFrame)
    :raise Exception: If fetching OHLC data fails, an error is logged and an exception is raised.
    """
    try:
        logging.info(f"Fetching OHLC data for symbol: {symbol}")
        key = yf.Ticker(f"{symbol}-USD")
        key_data = key.history(period='730d', interval='1h')
        logging.info(f"Fetched {len(key_data)} rows of data for {symbol}")
        return key_data
    except Exception as e:
        logging.error(f"Failed to fetch OHLC data for {symbol}: {e}")
        raise


def get_contracts() -> list:
    """
    Fetches contract numbers from the MongoDB collection.
    :return: List of contracts metadata from the MongoDB collection. (list)
    :raise Exception: If fetching contracts from MongoDB fails, an error is logged and an exception is raised.
    """
    try:
        logging.info("Fetching Ethereum contracts from MongoDB...")
        contracts_collection = get_mongo_collection(db_name='defi_db', collection_name='contracts')
        contracts_metadata = contracts_collection.find(
            {"blockchain": "ethereum"},
            {
                "blockchain": 1,
                "protocol_name": 1,
                "contract_address": 1,
                "protocol_symbol": 1,
                "type": 1,
                "_id": 0
            }
        )
        return contracts_metadata
    except Exception as e:
        logging.error(f"Failed to fetch contracts from MongoDB: {e}")
        raise


def fetch_prices():
    """
    Main function to fetch, transform, and load OHLC data for each Ethereum contract.
    :raise Exception: If the ETL process fails, an error is logged and an exception is raised.
    """
    logging.info("Starting the ETL process for fetching Ethereum contract prices...")

    try:
        contracts_metadata = get_contracts()

        if not contracts_metadata:
            logging.warning("No Ethereum contracts found.")
            return

        for contract in contracts_metadata:
            symbol = contract['protocol_symbol']
            logging.info(f"Processing symbol: {symbol}")

            raw_data = fetch_ohlc_data(symbol)
            display_arrays(raw_data.head(5), symbol)

            transformed_data = transform_ohlc_data(contract, symbol, raw_data)
            logging.info(f"Transformed data for {symbol}")

            load_data_to_mongodb(transformed_data)
            logging.info(f"Loaded transformed data to MongoDB for {symbol}")


    except Exception as e:
        logging.error(f"ETL process failed: {e}")
        raise