import logging.config

from .config import LOGGING_CONFIG
from .protocols import extract_protocols, load_protocols
from .contracts import deduct_contracts

logging.config.dictConfig(LOGGING_CONFIG)

def process_etl_pipeline(save_to_mongo=False, protocols=False, contracts=False):
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
    logging.info(f"--> protocols={protocols}")
    logging.info(f"--> contracts={contracts}")
    logging.info("\n")

    logging.info("====== Starting ETL pipeline ======")

    # Etape 1 : Extraction des protocoles
    if protocols:
        logging.info("------ Step 1: Extracting Protocols ------")
        protocols_data = extract_protocols()  # Extraction des données des protocoles
        load_protocols(protocols_data, save_to_mongo)  # Chargement des données dans la destination appropriée
        logging.info(f"Protocols extraction completed: {len(protocols_data)} protocols retrieved.\n")
    else:
        logging.info("No protocols extraction needed. Skipping step 1.\n")

    # Etape 2 : Déduction des contrats
    if contracts:
        logging.info("------ Step 2: Deducting Contracts ------")
        deduct_contracts()  # Déduction des contrats
        logging.info("Contracts deducted successfully.\n")
    else:
        logging.info("No contract deduction needed. Skipping step 2.\n")

    logging.info("ETL pipeline completed.")
