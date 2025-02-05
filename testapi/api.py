from flask import Flask, request, jsonify
from db_connections import DatabaseConnections
from config import Config

app = Flask(__name__)
db_conn = DatabaseConnections()

@app.before_first_request
def initialize_connections():
    db_conn.connect_all()

@app.teardown_appcontext
def cleanup(exception=None):
    db_conn.close_all()

'''
API Endpoints
'''
@app.route('/')
def index():
    return 'Hello World!'

@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Create user in MongoDB
    users_collection = db_conn.get_mongodb().users
    result = users_collection.insert_one({
        'username': data['username'],
        'email': data['email']
    })
    
    return jsonify({
        'message': 'User created successfully',
        'id': str(result.inserted_id)
    }), 201

if __name__ == '__main__':
    app.run(debug=Config.DEBUG)