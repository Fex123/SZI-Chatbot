import requests
from datetime import datetime, timedelta
from db_connections import DatabaseConnections
from config import Config
import json
import threading
import re

"""
TopQueriesService class
Responsible for handling operations related to top queries analysis
"""
class TopQueriesService:
    def __init__(self, update_interval_minutes):
        db = DatabaseConnections().get_mongodb()
        self.messages_collection = db.messages
        self.top_queries_collection = db.top_queries
        self.update_interval = timedelta(minutes=update_interval_minutes)
        self.default_queries = [
            "Wieviele Seiten braucht meine 2. Projektarbeit",
            "Welche Kapitel muss meine Projektarbeit enthalten",
            "Wie viele Credits bekomme ich für meine Bachelorarbeit?"
        ]
        self.is_updating = False

    def get_recent_conversations(self, limit=100):
        """Get recent messages from all users"""
        try:
            pipeline = [
                {"$match": {"messages": {"$exists": True, "$ne": []}}},
                {"$unwind": "$messages"},
                {"$match": {"messages.role": "user"}},
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
        if not conversations:
            print("No conversations to analyze")
            return self.default_queries
        
        # Format conversations for analysis
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in conversations if 'content' in msg and msg['content']
        ])

        if not conversation_text.strip():
            print("Empty conversation text")
            return self.default_queries

        # Prepare prompt for Dify
        prompt = (
            "Based on these conversation snippets, identify the top 3 most common "
            "or important topics/queries. Return ONLY a JSON array of exactly 3 strings, "
            "with no explanation or other text. Example response: [\"topic1\", \"topic2\", \"topic3\"]"
            f"\n\nThe conversations:\n\n{conversation_text}"
        )

        payload = {
            "inputs": {},
            "query": prompt,
            "response_mode": "blocking",
            "user": "system"
        }

        try:
            print("Sending request to Dify for conversation analysis...")
            response = requests.post(
                f"{Config.DIFY_URL}/chat-messages",
                headers=Config.DIFY_HEADERS,
                json=payload,
                timeout=30
            )

            if response.status_code != 200:
                print(f"Dify API error: {response.status_code}")
                return self.default_queries

            answer = response.json().get("answer", "[]")
            print(f"Raw response from Dify: {answer}")
            
            # Extract JSON array from the text using regex
            json_array_pattern = r'\[.*?\]'
            json_matches = re.search(json_array_pattern, answer, re.DOTALL)
            
            if json_matches:
                json_str = json_matches.group(0)
                print(f"Extracted JSON string: {json_str}")
                
                # Try to parse the extracted JSON
                try:
                    queries = json.loads(json_str)
                    if isinstance(queries, list) and len(queries) > 0:
                        print(f"Successfully parsed queries: {queries}")
                        return queries[:3]  # Ensure we return at most 3 queries
                    else:
                        print(f"Invalid parsed format (not a non-empty list): {queries}")
                except json.JSONDecodeError as e:
                    print(f"JSON decode error after extraction: {e}")
            else:
                print("Could not extract JSON array from response")
            
            # Fallback: Try direct JSON parsing in case it's a clean JSON string
            try:
                queries = json.loads(answer)
                if isinstance(queries, list) and len(queries) > 0:
                    print(f"Successfully parsed direct JSON: {queries}")
                    return queries[:3]
                else:
                    print(f"Invalid direct parse format: {queries}")
            except json.JSONDecodeError as e:
                print(f"Direct JSON decode error: {e}")
            
            # Second fallback: Manual extraction of strings
            if '"' in answer or "'" in answer:
                quoted_strings = re.findall(r'["\'](.*?)["\']', answer)
                if quoted_strings and len(quoted_strings) >= 3:
                    print(f"Extracted quoted strings: {quoted_strings[:3]}")
                    return quoted_strings[:3]
                    
            return self.default_queries
                
        except requests.exceptions.Timeout:
            print("Dify request timed out")
            return self.default_queries
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return self.default_queries
        except Exception as e:
            print(f"Unexpected error in analyze_conversations_with_dify: {e}")
            return self.default_queries

    def save_top_queries(self, queries):
        """Save analyzed queries to database"""
        try:
            doc = {
                "queries": queries,
                "created_at": datetime.now()
            }
            self.top_queries_collection.insert_one(doc)
            print(f"Saved top queries: {queries}")
            return True
        except Exception as e:
            print(f"Error saving top queries: {e}")
            return False

    def get_latest_top_queries(self):
        """Get most recent top queries or defaults if none exist"""
        try:
            result = self.top_queries_collection.find_one(
                sort=[("created_at", -1)]
            )
            if result and "queries" in result:
                return result["queries"]
            return self.default_queries
        except Exception as e:
            print(f"Error getting latest top queries: {e}")
            return self.default_queries

    def should_update_queries(self):
        """Check if queries should be updated based on configured interval"""
        try:
            latest = self.top_queries_collection.find_one(
                sort=[("created_at", -1)]
            )
            if not latest:
                return True

            next_update = latest["created_at"] + self.update_interval
            return datetime.now() >= next_update
        except Exception as e:
            print(f"Error checking if queries should be updated: {e}")
            return False

    def _async_update_queries(self, conversations):
        """Background task to update queries"""
        try:
            self.is_updating = True
            analyzed_queries = self.analyze_conversations_with_dify(conversations)
            self.save_top_queries(analyzed_queries)
        except Exception as e:
            print(f"Error in async update: {e}")
        finally:
            self.is_updating = False

    def update_top_queries(self):
        """Main method to update top queries with empty check"""
        try:
            # Skip if already updating
            if self.is_updating:
                print("Update already in progress, skipping")
                return False
                
            # Skip if update not needed
            if not self.should_update_queries():
                return False

            conversations = self.get_recent_conversations()
            if not conversations:
                # Save default queries if no conversations exist
                self.save_top_queries(self.default_queries)
                return True

            # Start background thread to update queries
            thread = threading.Thread(
                target=self._async_update_queries,
                args=(conversations,)
            )
            thread.daemon = True
            thread.start()
            
            print("Started background update of top queries")
            return True
            
        except Exception as e:
            print(f"Error initiating top queries update: {e}")
            return False
