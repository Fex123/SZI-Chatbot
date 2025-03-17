from db_connections import DatabaseConnections
from datetime import datetime
from bson import ObjectId
from typing import Dict, List, Optional, Union
from models.message import Message
from models.conversation import Conversation

"""
MessageService class
Responsible for handling message operations in the database
"""
class MessageService:
    def __init__(self):
        db = DatabaseConnections().get_mongodb()
        self.messages_collection = db.messages

    # Validation Methods
    def _validate_user_id(self, user_id: str) -> None:
        if not user_id:
            raise ValueError("user_id is required")

    def _validate_conversation_exists(self, conversation_id: str, user_id: str) -> Dict:
        conversation = self.messages_collection.find_one({
            'conversation_id': conversation_id,
            'user_id': user_id
        })
        if not conversation:
            raise ValueError("Conversation not found or access denied")
        return conversation

    # Conversation Management
    def create_conversation(self, user_id: str, title: Optional[str] = None) -> Conversation:
        self._validate_user_id(user_id)
        now = datetime.now()
        conversation = Conversation(
            conversation_id=str(ObjectId()),
            user_id=user_id,
            title=title or "New Conversation",
            messages=[],
            created_at=now,
            updated_at=now
        )
        self.messages_collection.insert_one(conversation.model_dump())
        return conversation

    def get_conversations(self, user_id: str) -> List[Dict]:
        self._validate_user_id(user_id)
        return list(self.messages_collection.find(
            {'user_id': user_id},
            {'_id': 0, 'conversation_id': 1, 'title': 1, 'created_at': 1, 'updated_at': 1}
        ).sort('created_at', -1))

    def update_conversation_title(self, conversation_id: str, new_title: str) -> bool:
        result = self.messages_collection.update_one(
            {'conversation_id': conversation_id},
            {'$set': {'title': new_title, 'updated_at': datetime.now()}}
        )
        return result.modified_count > 0

    def get_formatted_conversations(self, user_id: str) -> List[Dict]:
        self._validate_user_id(user_id)
        
        conversations = self.get_conversations(user_id)
        return [{
            'id': conv['conversation_id'],
            'title': conv.get('title', 'Untitled Chat'),
            'created_at': conv['created_at'],
            'updated_at': conv['updated_at']
        } for conv in conversations]

    # Message Operations
    def save_message(self, conversation_id: str, user_message: str, ai_response: str, user_id: str) -> str:
        self._validate_user_id(user_id)
        now = datetime.now()
        
        messages = [
            Message(role='user', content=user_message, timestamp=now),
            Message(role='assistant', content=ai_response, timestamp=now)
        ]

        if not conversation_id:
            return self._create_new_conversation_with_messages(user_id, messages, user_message)
        
        return self._add_messages_to_existing_conversation(conversation_id, user_id, messages)

    def _create_new_conversation_with_messages(self, user_id: str, messages: List[Message], 
                                            initial_message: str) -> str:
        conversation = self.create_conversation(
            user_id=user_id,
            title=f"Chat about: {initial_message[:30]}..."
        )
        self.messages_collection.update_one(
            {'conversation_id': conversation.conversation_id},
            {'$set': {'messages': [m.model_dump() for m in messages]}}
        )
        return conversation.conversation_id

    def _add_messages_to_existing_conversation(self, conversation_id: str, user_id: str, 
                                           messages: List[Message]) -> str:
        self._validate_conversation_exists(conversation_id, user_id)
        self.messages_collection.update_one(
            {'conversation_id': conversation_id},
            {
                '$push': {'messages': {'$each': [m.model_dump() for m in messages]}},
                '$set': {'updated_at': datetime.now()}
            }
        )
        return conversation_id

    def get_conversation_history(self, conversation_id: str, user_id: str) -> List[Dict]:
        self._validate_user_id(user_id)
        
        conversation = self.messages_collection.find_one(
            {
                'conversation_id': conversation_id,
                'user_id': user_id
            },
            {
                'messages': 1,
                'created_at': 1,
                '_id': 0
            }
        )
        
        if not conversation:
            return []
            
        return [conversation]

    def process_message(self, query: str, conversation_id: Optional[str], 
                       user_id: str) -> Optional[str]:
        self._validate_user_id(user_id)
        
        if not conversation_id:
            return None
            
        try:
            self._validate_conversation_exists(conversation_id, user_id)
            return conversation_id
        except ValueError:
            return None
