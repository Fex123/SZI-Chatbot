from services.user_service import UserService  # Updated import

"""
AuthController class
Responsible for handling user authentication and token verification
"""
class AuthController:
    def __init__(self):
        self.user_service = UserService()

    def verify_auth_token(self, token, token_manager):
        """Verify token and return user if valid"""
        if not token:
            return None
            
        user_id = token_manager.validate_token(token)
        if not user_id:
            return None
            
        return self.user_service.get_user(user_id)

    def get_user_from_request(self, request, token_manager):
        """Extract and verify token from request header"""
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header.split(' ')[1]
        return self.verify_auth_token(token, token_manager)
