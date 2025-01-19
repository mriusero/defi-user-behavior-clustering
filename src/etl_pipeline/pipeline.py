import logging

from .contracts import deduct_contracts
from .protocols import extract_protocols, load_protocols
from .transactions import process_ethereum_contracts
from .users import extract_users
from .price import fetch_prices
from .market import improve_market

def process_etl_pipeline(protocols=False, contracts=False, transactions=False, users=False, price=False, market=False):
    """
    Executes an ETL (Extract, Transform, Load) pipeline to process DeFi protocol data.
    """
    logging.info("====== PARAMETERS ======")
    logging.info(f"--> protocols={protocols}")
    logging.info(f"--> contracts={contracts}")
    logging.info(f"--> transactions={transactions}")
    logging.info(f"--> users={users}")
    logging.info(f"--> price={price}")
    logging.info(f"--> market={market}\n")

    logging.info("====== Starting ETL pipeline ======")

    # Etape 1 : Extraction des protocoles
    if protocols:
        logging.info("------ Step 1: Extracting Protocols ------")
        protocols_data = extract_protocols()
        load_protocols(protocols_data)
        logging.info(f"Protocols extraction completed: {len(protocols_data)} protocols retrieved.\n")
    else:
        logging.info("No protocols extraction asked. Skipping step 1.\n")

    # Etape 2 : Déduction des contrats
    if contracts:
        logging.info("------ Step 2: Deducting Contracts ------")
        deduct_contracts()
        logging.info("Contracts deducted successfully.\n")
    else:
        logging.info("No contract deduction asked. Skipping step 2.\n")

    # Etape 3 : Extraction des transactions associées aux contrats
    if transactions:
        logging.info("------ Step 3: Fetching Associated Transactions ------")
        process_ethereum_contracts(
            start_date='2023-01-01',
            end_date='2024-12-31'
        )
        logging.info("Transactions Fetched successfully.\n")
    else:
        logging.info("No transactions fetching asked. Skipping step 3.\n")

    # Etape 4 : Extraction des utilisateurs associés aux transactions
    if users:
        logging.info("------ Step 4: Extracting User Data ------")
        extract_users()
        logging.info("User data extraction completed.\n")
    else:
        logging.info("No user data extraction asked. Skipping step 4.\n")

    # Etape 5 : Extraction des prix sur la période
    if price:
        logging.info("------ Step 5: Fetching Cryptocurrency Prices ------")
        fetch_prices()
        logging.info("Cryptocurrency prices fetched successfully.\n")
    else:
        logging.info("No cryptocurrency price fetching asked. Skipping step 5.\n")

    # Etape 6 : Enrichissement des données de marché
    if market:
        logging.info("------ Step 6: Enriching Market Data ------")
        improve_market(
            start_date='2023-01-01',
            end_date='2024-12-31'
        )
        logging.info("Market data enriched successfully.\n")
    else:
        logging.info("No market data enrichment asked. Skipping step 6.\n")


    logging.info("ETL pipeline completed.")