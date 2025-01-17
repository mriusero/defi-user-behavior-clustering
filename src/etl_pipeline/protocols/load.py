import logging
from ..mongodb_handler import get_mongo_collection


def load_protocols(protocols_data):
    """
    Loads the extracted data either into MongoDB or into a JSON file.
    :param:
        protocols_data (list): List of protocol data dictionaries containing details like 'protocol_id' and 'name'.
        save_to_mongo (bool): Boolean flag to determine whether to save data to MongoDB or JSON file.
    """

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