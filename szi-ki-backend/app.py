from random import random

from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Lade Umgebungsvariablen
load_dotenv()

API_URL = os.getenv("DIFY_API_URL", "http://localhost/v1")
API_KEY = os.getenv("DIFY_API_KEY", "app-Ea0MYTfWhjxI4cf7lSlI3ErD")

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

app = Flask(__name__)
CORS(app)  # Erlaubt Cross-Origin-Anfragen für React

# TODO: Stellt euch die Frage: Für welche Interaktionen braucht der Nutzer Daten vom Backend? Dann wisst ihr welche Endpoints wir brauchen.


"""
Gets all conversation (ID, Title) to Display on the Sidebar
"""
@app.route('/api/getConversations', method=['POST'])
def getConversations():
    pass

"""
Gets a single Chat (history) with a conversation_id 
"""
@app.route('api/getChat', method=['POST'])
def getChat():
    pass

#TODO: If conversation_id == Null, make new chat
#TODO: Return entire chat history with every http response?
"""
Sends a message to the AI-chat, returns the AI's response, Adds the messages to chat history
"""
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_query = data.get("query")
    conversation_id = data.get("conversation_id", None)

    print("Hello World")
    if not user_query:
        return jsonify({"error": "Query ist erforderlich"}), 400

    payload = {
        "inputs": {},
        "query": user_query,
        "response_mode": "blocking",
        "conversation_id": conversation_id,
        "user": "user-123"
    }

    response = requests.post(f"{API_URL}/chat-messages", headers=HEADERS, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        return jsonify({
            "conversation_id": response_data.get("conversation_id"),
            "answer": response_data.get("answer", "Keine Antwort erhalten.")
        })
    else:
        return jsonify({"error": "Fehler bei der Kommunikation mit Dify"}), response.status_code


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "running"})

@app.route('/api/test', methods=['POST'])
def test():
    return print("Hello World")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
