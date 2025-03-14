from pymongo import MongoClient, ASCENDING
from config import Config

def init_mongodb_collections():
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.MONGO_DB_NAME]
    
    # Create users collection with schema validation
    if 'users' not in db.list_collection_names():
        db.create_collection('users', validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['user_id', 'username', 'password_hash', 'created_at'],
                'properties': {
                    'user_id': {'bsonType': 'string'},
                    'username': {'bsonType': 'string'},
                    'display_name': {'bsonType': 'string'},
                    'password_hash': {'bsonType': 'string'},
                    'created_at': {'bsonType': 'date'},
                    'last_login': {'bsonType': ['date', 'null']},
                    'is_active': {'bsonType': 'bool'},
                    'conversations': {'bsonType': 'array'}
                }
            }
        })
        
        users_collection = db.users
        # Create indexes
        users_collection.create_index([('user_id', ASCENDING)], unique=True)
        users_collection.create_index([('username', ASCENDING)], unique=True)
        print("Users collection created successfully with schema validation and indexes")
    
    # Create messages collection if it doesn't exist
    if 'messages' not in db.list_collection_names():
        messages_collection = db.create_collection('messages')
        # Create indexes for efficient querying
        messages_collection.create_index([('conversation_id', ASCENDING)], unique=True)
        messages_collection.create_index([('timestamp', ASCENDING)])
        messages_collection.create_index([
            ('user_id', ASCENDING),
            ('title', ASCENDING)
        ], unique=True)
        print("Messages collection created successfully with indexes")

    client.close()
    print("All collections initialized successfully!")

if __name__ == '__main__':
    print("Initializing MongoDB collections...")
    try:
        init_mongodb_collections()
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
