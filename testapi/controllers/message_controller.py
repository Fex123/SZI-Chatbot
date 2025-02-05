import requests
from config import Config
from db.message_service import MessageService
from db.user_service import UserService

class MessageController:
    def __init__(self):
        self.message_service = MessageService()
        self.user_service = UserService()

    def send_message_to_dify(self, query, conversation_id=None, user_id="dev-user"):
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
