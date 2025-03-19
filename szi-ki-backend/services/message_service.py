from db_connections import DatabaseConnections
from datetime import datetime
from bson import ObjectId

"""
MessageService class
Responsible for handling message operations in the database
"""
class MessageService:
    def __init__(self):
        db = DatabaseConnections().get_mongodb()
        self.messages_collection = db.messages

    def save_message(self, conversation_id, user_message, ai_response, user_id):
        """Save a new message in a conversation"""
        # Validate user_id is provided
        if not user_id:
            raise ValueError("user_id is required")
        
        now = datetime.now()
        message_pair = [
            {'role': 'user', 'content': user_message, 'timestamp': now},
            {'role': 'assistant', 'content': ai_response, 'timestamp': now}
        ]
        
        # Try to find existing conversation
        existing_conv = self.messages_collection.find_one({'conversation_id': conversation_id})
        
        if existing_conv:
            # Update existing conversation with new messages
            result = self.messages_collection.update_one(
                {'conversation_id': conversation_id},
                {
                    '$push': {'messages': {'$each': message_pair}},
                    '$set': {'updated_at': now}
                }
            )
        else:
            # Create new conversation document
            message_doc = {
                'conversation_id': conversation_id,
                'user_id': user_id,  # Add user_id to new conversations
                'messages': message_pair,
                'created_at': now, 
                'updated_at': now,
                'title': f"Chat about: {user_message[:30]}..."
            }
            result = self.messages_collection.insert_one(message_doc)
        
        return conversation_id

    def load_message(self, conversation_id):
        """Load a conversation by ID"""
        return self.messages_collection.find_one({'conversation_id': conversation_id})

    def get_conversation_history(self, conversation_id, user_id=None):
        """Get conversation history with optional user validation"""
        query = {'conversation_id': conversation_id}
        if user_id:
            query['user_id'] = user_id
            
        conversation = self.messages_collection.find_one(
            query,
            {
                'messages': 1,
                'created_at': 1,
                '_id': 0
            }
        )
        
        if not conversation and user_id:
            raise ValueError('Conversation not found or access denied')
            
        return [conversation] if conversation else []

    def _generate_unique_title(self, user_id, base_title):
        """Generate a unique title by adding a suffix number if needed"""
        title = base_title
        counter = 1
        
        while True:
            # Check if this title exists
            existing = self.messages_collection.find_one({
                'user_id': user_id,
                'title': title
            })
            
            if not existing:
                return title
                
            # Add or increment counter suffix
            title = f"{base_title} ({counter})"
            counter += 1

    def create_conversation(self, user_id, title=None):
        """Create a new conversation for a user"""
        conversation_id = str(ObjectId())
        now = datetime.now()
        
        base_title = title or "New Conversation"
        unique_title = self._generate_unique_title(user_id, base_title)
        
        conversation_doc = {
            'conversation_id': conversation_id,
            'user_id': user_id,
            'title': unique_title,
            'created_at': now,
            'updated_at': now
        }
        
        self.messages_collection.insert_one(conversation_doc)
        return conversation_doc

    def get_conversations(self, user_id):
        """
        Get all conversations for a user with their details
        Returns cursor of conversations with id, title, and timestamps
        """
        return self.messages_collection.find(
            {'user_id': user_id},
            {
                '_id': 0,
                'conversation_id': 1,
                'title': 1,
                'created_at': 1,
                'updated_at': 1
            }
        ).sort('created_at', -1)

    def update_conversation_title(self, conversation_id, new_title):
        """Update the title of a conversation"""
        return self.messages_collection.update_one(
            {'conversation_id': conversation_id},
            {'$set': {'title': new_title, 'updated_at': datetime.now()}}
        )

    def validate_conversation(self, conversation_id, user_id):
        """
        Validates if a conversation exists and belongs to the user
        Returns the conversation if valid, None if empty ID, raises Exception if invalid
        """
        if not conversation_id or conversation_id.strip() == "":
            return None
            
        conversation = self.messages_collection.find_one({
            'conversation_id': conversation_id,
            'user_id': user_id
        })
        
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found or does not belong to user {user_id}")
            
        return conversation

    def process_message(self, query, conversation_id, user_id):
        """
        Process and validate a new message
        Returns validated conversation_id or None if invalid
        """
        if not user_id:
            raise ValueError("user_id is required")
            
        if not conversation_id or conversation_id.strip() == "":
            return None
            
        try:
            conversation = self.validate_conversation(conversation_id, user_id)
            if not conversation:
                return None
        except ValueError:
            return None
            
        return conversation_id

    def get_formatted_conversations(self, user_id):
        """
        Get and format all conversations for a user
        Returns list of formatted conversation dictionaries
        """
        if not user_id:
            raise ValueError("user_id is required")
            
        conversations = self.get_conversations(user_id)
        formatted_conversations = []
        
        for conv in conversations:
            try:
                formatted_conv = {
                    'id': conv.get('conversation_id'),
                    'title': conv.get('title', 'Untitled Chat'),
                    'created_at': conv.get('created_at', datetime.now()),
                    'updated_at': conv.get('updated_at')
                }
                formatted_conversations.append(formatted_conv)
            except Exception as e:
                print(f"Error formatting conversation: {e}")
                continue
                
        return formatted_conversations
