import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import requests

from .load import upsert_transactions
from ..config import ETH_API_KEY
from ..mongodb_handler import get_mongo_collection
from ..utils import get_block_by_timestamp


def fetch_transactions(
    contract_address: str,
    start_block: int,
    end_block: int,
    page: int = 1,
    offset: int = 10000,
):
    """
    Retrieves Ethereum transactions related to a contract between two blocks, paginated if necessary.
    """
    url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid": 1,
        "module": "account",
        "action": "tokentx",
        "contractaddress": contract_address,
        "startblock": start_block,
        "endblock": end_block,
        "page": page,
        "offset": offset,
        "sort": "asc",
        "apikey": ETH_API_KEY,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise ValueError(
            f"HTTP error: {response.status_code}, response: {response.text}"
        )

    data = response.json()

    if "status" in data and data["status"] == "1" and "result" in data:
        return data["result"]
    elif (
        "status" in data
        and data["status"] == "0"
        and data["message"] == "No transactions found"
    ):
        return []
    else:
        raise ValueError(
            f"Error retrieving transactions: {data.get('message', 'Unknown error')}"
        )


def fetch_transactions_for_range(
    contract_address: str, start_block: int, end_block: int
):
    """
    Fetches all transactions for a given block range.

    :param contract_address: The Ethereum contract address to fetch transactions for. (str)
    :param start_block: The starting block number for the range. (int)
    :param end_block: The ending block number for the range. (int)

    :return: A list of transactions that occurred within the given block range. (list)

    :raise ValueError: If there is an error fetching transactions from the API for a specific block range.
    """
    transactions = []
    max_transactions = 10000  # API-imposed limit
    block_step = 5000  # Size of block sub-ranges

    current_start = start_block
    while current_start <= end_block:
        current_end = min(current_start + block_step - 1, end_block)
        logging.info(
            f"Fetching transactions for blocks {current_start} to {current_end}"
        )
        try:

            txs = fetch_transactions(
                contract_address, current_start, current_end
            )  # API call for the current block range
            transactions.extend(txs)
            logging.info(
                f"Fetched {len(txs)} transactions for blocks {current_start}-{current_end}"
            )
        except ValueError as e:
            logging.error(
                f"Error fetching transactions for blocks {current_start}-{current_end}: {e}"
            )

        current_start = current_end + 1  # Move to the next block range
    return transactions


def fetch_all_transactions_parallel(
    contract_address: str, start_block: int, end_block: int, max_workers: int = 4
):
    """
    Fetches all transactions in parallel to improve performance.

    :param contract_address: The Ethereum contract address to fetch transactions for. (str)
    :param start_block: The starting block number for the range. (int)
    :param end_block: The ending block number for the range. (int)
    :param max_workers: The maximum number of parallel workers for fetching transactions. Default is 4. (int)

    :return: A list of transactions that occurred within the given block range. (list)

    :raise Exception: If there is an error during the parallel fetching of transactions.
    """
    transactions = []
    block_step = 5000  # Size of block sub-ranges

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        current_start = start_block
        while current_start <= end_block:
            current_end = min(current_start + block_step - 1, end_block)
            futures.append(
                executor.submit(
                    fetch_transactions_for_range,
                    contract_address,
                    current_start,
                    current_end,
                )
            )
            current_start = current_end + 1

        for future in as_completed(futures):
            try:
                result = future.result()
                transactions.extend(result)
            except Exception as e:
                logging.error(f"Error fetching transactions in parallel: {e}")

    return transactions


def process_ethereum_contracts(start_date: str, end_date: str):
    """
    Fetches Ethereum contract transactions within the defined period, handling pagination.

    :param start_date: The start date for the transaction range in 'YYYY-MM-DD' format. (str)
    :param end_date: The end date for the transaction range in 'YYYY-MM-DD' format. (str)

    :return: None

    :raise ValueError: If there is an error fetching or processing transactions for any contract.
    """
    start_block = get_block_by_timestamp(
        int(datetime.strptime(start_date, "%Y-%m-%d").timestamp()), "before"
    )
    end_block = get_block_by_timestamp(
        int(datetime.strptime(end_date, "%Y-%m-%d").timestamp()), "after"
    )
    logging.info(
        f"Fetching transactions between blocks {start_block} and {end_block}..."
    )

    contracts_collection = get_mongo_collection(
        db_name="defi_db", collection_name="contracts"
    )
    ethereum_contracts = contracts_collection.find({"blockchain": "ethereum"})

    for contract in ethereum_contracts:
        protocol_name = contract["protocol_name"]
        type = contract["type"]
        contract_id = contract["contract_id"]
        contract_address = contract["contract_address"]
        blockchain = contract["blockchain"]

        logging.info(
            f"---- Processing contract '{contract_address}' for protocol '{protocol_name}':"
        )

        try:
            transactions = fetch_all_transactions_parallel(
                contract_address, start_block, end_block
            )
            logging.info(
                f"Fetched {len(transactions)} total transactions for contract {contract_address}"
            )

            upsert_transactions(
                protocol_name, type, contract_id, blockchain, transactions
            )
            logging.info(
                f"Successfully fetched and processed {len(transactions)} transactions for contract '{contract_address}' under protocol '{protocol_name}'.\n"
            )

        except ValueError as e:
            logging.error(
                f"Error fetching or processing transactions for contract {contract_address}: {e}"
            )
            continue
