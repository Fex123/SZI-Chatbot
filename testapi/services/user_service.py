from db_connections import DatabaseConnections
from datetime import datetime
import uuid
from typing import Optional, List
from utils.bcrypt_singleton import BcryptSingleton
from models.user import User

"""
UserService class
Responsible for handling operations related to user data in the database
"""
class UserService:
    def __init__(self):
        db = DatabaseConnections().get_mongodb()
        self.users_collection = db.users
        self.bcrypt = BcryptSingleton.get_instance().get_bcrypt()

    def _create_user_object(self, username: str, password: str, display_name: Optional[str] = None) -> User:
        return User(
            user_id=str(uuid.uuid4()),
            username=username,
            display_name=display_name or username,
            password_hash=self.bcrypt.generate_password_hash(password).decode('utf-8'),
            created_at=datetime.now(),
            last_login=None,
            is_active=True,
            conversations=[]
        )

    def create_user(self, username: str, password: str, display_name: Optional[str] = None) -> User:
        if self.get_user_by_username(username):
            raise ValueError('Username already exists')

        user = self._create_user_object(username, password, display_name)
        self.users_collection.insert_one(user.model_dump())
        return user

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user_doc = self.users_collection.find_one({'username': username})
        if not user_doc or not self.bcrypt.check_password_hash(user_doc['password_hash'], password):
            return None

        self.users_collection.update_one(
            {'_id': user_doc['_id']},
            {'$set': {'last_login': datetime.now()}}
        )
        return User(**user_doc)

    # Account Management
    def update_user(self, user_id: str, update_data: dict) -> bool:
        allowed_updates = {'display_name', 'is_active'}
        update_fields = {k: v for k, v in update_data.items() if k in allowed_updates}
        
        if not update_fields:
            return False

        result = self.users_collection.update_one(
            {'user_id': user_id},
            {'$set': update_fields}
        )
        return result.modified_count > 0

    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        user = self.get_user(user_id)
        if not user or not self.bcrypt.check_password_hash(user.password_hash, old_password):
            raise ValueError('Invalid credentials')

        new_hash = self.bcrypt.generate_password_hash(new_password).decode('utf-8')
        result = self.users_collection.update_one(
            {'user_id': user_id},
            {'$set': {'password_hash': new_hash}}
        )
        return result.modified_count > 0

    # Conversation Management
    def add_conversation(self, user_id: str, conversation_id: str) -> bool:
        result = self.users_collection.update_one(
            {'user_id': user_id},
            {'$addToSet': {'conversations': conversation_id}}
        )
        return result.modified_count > 0

    # Query Methods
    def get_user(self, user_id: str) -> Optional[User]:
        user_doc = self.users_collection.find_one({'user_id': user_id})
        return User(**user_doc) if user_doc else None

    def get_user_by_username(self, username: str) -> Optional[User]:
        user_doc = self.users_collection.find_one({'username': username})
        return User(**user_doc) if user_doc else None
