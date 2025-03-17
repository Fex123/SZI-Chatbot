from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Resource, Namespace
from swagger_config import create_swagger_api
from flask_httpauth import HTTPTokenAuth
from auth.token_manager import TokenManager
from pydantic import ValidationError
from db_connections import DatabaseConnections
from config import Config
from utils.bcrypt_singleton import BcryptSingleton
from controllers.auth_controller import AuthController
from controllers.message_controller import MessageController
from models.request_models import SendMessageRequest, UserCreateRequest, LoginRequest
from models.response_models import ConversationResponse, MessageResponse, UserResponse
from services.user_service import UserService

app = Flask(__name__)
CORS(app)

# Initialize Swagger and create namespaces
api = create_swagger_api()
ns_main = Namespace('main', description='Main endpoints')
ns_auth = Namespace('auth', description='Authentication endpoints')
ns_chat = Namespace('chat', description='Chat endpoints')

api.add_namespace(ns_main, path='/')
api.add_namespace(ns_auth, path='/api/auth')
api.add_namespace(ns_chat, path='/api')

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

@auth.verify_token
def verify_token(token):
    return auth_controller.verify_auth_token(token, token_manager)

@ns_main.route('/')
class Home(Resource):
    def get(self):
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
@ns_auth.route('/register')
class Register(Resource):
    @api.expect(api.models['UserCreate'])
    def post(self):
        try:
            data = UserCreateRequest(**request.json)
            user = user_service.create_user(
                username=data.username,
                password=data.password,
                display_name=data.display_name
            )
            return {'message': 'User created successfully', 'user_id': user['user_id']}, 201
        except ValidationError as e:
            return {'error': str(e)}, 400
        except ValueError as e:
            return {'error': str(e)}, 409
        except Exception as e:
            return {'error': str(e)}, 500

"""
Login user
POST /api/auth/login

Request body:
{
    "username": "john_doe",
    "password": "secure_password"
}

Response:
{
    "token": "your_token_here",
    "expires": "2024-02-21T15:30:00.000Z",
    "user": {
        "user_id": "uuid_here",
        "username": "john_doe",
        "display_name": "John Doe"
    }
}
"""
@ns_auth.route('/login')
class Login(Resource):
    @api.expect(api.models['Login'])
    def post(self):
        try:
            data = LoginRequest(**request.json)
            user = user_service.authenticate_user(data.username, data.password)
            
            if not user:
                return {'error': 'Invalid credentials'}, 401
                
            token, expiry = token_manager.generate_token(user['user_id'])
            return {
                'token': token,
                'expires': expiry.isoformat(),
                'user': {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'display_name': user['display_name']
                }
            }
        except Exception as e:
            return {'error': str(e)}, 500

"""
Logout user
POST /api/auth/logout
"""
@ns_auth.route('/logout')
class Logout(Resource):
    @auth.login_required
    def post(self):
        token = request.headers.get('Authorization').split(' ')[1]
        token_manager.revoke_token(token)
        return {'message': 'Logged out successfully'}, 200

"""
Send a message to the chatbot
POST /api/chat/send
Authorization: Bearer <token>
Content-Type: application/json

Request body:
{
    "query": "Hello, how are you?",
    "conversation_id": "507f1f77bcf86cd799439011",  # optional
}

Response:
{
    "conversation_id": "507f1f77bcf86cd799439011",
    "response": "Hello! I'm doing well, thank you for asking. How can I help you today?"
}
"""
@ns_chat.route('/chat/send')
class SendMessage(Resource):
    @auth.login_required
    @api.expect(api.models['Message'])
    def post(self):
        try:
            current_user = auth_controller.get_user_from_request(request, token_manager)
            if not current_user:
                return {'error': 'Authentication failed'}, 401

            data = request.json
            if 'conversation_id' in data and not data['conversation_id']:
                data['conversation_id'] = None
                
            request_params = SendMessageRequest(**data)

            # Process message using service class
            conversation_id = message_controller.message_service.process_message(
                request_params.query,
                request_params.conversation_id,
                current_user['user_id']  # Use current_user directly
            )

            # Send message to Dify
            result = message_controller.send_message_to_dify(
                query=request_params.query,
                conversation_id=conversation_id,
                user_id=current_user['user_id']  # Use current_user directly
            )

            # Set default title for new conversations
            if not conversation_id and result.get('conversation_id'):
                default_title = f"{request_params.query}"
                message_controller.message_service.update_conversation_title(
                    result['conversation_id'],
                    default_title
                )

            return result, 200
        except ValidationError as e:
            return {'error': e.errors()}, 400
        except ValueError as ve:
            return {'error': str(ve)}, 404
        except Exception as e:
            return {'error': str(e)}, 500

"""
Get all conversations for a user
GET /api/conversations
Authorization: Bearer <token>

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
"""
@ns_chat.route('/conversations')
class Conversations(Resource):
    @auth.login_required
    def get(self):
        try:
            current_user = auth_controller.get_user_from_request(request, token_manager)
            if not current_user:
                return {'error': 'Authentication failed'}, 401

            conversations = message_controller.message_service.get_formatted_conversations(
                current_user['user_id']
            )
            return {
                'conversations': [ConversationResponse(**conv).model_dump() for conv in conversations]
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

"""
Get all messages from a conversation
GET /api/conversations/<conversation_id>/messages
Authorization: Bearer <token>

Path parameters:
- conversation_id: string (required)

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

"""
@ns_chat.route('/conversations/<string:conversation_id>/messages')
class ConversationMessages(Resource):
    @auth.login_required
    def get(self, conversation_id):
        try:
            current_user = auth_controller.get_user_from_request(request, token_manager)
            if not current_user:
                return {'error': 'Authentication failed'}, 401

            messages = message_controller.message_service.get_conversation_history(
                conversation_id,
                user_id=current_user['user_id']
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
            
            return {'messages': formatted_messages}, 200
        except Exception as e:
            return {'error': str(e)}, 500

# Initialize the app with the API
api.init_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3104, debug=Config.DEBUG)