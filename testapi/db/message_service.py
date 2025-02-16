from db_connections import DatabaseConnections
from datetime import datetime
from bson import ObjectId

class MessageService:
    def __init__(self):
        db = DatabaseConnections().get_mongodb()
        self.messages_collection = db.messages

    def save_message(self, conversation_id, user_message, ai_response):
        message_doc = {
            'conversation_id': conversation_id,
            'messages': [
                {'role': 'user', 'content': user_message},
                {'role': 'assistant', 'content': ai_response}
            ],
            'timestamp': datetime.now()
        }
        return self.messages_collection.insert_one(message_doc)
    
    def load_message(self, conversation_id):
        return self.messages_collection.find_one({'conversation_id': conversation_id})

    def get_conversation_history(self, conversation_id):
        return self.messages_collection.find(
            {'conversation_id': conversation_id},
            {
                'messages': 1,
                'timestamp': 1,
                '_id': 0
            }
        ).sort('timestamp', 1)

    def create_conversation(self, user_id, title=None):
        conversation_id = str(ObjectId())
        conversation_doc = {
            'conversation_id': conversation_id,
            'user_id': user_id,
            'title': title or "New Conversation",
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        self.messages_collection.insert_one(conversation_doc)
        return conversation_doc

    def get_conversations(self, user_id):
        return self.messages_collection.find(
            {'user_id': user_id},
            {
                'conversation_id': 1,
                'title': 1,
                'created_at': 1,
                'updated_at': 1,
                '_id': 0
            }
        ).sort('created_at', -1)

    def update_conversation_title(self, conversation_id, new_title):
        return self.messages_collection.update_one(
            {'conversation_id': conversation_id},
            {'$set': {'title': new_title, 'updated_at': datetime.now()}}
        )
