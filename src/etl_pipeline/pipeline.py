import logging.config

from .config import LOGGING_CONFIG
from .protocols import extract_protocols, load_protocols

logging.config.dictConfig(LOGGING_CONFIG)

def process_etl_pipeline(save_to_mongo=False, protocols=False):
    """
     Executes an ETL (Extract, Transform, Load) pipeline to process DeFi protocol data.

     :param save_to_mongo: Boolean indicating whether to save the data to MongoDB.
     :param protocols: Boolean indicating whether to extract and process DeFi protocols.

     Steps:
     1. Extract key DeFi protocols from a predefined list (KEY_PROTOCOLS).
     2. Transform the extracted data by fetching detailed information for each protocol.
     3. Save the transformed data into a JSON file or MongoDB based on user preference.

     Logs are generated for each step to facilitate debugging and tracking of the pipeline process.
     """
    logging.info("====== PARAMETERS ======")
    logging.info(f"--> save_to_mongo={save_to_mongo}")
    logging.info(f"--> protocols={protocols}\n")

    logging.info("====== Starting ETL pipeline ======")

    if protocols:
        logging.info("1. Extracting protocols")
        protocols_data = extract_protocols()                                                            # Extract protocol data
        load_protocols(protocols_data, save_to_mongo)                                                   # Load data into the appropriate destination
        logging.info(f"Protocols extraction completed: {len(protocols_data)} protocols retrieved.\n")
    else:
        logging.info("No protocols extraction needed.\n")

