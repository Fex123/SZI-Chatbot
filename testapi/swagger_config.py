from flask_restx import Api, fields

def create_swagger_api():
    api = Api(
        title='SZI Chatbot API',
        version='1.0',
        description='RESTful API for the SZI Chatbot',
        doc='/api/docs',
        authorizations={
            'Bearer Auth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'Add a Bearer token with the format "Bearer {token}"'
            }
        },
        security='Bearer Auth'
    )

    # Request Models
    api.model('UserCreate', {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password'),
        'display_name': fields.String(description='Display name')
    })

    api.model('Login', {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password')
    })

    api.model('SendMessage', {
        'query': fields.String(required=True, description='Message text'),
        'conversation_id': fields.String(description='Conversation ID (optional)')
    })

    # Response Models
    api.model('User', {
        'user_id': fields.String(description='User ID'),
        'username': fields.String(description='Username'),
        'display_name': fields.String(description='Display name')
    })

    api.model('LoginResponse', {
        'token': fields.String(description='JWT token'),
        'expires': fields.DateTime(description='Token expiration date'),
        'user': fields.Nested(api.model('User'))
    })

    api.model('Message', {
        'role': fields.String(description='Message role (user/assistant)'),
        'content': fields.String(description='Message content'),
        'created_at': fields.DateTime(description='Creation timestamp')
    })

    api.model('Conversation', {
        'id': fields.String(description='Conversation ID'),
        'title': fields.String(description='Conversation title'),
        'created_at': fields.DateTime(description='Creation timestamp'),
        'updated_at': fields.DateTime(description='Last update timestamp')
    })

    return api
