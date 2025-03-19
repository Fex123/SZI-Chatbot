import requests
from datetime import datetime, timedelta
from db_connections import DatabaseConnections
from config import Config

"""
TopQueriesService class
Responsible for handling operations related to top queries analysis
"""
class TopQueriesService:
    def __init__(self, update_interval_minutes):
        db = DatabaseConnections().get_mongodb()
        self.messages_collection = db.messages
        self.top_queries_collection = db.top_queries
        self.update_interval = timedelta(days=update_interval_minutes)
        self.default_queries = [
            "Wieviele Seiten braucht meine 2. Projektarbeit",
            "Welche Kapitel muss meine Projektarbeit enthalten",
            "Wie viele Credits bekomme ich für meine Bachelorarbeit?"
        ]

    def get_recent_conversations(self, limit=100):
        """Get recent messages from all users"""
        try:
            pipeline = [
                {"$unwind": "$messages"},
                {"$sort": {"messages.timestamp": -1}},
                {"$limit": limit},
                {"$group": {
                    "_id": None,
                    "conversations": {
                        "$push": {
                            "content": "$messages.content",
                            "role": "$messages.role"
                        }
                    }
                }}
            ]
            
            result = list(self.messages_collection.aggregate(pipeline))
            if not result:
                print("No conversations found in database")
                return []
                
            return result[0]["conversations"]
            
        except Exception as e:
            print(f"Error fetching conversations: {e}")
            return []

    def analyze_conversations_with_dify(self, conversations):
        """Send conversations to Dify for analysis"""
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in conversations
        ])

        prompt = (
            "Based on these conversation snippets, identify the top 3 most common "
            "or important topics/queries. Format your response as a JSON array of "
            "exactly 3 strings. Example: ['topic1', 'topic2', 'topic3']. Here are "
            f"the conversations:\n\n{conversation_text}"
        )

        payload = {
            "inputs": {},
            "query": prompt,
            "response_mode": "blocking",
            "user": "system"
        }

        response = requests.post(
            f"{Config.DIFY_URL}/chat-messages",
            headers=Config.DIFY_HEADERS,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(f"Dify API error: {response.status_code}")

        return response.json().get("answer", "[]")

    def save_top_queries(self, queries):
        """Save analyzed queries to database"""
        doc = {
            "queries": queries,
            "created_at": datetime.now()
        }
        self.top_queries_collection.insert_one(doc)

    def get_latest_top_queries(self):
        """Get most recent top queries or defaults if none exist"""
        result = self.top_queries_collection.find_one(
            sort=[("created_at", -1)]
        )
        return result["queries"] if result else self.default_queries

    def should_update_queries(self):
        """Check if queries should be updated based on configured interval"""
        latest = self.top_queries_collection.find_one(
            sort=[("created_at", -1)]
        )
        if not latest:
            return True

        next_update = latest["created_at"] + self.update_interval
        return datetime.now() >= next_update

    def update_top_queries(self):
        """Main method to update top queries with empty check"""
        if not self.should_update_queries():
            return False

        conversations = self.get_recent_conversations()
        if not conversations:
            # Save default queries if no conversations exist
            self.save_top_queries(self.default_queries)
            return True

        analyzed_queries = self.analyze_conversations_with_dify(conversations)
        self.save_top_queries(analyzed_queries)
        return True
