import os
from pymongo import MongoClient, errors
from dotenv import load_dotenv

load_dotenv()

client = None

def connect_to_db():
    global client
    if client is None:
        try:
            mongo_uri = os.getenv("MONGO_URI")
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            print("Connected to MongoDB")
        except errors.ServerSelectionTimeoutError as err:
            print("Could not connect to MongoDB:", err)
            client = None
    if client:
        mongo_db = os.getenv("MONGO_DB")
        return client[mongo_db]
    return None
