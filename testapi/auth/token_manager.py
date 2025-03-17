import secrets
from datetime import datetime, timedelta
from db_connections import DatabaseConnections

class TokenManager:
    def __init__(self):
        db = DatabaseConnections().get_mongodb()
        self.tokens_collection = db.tokens

    def generate_token(self, user_id, expires_in=86400):
        """Generate a new token for a user and store in MongoDB"""
        token = secrets.token_urlsafe(32)
        expiry = datetime.now() + timedelta(seconds=expires_in)
        
        # Store token in MongoDB
        self.tokens_collection.insert_one({
            'token': token,
            'user_id': user_id,
            'expiry': expiry,
            'created_at': datetime.now()
        })
        
        return token, expiry

    def validate_token(self, token):
        """Validate token from MongoDB and return user_id if valid"""
        token_doc = self.tokens_collection.find_one({'token': token})
        if not token_doc:
            return None
            
        if datetime.now() > token_doc['expiry']:
            self.tokens_collection.delete_one({'token': token})
            return None
            
        return token_doc['user_id']

    def revoke_token(self, token):
        """Revoke token by removing from MongoDB"""
        result = self.tokens_collection.delete_one({'token': token})
        return result.deleted_count > 0

    def cleanup_expired_tokens(self):
        """Remove all expired tokens"""
        self.tokens_collection.delete_many({
            'expiry': {'$lt': datetime.now()}
        })
