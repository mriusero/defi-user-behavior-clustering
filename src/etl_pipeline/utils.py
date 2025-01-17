import json


def save_to_json(output, filename):
    """
        Saves API output to a JSON file.
        :param:
            output (Dict): The API output to be saved, in Python dictionary format.
            filename (str): The name of the file to save the JSON data.
        """
    with open(filename, 'w') as f:
        json.dump(output, f, indent=4)
