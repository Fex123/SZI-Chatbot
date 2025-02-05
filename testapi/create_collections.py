from pymongo import MongoClient, ASCENDING
from config import Config

def init_mongodb_collections():
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.MONGO_DB_NAME]
    
    # Create users collection if it doesn't exist
    if 'users' not in db.list_collection_names():
        users_collection = db.create_collection('users')
        users_collection.create_index([('user_id', 1)], unique=True)
        print("Users collection created successfully with indexes")
    
    # Create messages collection if it doesn't exist
    if 'messages' not in db.list_collection_names():
        messages_collection = db.create_collection('messages')
        # Create indexes for efficient querying
        messages_collection.create_index([('conversation_id', ASCENDING)])
        messages_collection.create_index([('timestamp', ASCENDING)])
        # Compound index for conversation lookup with timestamp sorting
        messages_collection.create_index([
            ('conversation_id', ASCENDING),
            ('timestamp', ASCENDING)
        ])
        print("Messages collection created successfully with indexes")

    client.close()
    print("All collections initialized successfully!")

if __name__ == '__main__':
    print("Initializing MongoDB collections...")
    try:
        init_mongodb_collections()
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
