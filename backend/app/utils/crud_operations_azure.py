import pymongo
from typing import Any, Dict, List, Union
import logging 
import os
from dotenv import load_dotenv, find_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv(find_dotenv())

CONNECTION_STRING = os.environ.get("MONGODB_STRING")
DB_NAME = "myFitnessAIcoach"

REQUIRED_KEYS = {"intensity", "calories_burned", "targeted_muscles"}

def validate_keys(data: Dict[str, Any], required_keys: set) -> bool:
    """Validate that the provided data contain the required keys."""
    if set(data.keys()) != required_keys:
        raise ValueError(f"JSON data keys do not match required keys: {required_keys}")
    return True

def delete_document(collection: pymongo.collection.Collection, document_id: Any) -> None:
    """Delete the document containing document_id from the collection"""
    collection.delete_one({"_id": document_id})
    logger.info("Deleted document with _id {}".format(document_id))

def read_document(collection: pymongo.collection.Collection, document_id: Any) -> Dict[str, Any]:
    """Return the contents of the document containing document_id"""
    document = collection.find_one({"_id": document_id})
    logger.info("Found a document with _id {}: {}".format(document_id, document))
    return document

def update_document_id(collection: pymongo.collection.Collection, document_id: Any, update_data: Dict[str, Any]) -> None:
    """Update the document containing document_id with update_data"""
    validate_keys(update_data, REQUIRED_KEYS)
    collection.update_one({"_id": document_id}, {"$set": update_data})
    logger.info("Updated document with _id {}: {}".format(document_id, collection.find_one({"_id": document_id})))

def insert_document(collection: pymongo.collection.Collection, document_data: Dict[str, Any]) -> Any:
    """Insert a document with document_data and return the contents of its _id field"""
    validate_keys(document_data, REQUIRED_KEYS)
    document_id = collection.insert_one(document_data).inserted_id
    logger.info("Inserted document with _id {}".format(document_id))
    return document_id

def create_collection_if_not_exists(client: pymongo.MongoClient, collection_name: str) -> pymongo.collection.Collection:
    """Create a collection if it doesn't exist"""
    db = client[DB_NAME]
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        logger.info("Created collection {}".format(collection_name))
    return db[collection_name]

def retrieve_all_values_for_key(collection: pymongo.collection.Collection, key: str) -> List[Union[Any, Dict[str, Any]]]:
    """Retrieve all values for a specific key in the collection, and if the value is a dictionary, 
    like in the case for the targeted_muscles, then it outputs the dictionaries."""
    values = collection.find({}, {key: 1, '_id': 0})
    result = []
    
    for value in values:
        if key in value:
            val = value[key]
            if isinstance(val, dict):
                result.append({k: v for k, v in val.items()})
            else:
                result.append(val)
    return result

def server_crud_operations(operation: str, json_data: Dict[str, Any] = None, collection_name: str = None, key: str = None, value: Any = None, 
         update_data: Dict[str, Any] = None, document_id: int = None, ) -> None:
    """Connect to the API for MongoDB, create DB and collection, and perform CRUD operations"""
    client = pymongo.MongoClient(CONNECTION_STRING)
    try:
        client.server_info()  # Validate connection string
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")

    if operation == "create" and collection_name:
        create_collection_if_not_exists(client, collection_name)

    elif operation == "insert" and json_data and collection_name:
        collection = create_collection_if_not_exists(client, collection_name)
        insert_document(collection, json_data)

    elif operation == "read" and collection_name and key and value:
        collection = create_collection_if_not_exists(client, collection_name)
        read_document(collection, key, value)

    elif operation == "update_by_id" and collection_name and document_id and update_data:
        collection = create_collection_if_not_exists(client, collection_name)
        update_document_id(collection, document_id, update_data)

    elif operation == "delete" and collection_name and document_id:
        collection = create_collection_if_not_exists(client, collection_name)
        delete_document(collection, document_id)
    else:
        logger.error("Invalid operation or missing parameters")

def find_all_documents(collection: pymongo.collection.Collection) -> List[Dict[str, Any]]:
    return list(collection.find({}))
