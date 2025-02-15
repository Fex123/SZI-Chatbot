from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from typing import Optional
from db_connections import DatabaseConnections
from controllers.message_controller import MessageController
from config import Config
from db.user_service import UserService

app = Flask(__name__)

# Initialize database connection once
db_conn = DatabaseConnections()
db_conn.connect_all()

# Initialize services
message_controller = MessageController()
user_service = UserService()

"""
    Request Body Classes:
"""
class SendMessageRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None
    user_id: str = "dev-user"




"""
    Endpoints:
"""
@app.route('/')
def home():
    return "Welcome to the chat API! Use /api/chat/send to send a message. (Post request with 'query' in JSON body)"

"""
Post a new conversation to the chatbot, receive new conversation.
Example usage:
    - User clicks on "New Chat" button to create a new conversation
"""
# TODO: Kinda works, creates a new chat database entry but doesnt return anything, instead 500 error
@app.route('/api/chat/new', methods=['POST'])
def create_new_chat():
    try:
        data = request.json or {}
        user_id = data.get('user_id', 'dev-user')
        title = data.get('title')

        result = message_controller.create_new_chat(user_id, title)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""
Post a message to the chatbot, receive the result of the conversation.
Example usage:
    - User sends a message to the chatbot using the input
"""
@app.route('/api/chat/send', methods=['POST'])
def send_message():
    try:
        data = request.json
        request_params = SendMessageRequest(**data)

        result = message_controller.send_message_to_dify(
            query=request_params.query,
            conversation_id=request_params.conversation_id,
            user_id=request_params.user_id
        )

        return jsonify(result), 200

    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""
Get chat history from one specific conversation.
Example usage:
    - Click on chat in the sidebar to see the Conversations chat history
"""
# TODO: Broken, example: http://127.0.0.1:5000/api/chat/history/"e7116c61-5e12-441d-a793-5a9922c37a70"
# returns: { "messages": [] }
@app.route('/api/chat/history/<conversation_id>', methods=['GET'])
def get_chat_history(conversation_id):
    try:
        messages = message_controller.message_service.get_conversation_history(conversation_id)
        return jsonify({'messages': list(messages)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""
Get all chats from one specific User
Example usage:
    - When opening the app, display all chats the user had on the sidebar
EXAMPLE CALL: http://127.0.0.1:5000/api/user/dev_user/conversations
RETURNS: {
    "conversations": [
        "e7116c61-5e12-441d-a793-5a9922c37a70",
        "67ae405ae63552191d42c01f"
    ]
}
"""
@app.route('/api/user/<user_id>/conversations', methods=['GET'])
def get_user_conversations(user_id):
    try:
        user = user_service.get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'conversations': user.get('conversations', [])}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""
Get all messages from one specific conversation for a user
Example usage:
    - When opening a chat, display all messages from that chat

Example call:  /api/chat/DB_CONVERSATION_ID/messages?user_id=dev_user
"""
@app.route('/api/chat/<conversation_id>/messages', methods=['GET'])
def get_chat_messages(conversation_id):
    try:
        user_id = request.args.get('user_id', 'dev-user')
        messages = message_controller.get_user_chat_history(conversation_id, user_id)
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""
Get all available conversations for a user
Example usage:
    - When opening the App, display all chats the user had on the sidebar

Example call: http://127.0.0.1:5000/api/chat/conversations?user_id="dev_user"
returns: 
{
    "dify_conversations": {
        "data": [],
        "has_more": false,
        "limit": 20
    },
    "local_conversations": []
}
"""
# TODO: Change DIFYAPI call logic, returns weird stuff
@app.route('/api/chat/conversations', methods=['GET'])
def get_conversations():
    try:
        user_id = request.args.get('user_id', 'dev-user')
        conversations = message_controller.get_user_conversations(user_id)
        return jsonify(conversations), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG)