from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError
from typing import Optional
from db_connections import DatabaseConnections
from controllers.message_controller import MessageController
from config import Config
from db.user_service import UserService
from datetime import datetime
from utils.json_encoder import CustomJSONProvider

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.json = CustomJSONProvider(app)  # Updated JSON provider configuration

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
    user_id: str = "dev_user"

"""
    Response Classes:
"""
class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: Optional[datetime]

class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime

"""
Root endpoint
GET /
Returns a welcome message
"""
@app.route('/')
def home():
    return "Welcome to the chat API!"

"""
Send a message to the chatbot
POST /api/chat/send

Request body:
{
    "query": "Hello, how are you?",
    "conversation_id": "507f1f77bcf86cd799439011",  # optional
    "user_id": "dev_user"                           # optional
}

Response:
{
    "conversation_id": "507f1f77bcf86cd799439011",
    "response": "Hello! I'm doing well, thank you for asking. How can I help you today?"
}

Example curl:
curl -X POST http://localhost:5000/api/chat/send \
    -H "Content-Type: application/json" \
    -d '{"query": "Hello, how are you?", "conversation_id": "507f1f77bcf86cd799439011"}'
"""
@app.route('/api/chat/send', methods=['POST'])
def send_message():
    try:
        data = request.json
        if 'conversation_id' in data and not data['conversation_id']:
            data['conversation_id'] = None
            
        request_params = SendMessageRequest(**data)

        # Process message using service
        conversation_id = message_controller.message_service.process_message(
            request_params.query,
            request_params.conversation_id,
            request_params.user_id
        )

        # Send message to Dify
        result = message_controller.send_message_to_dify(
            query=request_params.query,
            conversation_id=conversation_id,
            user_id=request_params.user_id
        )

        # Set default title for new conversations
        if not conversation_id and result.get('conversation_id'):
            default_title = f"{request_params.query}"
            message_controller.message_service.update_conversation_title(
                result['conversation_id'],
                default_title
            )

        return jsonify(result), 200

    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


"""
Get all conversations for a user
GET /api/conversations?user_id=dev_user

Query parameters:
- user_id: string (optional, defaults to "dev_user")

Response:
{
    "conversations": [
        {
            "id": "507f1f77bcf86cd799439011",
            "title": "My Chat",
            "created_at": "2024-02-20T15:30:00.000Z",
            "updated_at": "2024-02-20T15:35:00.000Z"
        },
        ...
    ]
}

Example curl:
curl "http://localhost:5000/api/conversations?user_id=dev_user"
"""
@app.route('/api/conversations', methods=['GET'])
def get_user_conversations():
    try:
        user_id = request.args.get('user_id', 'dev_user')
        
        # First check if user exists
        user = user_service.get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get formatted conversations from service
        conversations = message_controller.message_service.get_formatted_conversations(user_id)
        return jsonify({'conversations': conversations}), 200
        
    except Exception as e:
        print(f"Error in get_user_conversations: {e}")
        return jsonify({'error': str(e)}), 500

"""
Get all messages from a conversation
GET /api/conversations/<conversation_id>/messages?user_id=dev_user

Path parameters:
- conversation_id: string (required)

Query parameters:
- user_id: string (optional, defaults to "dev_user")

Response:
{
    "messages": [
        {
            "role": "user",
            "content": "Hello, how are you?",
            "created_at": "2024-02-20T15:30:00.000Z"
        },
        {
            "role": "assistant",
            "content": "Hello! I'm doing well, thank you for asking. How can I help you today?",
            "created_at": "2024-02-20T15:30:01.000Z"
        },
        ...
    ]
}

Example curl:
curl "http://localhost:5000/api/conversations/507f1f77bcf86cd799439011/messages?user_id=dev_user"
"""
@app.route('/api/conversations/<conversation_id>/messages', methods=['GET'])
def get_conversation_messages(conversation_id):
    try:
        user_id = request.args.get('user_id', 'dev_user')
        messages = message_controller.message_service.get_conversation_history(conversation_id)
        
        formatted_messages = [
            MessageResponse(
                role=m['role'],
                content=m['content'],
                created_at=msg['created_at']
            ).model_dump()
            for msg in messages
            for m in msg['messages']
        ]
        
        return jsonify({'messages': formatted_messages}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host= "0.0.0.0", port= 3104, debug=Config.DEBUG)