import json
import requests
import logging

from .config import ETH_API_KEY


def reset_log_file():
    """
    Reset the log file to avoid duplicate logs.
    :return: Empty log file.
    """
    for handler in logging.root.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            handler.stream.close()
            logging.root.removeHandler(handler)

    logging.basicConfig(filename='votre_fichier_de_log.log', level=logging.INFO)


def save_to_json(output, filename):
    """
        Saves API output to a JSON file.
        :param:
            output (Dict): The API output to be saved, in Python dictionary format.
            filename (str): The name of the file to save the JSON data.
        """
    with open(filename, 'w') as f:
        json.dump(output, f, indent=4)


def get_block_by_timestamp(timestamp: int, closest: str = "before"):
    """
    Retrieves the block number from a timestamp using the Etherscan API.

    :param timestamp: The timestamp to search for. (int)
    :param closest: Defines whether to return the block before or after the timestamp. Defaults to "before". (str)
    :return: The block number closest to the specified timestamp. (int)
    :raise ValueError: If there is an error retrieving the block number from the API.
    """
    url = "https://api.etherscan.io/api"  # Correct endpoint for block lookup
    params = {
        "module": "block",
        "action": "getblocknobytime",
        "timestamp": timestamp,
        "closest": closest,
        "apikey": ETH_API_KEY,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise ValueError(f"HTTP error: {response.status_code}, response: {response.text}")

    data = response.json()

    if data.get("status") == "1" and "result" in data:
        return int(data["result"])
    elif data.get("status") == "0":
        raise ValueError(f"Error retrieving block: {data.get('message', 'Unknown error')}")
    else:
        raise ValueError("Unexpected response structure")