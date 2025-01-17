import json
import requests

from .config import ETH_API_KEY

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
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "block",
        "action": "getblocknobytime",
        "timestamp": timestamp,
        "closest": closest,
        "apikey": ETH_API_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] == "1":
        return int(data["result"])
    else:
        raise ValueError(f"Error retrieving block: {data['message']}")