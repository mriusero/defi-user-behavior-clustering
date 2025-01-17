import logging.config

from .config import LOGGING_CONFIG
from .protocols import extract_protocols, load_protocols
from .contracts import deduct_contracts
from .transactions import process_ethereum_contracts

logging.config.dictConfig(LOGGING_CONFIG)

def process_etl_pipeline(protocols=False, contracts=False, transactions=False):
    """
     Executes an ETL (Extract, Transform, Load) pipeline to process DeFi protocol data.

     :param protocols: Boolean indicating whether to extract and process DeFi protocols.
     :param contracts: Boolean indicating whether to deduct contracts from the extracted protocols.
     :param transactions: Boolean indicating whether to fetch transactions for the deducted contracts.

     Steps:
     1. Extract key DeFi protocols from a predefined list (KEY_PROTOCOLS).
     2. Transform the extracted data by fetching detailed information for each protocol.
     3. Save the transformed data into a JSON file or MongoDB based on user preference.

     Logs are generated for each step to facilitate debugging and tracking of the pipeline process.
     """
    logging.info("====== PARAMETERS ======")
    logging.info(f"--> protocols={protocols}")
    logging.info(f"--> contracts={contracts}")
    logging.info(f"--> transactions={transactions}")
    logging.info("\n")

    logging.info("====== Starting ETL pipeline ======")

    # Etape 1 : Extraction des protocoles
    if protocols:
        logging.info("------ Step 1: Extracting Protocols ------")
        protocols_data = extract_protocols()
        load_protocols(protocols_data)
        logging.info(f"Protocols extraction completed: {len(protocols_data)} protocols retrieved.\n")
    else:
        logging.info("No protocols extraction needed. Skipping step 1.\n")


    # Etape 2 : Déduction des contrats
    if contracts:
        logging.info("------ Step 2: Deducting Contracts ------")
        deduct_contracts()
        logging.info("Contracts deducted successfully.\n")
    else:
        logging.info("No contract deduction needed. Skipping step 2.\n")


    # Etape 3 : Extraction des transactions
    if transactions:
        logging.info("------ Step 3: Fetching Associated Transactions ------")
        process_ethereum_contracts(
            start_date='2024-12-01',
            end_date='2024-12-02'
        )
        logging.info("Transactions Fetched successfully.\n")
    else:
        logging.info("No transactions fetching needed. Skipping step 3.\n")

    logging.info("ETL pipeline completed.")