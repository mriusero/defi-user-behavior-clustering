import time
import logging.config

from .config import LOGGING_CONFIG, KEY_PROTOCOLS
from .protocols import get_defi_protocol_info
from .utils import save_to_json

logging.config.dictConfig(LOGGING_CONFIG)
logging.info("Logging configured successfully !")

def process_etl_pipeline(protocols=True):
    """
    Executes an ETL (Extract, Transform, Load) pipeline to process DeFi protocol data.

    Steps:
    1. Extract key DeFi protocols from a predefined list (KEY_PROTOCOLS).
    2. Transform the extracted data by fetching detailed information for each protocol.
    3. Save the transformed data into a JSON file.

    Logs are generated for each step to facilitate debugging and tracking of the pipeline process.
    """
    logging.info(f"protocols={protocols}")

    if protocols:
        logging.info("====== Starting ETL pipeline ======")
        logging.info("-----Extracting protocols-----")

        protocols_data = []

        for protocol_id in KEY_PROTOCOLS:
            try:
                protocol_info = get_defi_protocol_info(protocol_id)
                if protocol_info:
                    protocols_data.append(protocol_info)
                else:
                    logging.warning(f"No data found for protocol ID: {protocol_id}")
            except Exception as e:
                logging.error(f"Error fetching data for protocol ID: {protocol_id} - {e}")

            time.sleep(2)  # Avoid hitting rate limits

        try:
            output_file = 'data/protocols.json'
            save_to_json(output=protocols_data, filename=output_file)
            logging.info(f"Data successfully saved to '{output_file}'.")
            logging.info(f"-----Protocols extraction completed: {len(protocols_data)} protocols retrieved.-----")
        except Exception as e:
            logging.critical(f"Failed to save data to JSON file: {e}")

    else:
        logging.info("no protocols extraction needed.")