import requests
from config import Config
from db.message_service import MessageService
from db.user_service import UserService

"""
Message Controller class
Responsible for making requests to Dify API
"""
class MessageController:
    def __init__(self):
        self.message_service = MessageService()
        self.user_service = UserService()

    def send_message_to_dify(self, query, conversation_id, user_id):
        # Ensure user exists
        user = self.user_service.get_user(user_id)
        if not user:
            self.user_service.create_user(user_id)

        payload = {
            "inputs": {},
            "query": query,
            "response_mode": "blocking",
            "conversation_id": conversation_id or "",
            "user": user_id
        }

        response = requests.post(
            f"{Config.DIFY_URL}/chat-messages",
            headers=Config.DIFY_HEADERS,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(f"Dify API error: {response.status_code}")

        response_data = response.json()
        new_conversation_id = response_data.get("conversation_id")
        ai_response = response_data.get("answer", "No response received.")

        # Save to database
        self.message_service.save_message(new_conversation_id, query, ai_response)

        if new_conversation_id:
            self.user_service.add_conversation(user_id, new_conversation_id)

        return {
            'conversation_id': new_conversation_id,
            'response': ai_response
        }

    def create_new_chat(self, user_id, title=None):
        # Create conversation first
        conversation = self.message_service.create_conversation(user_id, title)
        
        # Only add to user if it's a new conversation
        if conversation.get('_id'):  # New conversation was created
            self.user_service.add_conversation(user_id, conversation['conversation_id'])
            
        return conversation

    def get_user_chat_history(self, conversation_id, user_id):
        # Get chat history from Dify API
        response = requests.get(
            f"{Config.DIFY_URL}/messages",
            headers=Config.DIFY_HEADERS,
            params={'conversation_id': conversation_id, 'user': user_id}
        )
        
        if response.status_code != 200:
            raise Exception(f"Dify API error: {response.status_code}")
            
        return response.json()

    def get_user_conversations(self, user_id):
        # Get conversations from Dify API
        response = requests.get(
            f"{Config.DIFY_URL}/conversations",
            headers=Config.DIFY_HEADERS,
            params={'user': user_id}
        )
        
        if response.status_code != 200:
            raise Exception(f"Dify API error: {response.status_code}")
            
        dify_conversations = response.json()
        
        # Get local conversations
        local_conversations = self.message_service.get_conversations(user_id)
        
        return {
            'dify_conversations': dify_conversations,
            'local_conversations': list(local_conversations)
        }
