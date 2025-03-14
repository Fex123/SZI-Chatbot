import secrets
from datetime import datetime, timedelta

class TokenManager:
    def __init__(self):
        self.tokens = {}  # Store tokens in memory: {token: (user_id, expiry)}

    def generate_token(self, user_id, expires_in=3600):
        """Generate a new token for a user"""
        token = secrets.token_urlsafe(32)
        expiry = datetime.now() + timedelta(seconds=expires_in)
        self.tokens[token] = (user_id, expiry)
        return token, expiry

    def validate_token(self, token):
        """Validate a token and return user_id if valid"""
        if token not in self.tokens:
            return None
        user_id, expiry = self.tokens[token]
        if datetime.now() > expiry:
            self.tokens.pop(token)
            return None
        return user_id

    def revoke_token(self, token):
        """Revoke a token"""
        if token in self.tokens:
            self.tokens.pop(token)
            return True
        return False
