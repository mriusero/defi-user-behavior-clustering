import logging
import time

import requests

from .transform import infer_protocol_type, generate_protocol_id
from ..config import CG_API_KEY, KEY_PROTOCOLS


def get_defi_protocol_info(protocol_id):
    """
    Fetch detailed information about a specific DeFi protocol.
    :param:
        protocol_id (str): The identifier of the protocol to fetch data for.
    :return:
        dict: A dictionary containing protocol information such as name, type, blockchain contracts,
              website URL, symbol, old_market cap rank, and a short description. Returns None if the
              protocol information cannot be retrieved.
    :raise:
        - INFO: Successful data retrieval.
        - WARNING: Non-200 HTTP responses (e.g., 404, 429).
        - ERROR: Exceptions encountered during API requests.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{protocol_id}"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": CG_API_KEY
    }

    try:
        logging.debug(f"Requesting data for protocol ID: {protocol_id}")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            platforms = data.get('platforms', {})

            protocol_info = {
                'protocol_id': generate_protocol_id(data.get('name', 'N/A')),  # Generate the ID
                'name': data.get('name', 'N/A'),
                'type': infer_protocol_type(protocol_id),
                'blockchain_contracts': [
                    {'blockchain': blockchain, 'contract': contract}
                    for blockchain, contract in platforms.items()
                ],
                'website_url': data.get('links', {}).get('homepage', ['N/A'])[0],
                'symbol': data.get('symbol', 'N/A'),
                'market_cap_rank': data.get('market_cap_rank', 'N/A'),
                'description': data.get('description', {}).get('en', '')[:250],
            }

            logging.info(f"Successfully retrieved data for protocol ID: {protocol_id}")
            return protocol_info

        elif response.status_code == 404:
            logging.warning(f"Protocol not found: {protocol_id}")
        elif response.status_code == 429:
            logging.warning("Too many requests. Waiting for 10 seconds...")
            time.sleep(10)  # Wait 10 seconds and retry
            return get_defi_protocol_info(protocol_id)
        else:
            logging.error(f"Unexpected error for protocol ID {protocol_id}: HTTP {response.status_code}")

    except Exception as e:
        logging.error(f"Error while fetching data for protocol ID {protocol_id}: {e}")

    return None


def extract_protocols():
    """
    Extracts data for each protocol from a predefined list of protocols.
    :return:
        List[Dict]: The list of protocol data, where each item is a dictionary containing information about a protocol.
    :raise:
        Exception: If there's an error fetching data for any protocol.
    """
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

        time.sleep(2)       # Avoid hitting rate limits

    return protocols_data
