from db_connections import DatabaseConnections
from datetime import datetime

"""
UserService class
Responsible for handling user data operations in the database
"""
class UserService:
    def __init__(self):
        db = DatabaseConnections().get_mongodb()
        self.users_collection = db.users

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
        # Create user if doesn't exist
        user = self.get_user(user_id)
        if not user:
            self.create_user(user_id)
            
        # Add conversation to user's list
        return self.users_collection.update_one(
            {'user_id': user_id},
            {'$addToSet': {'conversations': conversation_id}}
        )
