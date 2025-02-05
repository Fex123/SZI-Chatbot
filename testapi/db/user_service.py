from db_connections import DatabaseConnections
from datetime import datetime

class UserService:
    def __init__(self):
        self.db_conn = DatabaseConnections()
        self.db = self.db_conn.get_mongodb()
        self.users_collection = self.db.users

    def create_user(self, user_id):
        user_doc = {
            'user_id': user_id,
            'created_at': datetime.now(),
            'conversations': []
        }
        return self.users_collection.insert_one(user_doc)

    def get_user(self, user_id):
        return self.users_collection.find_one({'user_id': user_id})

    def add_conversation(self, user_id, conversation_id):
        return self.users_collection.update_one(
            {'user_id': user_id},
            {'$addToSet': {'conversations': conversation_id}}
        )
