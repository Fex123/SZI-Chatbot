from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError
from typing import Optional
from db_connections import DatabaseConnections
from controllers.message_controller import MessageController
from config import Config
from db.user_service import UserService
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


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

class CreateNewChatRequest(BaseModel):
    user_id: str = "dev-user"
    title: Optional[str] = None

class GetConversationRequest(BaseModel):
    user_id: str = "dev-user"
    conversation_id: str

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
    timestamp: datetime

"""
Root endpoint
GET /
Returns a welcome message
"""
@app.route('/')
def home():
    return "Welcome to the chat API!"

"""
Create a new chat conversation
POST /api/chat/new

Request body:
{
    "user_id": "dev-user",    # optional, defaults to "dev-user"
    "title": "My Chat"        # optional, defaults to timestamp-based title
}

Response:
{
    "conversation_id": "507f1f77bcf86cd799439011",
    "title": "My Chat",
    "created_at": "2024-02-20T15:30:00.000Z",
    "user_id": "dev-user"
}

Example curl:
curl -X POST http://localhost:5000/api/chat/new \
    -H "Content-Type: application/json" \
    -d '{"title": "My Chat", "user_id": "dev-user"}'
"""
@app.route('/api/chat/new', methods=['POST'])
def create_new_chat():
    try:
        request_params = CreateNewChatRequest(**request.json or {})
        default_title = f"New Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        result = message_controller.create_new_chat(
            request_params.user_id, 
            request_params.title or default_title
        )
        return jsonify(result), 200
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""
Send a message to the chatbot
POST /api/chat/send

Request body:
{
    "query": "Hello, how are you?",
    "conversation_id": "507f1f77bcf86cd799439011",  # optional
    "user_id": "dev-user"                           # optional
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
Get all conversations for a user
GET /api/conversations?user_id=dev_user

Query parameters:
- user_id: string (optional, defaults to "dev-user")

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
        user_id = request.args.get('user_id', 'dev-user')
        conversations = message_controller.message_service.get_conversations(user_id)
        
        formatted_conversations = [
            ConversationResponse(
                id=conv['conversation_id'],
                title=conv['title'],
                created_at=conv['created_at'],
                updated_at=conv.get('updated_at')
            ).model_dump()
            for conv in conversations
        ]
        
        return jsonify({'conversations': formatted_conversations}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""
Get all messages from a conversation
GET /api/conversations/<conversation_id>/messages?user_id=dev_user

Path parameters:
- conversation_id: string (required)

Query parameters:
- user_id: string (optional, defaults to "dev-user")

Response:
{
    "messages": [
        {
            "role": "user",
            "content": "Hello, how are you?",
            "timestamp": "2024-02-20T15:30:00.000Z"
        },
        {
            "role": "assistant",
            "content": "Hello! I'm doing well, thank you for asking. How can I help you today?",
            "timestamp": "2024-02-20T15:30:01.000Z"
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
        user_id = request.args.get('user_id', 'dev-user')
        messages = message_controller.message_service.get_conversation_history(conversation_id)
        
        formatted_messages = [
            MessageResponse(
                role=m['role'],
                content=m['content'],
                timestamp=msg['timestamp']
            ).model_dump()
            for msg in messages
            for m in msg['messages']
        ]
        
        return jsonify({'messages': formatted_messages}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG)