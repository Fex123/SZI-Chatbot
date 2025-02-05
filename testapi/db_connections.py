from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import time
from config import Config

class DatabaseConnections:
    _instance = None
    _is_initialized = False
    _is_connected = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnections, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._is_initialized:
            self.mongodb_client = None
            self.db = None
            self._is_initialized = True

    def connect_all(self):
        if self._is_connected:
            return self.db

        max_retries = 5
        retry_delay = 3
        
        for attempt in range(max_retries):
            try:
                print(f"\nAttempt {attempt + 1} of {max_retries}")
                
                # MongoDB connection
                print("Connecting to MongoDB...")
                self.mongodb_client = MongoClient(
                    Config.MONGO_URI,
                    serverSelectionTimeoutMS=5000
                )
                
                # Validate connection and database
                self.mongodb_client.server_info()
                self.db = self.mongodb_client[Config.MONGO_DB_NAME]
                
                # Verify required collections exist
                required_collections = ['users', 'messages']
                existing_collections = self.db.list_collection_names()
                
                missing_collections = [
                    coll for coll in required_collections 
                    if coll not in existing_collections
                ]
                
                if missing_collections:
                    raise Exception(
                        f"Missing required collections: {missing_collections}. "
                        "Please run create_collections.py first."
                    )
                
                print("MongoDB connection established successfully!")
                self._is_connected = True
                return self.db
                
            except ConnectionFailure as e:
                print(f"MongoDB connection failure: {str(e)}")
            except ServerSelectionTimeoutError as e:
                print(f"MongoDB server selection timeout: {str(e)}")
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
            
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to connect after {max_retries} attempts")

    def close_all(self):
        if self.mongodb_client is not None:
            self.mongodb_client.close()
            self.mongodb_client = None
            self.db = None
            self._is_connected = False

    def get_mongodb(self):
        if not self._is_connected or self.mongodb_client is None:
            return self.connect_all()
        return self.db
