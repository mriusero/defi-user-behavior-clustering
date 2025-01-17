import logging
from ..mongodb_handler import get_mongo_collection
from ..utils import save_to_json


def load_protocols(protocols_data, save_to_mongo):
    """
    Loads the extracted data either into MongoDB or into a JSON file.
    :param:
        protocols_data (list): List of protocol data dictionaries containing details like 'protocol_id' and 'name'.
        save_to_mongo (bool): Boolean flag to determine whether to save data to MongoDB or JSON file.
    """
    if save_to_mongo:
        try:
            collection = get_mongo_collection(
                db_name="defi_db",                  # Name of the database
                collection_name="protocols"         # Name of the collection
            )

            for protocol in protocols_data:
                unique_filter = {"protocol_id": protocol.get("protocol_id")}

                result = collection.update_one(
                    unique_filter,                  # Filter to find existing document
                    {"$setOnInsert": protocol},     # Data to insert if not found
                    upsert=True                     # Create new document if not found
                )

                if result.upserted_id:
                    logging.info(f"Inserted new protocol '{protocol.get('name')}': with unique ID '{protocol.get('protocol_id')}'")
                else:
                    logging.info(f"Protocol already exists '{protocol.get('name')}': with unique ID '{protocol.get('protocol_id')}'")

        except Exception as e:
            logging.error(f"Failed to insert data into MongoDB: {e}")
    else:
        try:
            output_file = 'data/protocols.json'         # Path to save the JSON file
            save_to_json(
                output=protocols_data,                  # Data to be saved
                filename=output_file                    # File name and path
            )
            logging.info(f"Data successfully saved to '{output_file}'.")
        except Exception as e:
            logging.critical(f"Failed to save data to JSON file: {e}")
