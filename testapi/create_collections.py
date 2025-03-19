from pymongo import MongoClient, ASCENDING
from config import Config

# Function to initialize MongoDB collections with schema validation and indexes
# This function will be called when the script is run
def init_mongodb_collections():
    """Initialize MongoDB collections with schema validation and indexes"""
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
        # Remove the unique constraint from the compound index
        messages_collection.create_index([
            ('user_id', ASCENDING),
            ('title', ASCENDING)
        ])
        print("Messages collection created successfully with indexes")

    # Create tokens collection if it doesn't exist
    if 'tokens' not in db.list_collection_names():
        tokens_collection = db.create_collection('tokens')
        # Create indexes for token management
        tokens_collection.create_index([('token', ASCENDING)], unique=True)
        tokens_collection.create_index([('user_id', ASCENDING)])
        tokens_collection.create_index([('expiry', ASCENDING)])
        print("Tokens collection created successfully with indexes")

    # Create top_queries collection if it doesn't exist
    if 'top_queries' not in db.list_collection_names():
        top_queries_collection = db.create_collection('top_queries')
        # Create indexes for efficient querying
        top_queries_collection.create_index([('created_at', ASCENDING)])
        top_queries_collection.create_index([('query', ASCENDING)])
        print("Top queries collection created successfully with indexes")

    client.close()
    print("All collections initialized successfully!")

if __name__ == '__main__':
    print("Initializing MongoDB collections...")
    try:
        init_mongodb_collections()
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
