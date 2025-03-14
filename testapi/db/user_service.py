from db_connections import DatabaseConnections
from datetime import datetime
import uuid
from flask_bcrypt import Bcrypt
from flask import current_app

"""
UserService class
Responsible for handling operations related to user data in the database
"""
class UserService:
    def __init__(self):
        db = DatabaseConnections().get_mongodb()
        self.users_collection = db.users
        self.bcrypt = Bcrypt(current_app)

    def create_user(self, username, password, display_name=None):
        """Create a new user with hashed password"""
        existing_user = self.users_collection.find_one({'username': username})
        if existing_user:
            raise ValueError('Username already exists')

        user_doc = {
            'user_id': str(uuid.uuid4()),
            'username': username,
            'display_name': display_name or username,
            'password_hash': self.bcrypt.generate_password_hash(password).decode('utf-8'),
            'created_at': datetime.now(),
            'last_login': None,
            'is_active': True,
            'conversations': []
        }
        
        result = self.users_collection.insert_one(user_doc)
        user_doc['_id'] = result.inserted_id
        return user_doc

    def authenticate_user(self, username, password):
        """Authenticate user and return user document if successful"""
        user = self.users_collection.find_one({'username': username})
        if user and self.bcrypt.check_password_hash(user['password_hash'], password):
            # Update last login time
            self.users_collection.update_one(
                {'_id': user['_id']},
                {'$set': {'last_login': datetime.now()}}
            )
            return user
        return None

    def get_user(self, user_id):
        """Get user by user_id"""
        return self.users_collection.find_one({'user_id': user_id})

    def get_user_by_username(self, username):
        """Get user by username"""
        return self.users_collection.find_one({'username': username})

    def update_user(self, user_id, update_data):
        """Update user details"""
        allowed_updates = ['display_name', 'is_active']
        update_fields = {k: v for k, v in update_data.items() if k in allowed_updates}
        
        if update_fields:
            return self.users_collection.update_one(
                {'user_id': user_id},
                {'$set': update_fields}
            )
        return None

    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        user = self.get_user(user_id)
        if not user:
            raise ValueError('User not found')
            
        if not self.bcrypt.check_password_hash(user['password_hash'], old_password):
            raise ValueError('Invalid old password')
            
        new_hash = self.bcrypt.generate_password_hash(new_password).decode('utf-8')
        self.users_collection.update_one(
            {'user_id': user_id},
            {'$set': {'password_hash': new_hash}}
        )
        return True

    def add_conversation(self, user_id, conversation_id):
        """Add conversation to user's list"""
        return self.users_collection.update_one(
            {'user_id': user_id},
            {'$addToSet': {'conversations': conversation_id}}
        )

    def get_user_conversations(self, user_id):
        """Get all conversations for a user"""
        user = self.get_user(user_id)
        return user.get('conversations', []) if user else []
