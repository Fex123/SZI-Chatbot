import requests
from config import Config
from services.message_service import MessageService 
from services.user_service import UserService      

"""
Message Controller class
Responsible for making requests to Dify API
"""
class MessageController:
    def __init__(self):
        self.message_service = MessageService()
        self.user_service = UserService()

    def send_message_to_dify(self, query, conversation_id, user_id):
        if not user_id:
            raise ValueError("Authenticated user is required")
            
        try:
            # Ensure user exists first
            user = self.user_service.get_user(user_id)
            if not user:
                raise ValueError("User not found")

            # Check if this is part of an existing conversation
            existing_conv = None
            if conversation_id:
                existing_conv = self.message_service.load_message(conversation_id)

            payload = {
                "inputs": {},
                "query": query,
                "response_mode": "blocking",
                "conversation_id": existing_conv['conversation_id'] if existing_conv else None,
                "user": user_id
            }

            print(f"Sending request to Dify with payload: {payload}")

            response = requests.post(
                f"{Config.DIFY_URL}/chat-messages",
                headers=Config.DIFY_HEADERS,
                json=payload
            )
            if response.status_code != 200:
                print(f"Dify API error response: {response.text}")
                raise Exception(f"Dify API error: {response.status_code}. Details: {response.text}")

            response_data = response.json()
            new_conversation_id = response_data.get("conversation_id")
            ai_response = response_data.get("answer", "No response received.")

            # Use existing conversation_id if available, otherwise use new one
            final_conversation_id = conversation_id or new_conversation_id

            if final_conversation_id and ai_response:
                # Save message and ensure conversation is linked to user
                self.message_service.save_message(
                    final_conversation_id,
                    query,
                    ai_response,
                    user_id
                )
                
                # Always try to add conversation to user's list
                self.user_service.add_conversation(user_id, final_conversation_id)

            return {
                'conversation_id': final_conversation_id,
                'response': ai_response
            }

        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            raise Exception(f"Failed to communicate with Dify API: {str(e)}")

    def create_new_chat(self, user_id, title=None):
        if not user_id:
            raise ValueError("Authenticated user is required")
            
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
