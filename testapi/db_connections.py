from pymongo import MongoClient
import time
from config import Config

class DatabaseConnections:
    def __init__(self):
        self.mongodb_client = None

    def connect_all(self):
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
                # Test MongoDB connection
                self.mongodb_client.server_info()
                
                print("MongoDB connection established successfully!")
                return
                
            except Exception as e:
                print(f"Connection error: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise Exception(f"Failed to connect after {max_retries} attempts")

    def close_all(self):
        if self.mongodb_client:
            self.mongodb_client.close()

    def get_mongodb(self):
        if not self.mongodb_client:
            self.connect_all()
        return self.mongodb_client[Config.MONGO_DB_NAME]
