from pymongo import MongoClient
from config import Config

def check_mongodb_collections(mongo_client):
    try:
        db = mongo_client[Config.MONGO_DB_NAME]
        collections = db.list_collection_names()
        return 'users' in collections
    except Exception:
        return False

def init_mongodb_collections(mongo_client):
    db = mongo_client[Config.MONGO_DB_NAME]
    
    # Create users collection with schema
    if 'users' not in db.list_collection_names():
        users_collection = db.create_collection('users')
        users_collection.create_index([('user_id', 1)], unique=True)
        users_collection.create_index([('conversation_id', 1)], unique=True)
        print("Users collection created successfully")

if __name__ == '__main__':
    mongo_client = MongoClient(Config.MONGO_URI)
    
    # Check and initialize MongoDB collections
    if not check_mongodb_collections(mongo_client):
        init_mongodb_collections(mongo_client)
        print("MongoDB collections initialized successfully")
    else:
        print("MongoDB collections already exist")
