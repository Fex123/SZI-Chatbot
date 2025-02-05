from db_connections import DatabaseConnections
from datetime import datetime

class MessageService:
    def __init__(self):
        self.db_conn = DatabaseConnections()
        self.db = self.db_conn.get_mongodb()
        self.messages_collection = self.db.messages

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
            {'messages': 1, 'timestamp': 1}
        ).sort('timestamp', 1)
