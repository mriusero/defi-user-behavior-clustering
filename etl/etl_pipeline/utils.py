import json
import logging
import os
import requests


def clear_log_file(log_filename="logs/etl_pipeline.log"):
    """
    Vide le fichier de logs spécifié.
    """
    if os.path.exists(log_filename):
        open(log_filename, "w").close()  # Ouvre le fichier en mode écriture et le vide
        print(f"[INFO] Le fichier de logs '{log_filename}' a été vidé.")
    else:
        print(f"[WARNING] Le fichier de logs '{log_filename}' n'existe pas.")


def save_to_json(output, filename):
    """
    Saves API output to a JSON file.
    :param:
        output (Dict): The API output to be saved, in Python dictionary format.
        filename (str): The name of the file to save the JSON data.
    """
    with open(filename, "w") as f:
        json.dump(output, f, indent=4)


def get_block_by_timestamp(timestamp: int, closest: str = "before"):
    """
    Retrieves the block number from a timestamp using the Etherscan API.

    :param timestamp: The timestamp to search for. (int)
    :param closest: Defines whether to return the block before or after the timestamp. Defaults to "before". (str)
    :return: The block number closest to the specified timestamp. (int)
    :raise ValueError: If there is an error retrieving the block number from the API.
    """
    from .config import ETH_API_KEY

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
        raise ValueError(
            f"HTTP error: {response.status_code}, response: {response.text}"
        )

    data = response.json()

    if data.get("status") == "1" and "result" in data:
        return int(data["result"])
    elif data.get("status") == "0":
        raise ValueError(
            f"Error retrieving block: {data.get('message', 'Unknown error')}"
        )
    else:
        raise ValueError("Unexpected response structure")
