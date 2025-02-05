from flask import Flask, request, jsonify
from db_connections import DatabaseConnections
from controllers.message_controller import MessageController
from config import Config
from db.user_service import UserService

app = Flask(__name__)
db_conn = DatabaseConnections()
message_controller = MessageController()
user_service = UserService()

@app.before_first_request
def initialize_connections():
    db_conn.connect_all()

@app.route('/')
def home():
    return "Welcome to the chat API! Use /api/chat/send to send a message. (Post request with 'query' in JSON body)"

@app.route('/api/chat/send', methods=['POST'])
def send_message():
    try:
        data = request.json
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400

        result = message_controller.send_message_to_dify(
            query=data['query'],
            conversation_id=data.get('conversation_id'),
            user_id=data.get('user_id', 'dev-user')
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/history/<conversation_id>', methods=['GET'])
def get_chat_history(conversation_id):
    try:
        messages = message_controller.message_service.get_conversation_history(conversation_id)
        return jsonify({'messages': list(messages)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/<user_id>/conversations', methods=['GET'])
def get_user_conversations(user_id):
    try:
        user = user_service.get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'conversations': user.get('conversations', [])}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG)