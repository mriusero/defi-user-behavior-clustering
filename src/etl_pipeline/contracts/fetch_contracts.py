import hashlib
import logging

from ..mongodb_handler import get_mongo_collection


def generate_contract_id(adress):
    """
    Generate a unique contract_id based on the contract adress.
    :param:
        adress (str): The name of the protocol.
    :return:
        str: A unique protocol_id.
    """
    normalized_name = adress.strip().lower()                                  # Normalize the name (lowercase and strip whitespace)
    contract_id = hashlib.md5(normalized_name.encode()).hexdigest()           # Generate a hash from the normalized name

    return contract_id


def deduct_contracts():
    """
    Extracts contracts from protocols and adds them to the 'contracts' collection in the database, ensuring
    that contracts are only added if they do not already exist. This function processes each protocol in the
    'protocols' collection and extracts relevant contract details, including contract address, blockchain, and
    protocol metadata. If the contract does not exist in the 'contracts' collection, it is inserted; otherwise,
    the function logs that the contract already exists.
    The function uses MongoDB's update_one method with the 'upsert' option to either insert or skip contracts as appropriate.
    :return:
        None
    """

    # Set up logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("Starting contract extraction and insertion process.")

    try:
        protocols_collection = get_mongo_collection(
            db_name='defi_db',
            collection_name='protocols',
        )
        contracts_collection = get_mongo_collection(
            db_name='defi_db',
            collection_name='contracts',
        )

        # Retrieve all protocols from the collection
        protocols_cursor = protocols_collection.find()

        # Process each protocol to extract contracts and add to the 'contracts' collection
        for protocol in protocols_cursor:
            protocol_id = protocol["protocol_id"]
            description = protocol["description"]
            name = protocol["name"]
            symbol = protocol["symbol"]
            type_ = protocol["type"]
            website_url = protocol["website_url"]

            for blockchain_contract in protocol["blockchain_contracts"]:
                blockchain = blockchain_contract["blockchain"]
                contract_address = blockchain_contract["contract"]

                contract_document = {
                    "contract_id": generate_contract_id(contract_address),  # Generate the ID for the contract
                    "contract_address": contract_address,
                    "protocol_name": name,
                    "protocol_id": protocol_id,
                    "protocol_symbol": symbol,
                    "blockchain": blockchain,
                    "description": description,
                    "type": type_,
                    "website_url": website_url,
                }

                result = contracts_collection.update_one(
                    {"contract_id": generate_contract_id(contract_address)},
                    {"$setOnInsert": contract_document},
                    upsert=True
                )

                if result.upserted_id:
                    logging.info(f"Contract {contract_address} on {blockchain} added to the 'contracts' collection.")
                else:
                    logging.info(f"Contract {contract_address} already exists in the 'contracts' collection.")

        logging.info("Contracts collection has been fully processed.")

    except Exception as e:
        logging.error(f"An error occurred while processing contracts: {e}")