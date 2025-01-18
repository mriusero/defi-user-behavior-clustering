import logging

from pymongo import MongoClient


def get_mongo_client(mongo_uri="mongodb://localhost:27017/"):
    """
    Connects to a MongoDB server and returns the client object.
    :param:
        mongo_uri (str): URI of the MongoDB server. Default is 'mongodb://localhost:27017'.
    :return:
        MongoClient: The MongoDB client object.
    :raise:
        ValueError: If the URI is invalid.
    """
    try:
        client = MongoClient(mongo_uri)
        logging.info(f"Connected to MongoDB at {mongo_uri}")
        return client
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        raise ValueError(f"Invalid URI: {mongo_uri}")


def get_mongo_collection(db_name, collection_name, mongo_uri="mongodb://localhost:27017"):
    """
    Returns a MongoDB collection object.
    :param:
        db_name (str): Name of the database.
        collection_name (str): Name of the collection.
        mongo_uri (str): URI of the MongoDB server. Default is 'mongodb://localhost:27017'.
    :return:
        Collection: The requested MongoDB collection object.
    :raise:
        ConnectionError: If the connection to MongoDB fails.
    """
    try:
        client = MongoClient(mongo_uri)  # Connect to the MongoDB server
        database = client[db_name]  # Access the database
        collection = database[collection_name]  # Access the collection

        return collection
    except Exception as e:
        raise ConnectionError(f"Failed to connect to MongoDB: {e}")