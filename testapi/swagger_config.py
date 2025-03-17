from flask_restx import Api, fields

def create_swagger_api():
    api = Api(
        title='SZI Chatbot API',
        version='1.0',
        description='API for interacting with the SZI Chatbot',
        doc='/api/docs'
    )

    # Define models for request/response documentation
    user_create_model = api.model('UserCreate', {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password'),
        'display_name': fields.String(description='Display name')
    })

    login_model = api.model('Login', {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password')
    })

    message_model = api.model('Message', {
        'query': fields.String(required=True, description='Message text'),
        'conversation_id': fields.String(required=False, description='Conversation ID')
    })

    conversation_model = api.model('Conversation', {
        'id': fields.String(description='Conversation ID'),
        'title': fields.String(description='Conversation title'),
        'created_at': fields.DateTime(description='Creation timestamp'),
        'updated_at': fields.DateTime(description='Last update timestamp')
    })

    chat_message_model = api.model('ChatMessage', {
        'role': fields.String(description='Message role (user/assistant)'),
        'content': fields.String(description='Message content'),
        'created_at': fields.DateTime(description='Message timestamp')
    })

    # Add models to the API
    api.models[user_create_model.name] = user_create_model
    api.models[login_model.name] = login_model
    api.models[message_model.name] = message_model
    api.models[conversation_model.name] = conversation_model
    api.models[chat_message_model.name] = chat_message_model

    return api
