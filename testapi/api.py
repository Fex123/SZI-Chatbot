from flask import Flask, request, jsonify
from flask_httpauth import HTTPTokenAuth
from auth.token_manager import TokenManager
from pydantic import BaseModel, ValidationError
from flask_cors import CORS
from typing import Optional
from db_connections import DatabaseConnections
from config import Config
from datetime import datetime
from utils.bcrypt_singleton import BcryptSingleton
from controllers.auth_controller import AuthController
from controllers.message_controller import MessageController
from services.validation_service import ValidationService
from services.user_service import UserService
from services.message_service import MessageService

app = Flask(__name__)
CORS(app)

# Initialize Bcrypt singleton with app FIRST
bcrypt_singleton = BcryptSingleton.get_instance()
bcrypt_singleton.init_bcrypt(app)

# Initialize auth components AFTER bcrypt is ready
auth = HTTPTokenAuth(scheme='Bearer')
token_manager = TokenManager()

# Initialize database connection
db_conn = DatabaseConnections()
db_conn.connect_all()

# Initialize rest of services AFTER bcrypt and database are ready
user_service = UserService()
message_controller = MessageController()
auth_controller = AuthController()

"""
    Request Body Classes:
"""
class SendMessageRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None
    # Remove default user_id as it will come from authentication

class UserCreateRequest(BaseModel):
    username: str
    password: str
    display_name: Optional[str] = None

    model_config = ValidationService.get_model_config()
    validate_username = ValidationService.validate_username
    validate_password = ValidationService.validate_password

class LoginRequest(BaseModel):
    username: str
    password: str

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

@auth.verify_token
def verify_token(token):
    return auth_controller.verify_auth_token(token, token_manager)

"""
Root endpoint
GET /
Returns a welcome message
"""
@app.route('/')
def home():
    return "Welcome to the chat API!"

"""
Create a new user
POST /api/auth/register

Request body:
{
    "username": "john_doe",
    "password": "secure_password",
    "display_name": "John Doe"
}
"""
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = UserCreateRequest(**request.json)
        user = user_service.create_user(
            username=data.username,
            password=data.password,
            display_name=data.display_name
        )
        return jsonify({
            'message': 'User created successfully',
            'user_id': user['user_id']
        }), 201
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""
Login user
POST /api/auth/login

Request body:
{
    "username": "john_doe",
    "password": "secure_password"
}
"""
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = LoginRequest(**request.json)
        user = user_service.authenticate_user(data.username, data.password)
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
            
        token, expiry = token_manager.generate_token(user['user_id'])
        return jsonify({
            'token': token,
            'expires': expiry.isoformat(),
            'user': {
                'user_id': user['user_id'],
                'username': user['username'],
                'display_name': user['display_name']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""
Logout user
POST /api/auth/logout
"""
@app.route('/api/auth/logout', methods=['POST'])
@auth.login_required
def logout():
    token = request.headers.get('Authorization').split(' ')[1]
    token_manager.revoke_token(token)
    return jsonify({'message': 'Logged out successfully'}), 200

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
@auth.login_required
def send_message():
    try:
        # Get authenticated user
        current_user = auth_controller.get_user_from_request(request, token_manager)
        if not current_user:
            return jsonify({'error': 'Authentication failed'}), 401

        data = request.json
        if 'conversation_id' in data and not data['conversation_id']:
            data['conversation_id'] = None
            
        request_params = SendMessageRequest(**data)
        request_params.user_id = current_user['user_id']  # Use authenticated user's ID

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
@auth.login_required
def get_user_conversations():
    try:
        current_user = auth_controller.get_user_from_request(request, token_manager)
        if not current_user:
            return jsonify({'error': 'Authentication failed'}), 401

        conversations = message_controller.message_service.get_formatted_conversations(
            current_user['user_id']
        )
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
@auth.login_required
def get_conversation_messages(conversation_id):
    try:
        current_user = auth_controller.get_user_from_request(request, token_manager)
        if not current_user:
            return jsonify({'error': 'Authentication failed'}), 401

        messages = message_controller.message_service.get_conversation_history(
            conversation_id,
            user_id=current_user['user_id']  # Add user_id for ownership validation
        )
        
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

# Use similar pattern for other endpoints that need user context
@app.route('/api/auth/profile', methods=['GET'])
@auth.login_required
def get_profile():
    try:
        current_user = auth_controller.get_user_from_request(request, token_manager)
        if not current_user:
            return jsonify({'error': 'Authentication failed'}), 401

        return jsonify({
            'user_id': current_user['user_id'],
            'username': current_user['username'],
            'display_name': current_user['display_name'],
            'created_at': current_user['created_at']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host= "0.0.0.0", port= 3104, debug=Config.DEBUG)