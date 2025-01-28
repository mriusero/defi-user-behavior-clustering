import logging

from pymongo import MongoClient


def get_mongo_client(mongo_uri="mongodb://localhost:27017/"):
    """
    Connects to a MongoDB server and returns the client object.
    :param: mongo_uri (str): URI of the MongoDB server. Default is 'mongodb://localhost:27017'.
    :return: MongoClient: The MongoDB client object.
    :raise: ValueError: If the URI is invalid.
    """
    try:
        client = MongoClient(mongo_uri)
        logging.info("Connected to MongoDB at %s", mongo_uri)
        return client
    except Exception as e:
        logging.error("Failed to connect to MongoDB: %s", e)
        raise ValueError(f"Invalid URI: {mongo_uri}") from e


def get_mongo_database(db_name):
    """
    Get a specific database from the MongoDB client.
    :param db_name: Name of the database (str)
    :return: Database instance
    """
    client = MongoClient()
    return client[db_name]


def get_mongo_collection(db_name, collection_name):
    """
    Returns a MongoDB collection object.
    :param: db_name (str): Name of the database.
    :param: collection_name (str): Name of the collection.
    :return: Collection: The requested MongoDB collection object.
    :raise: ConnectionError: If the connection to MongoDB fails.
    """
    try:
        client = MongoClient()
        database = client[db_name]
        collection = database[collection_name]

        return collection
    except Exception as e:
        raise ConnectionError(f"Failed to connect to MongoDB: {e}") from e
