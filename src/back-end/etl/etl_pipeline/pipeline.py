from datetime import datetime
import logging
from rich.console import Console

from .config import setup_logging
from .utils import clear_log_file
from .contracts import deduct_contracts
from .protocols import extract_protocols, load_protocols
from .transactions import process_ethereum_contracts
from .users import extract_users
from .price import fetch_prices
from .market import aggregation_task
from .dataset import generate_dataset, save_mongodb_to_parquet

# INITIALIZE LOGGING
setup_logging()
logger = logging.getLogger()
console = Console()


# PIPELINE
def process_etl_pipeline(
    protocols=False,
    contracts=False,
    transactions=False,
    users=False,
    price=False,
    market=False,
    dataset=False,
    save=False,
):
    """
    Executes an etl (Extract, Transform, Load) pipeline to process DeFi protocol data.
    """
    clear_log_file()

    console.rule("[bold blue]etl Pipeline Parameters")
    logger.info(f"protocols: {protocols}")
    logger.info(f"contracts: {contracts}")
    logger.info(f"transactions: {transactions}")
    logger.info(f"users: {users}")
    logger.info(f"price: {price}")
    logger.info(f"market: {market}")
    logger.info(f"dataset: {dataset}")
    logger.info(f"save: {save}\n")

    console.rule(f"[bold green]Starting etl Pipeline{datetime.now()}")

    # Step 1: Extracting Protocols
    if protocols:
        console.rule("[bold yellow]Step 1: Extracting Protocols")
        logger.info("Extracting protocols...")
        protocols_data = extract_protocols()
        load_protocols(protocols_data)
        logger.info(
            f"Protocols extraction completed: {len(protocols_data)} protocols retrieved.\n"
        )
    else:
        logger.warning("No protocols extraction asked. Skipping step 1.\n")

    # Step 2: Deducting Contracts
    if contracts:
        console.rule("[bold yellow]Step 2: Deducting Contracts")
        logger.info("Deducting contracts...")
        deduct_contracts()
        logger.info("Contracts deducted successfully.\n")
    else:
        logger.warning("No contract deduction asked. Skipping step 2.\n")

    # Step 3: Fetching Associated Transactions
    if transactions:
        console.rule("Step 3: Fetching Associated Transactions")
        logger.info("Fetching associated transactions...")
        process_ethereum_contracts(start_date="2023-01-01", end_date="2024-12-31")
        logger.info("Transactions fetched successfully.\n")
    else:
        logger.warning("No transactions fetching asked. Skipping step 3.\n")

    # Step 4: Extracting User Data
    if users:
        console.rule("Step 4: Extracting User Data")
        logger.info("Extracting user data...")
        extract_users()
        logger.info("User data extraction completed.\n")
    else:
        logger.warning("No user data extraction asked. Skipping step 4.\n")

    # Step 5: Fetching Cryptocurrency Prices
    if price:
        console.rule("Step 5: Fetching Cryptocurrency Prices")
        logger.info("Fetching cryptocurrency prices...")
        fetch_prices()
        logger.info("Cryptocurrency prices fetched successfully.\n")
    else:
        logger.warning("No cryptocurrency price fetching asked. Skipping step 5.\n")

    # Step 6: Enriching Market Data
    if market:
        console.rule("Step 6: Enriching Market Data")
        logger.info("Enriching market data...")
        aggregation_task(start_date="2023-01-01", end_date="2024-12-31")
        logger.info("Market data enriched successfully.\n")
    else:
        logger.warning("No market data enrichment asked. Skipping step 6.\n")

    # Step 7: Generating Dataset
    if dataset:
        console.rule("Step 7: Generating Dataset")
        logger.info("Generating dataset...")
        generate_dataset()
        logger.info("Dataset generated successfully.\n")
    else:
        logger.warning("No dataset generation asked. Skipping step 7.\n")

    # Step 8: Saving Dataset
    if save:
        console.rule("Step 8: Saving Dataset")
        logger.info("Saving dataset...")
        save_mongodb_to_parquet()
        logger.info("Dataset saved successfully.\n")
    else:
        logger.warning("No dataset saving asked. Skipping step 8.\n")

    console.rule("etl Pipeline Completed")
