import json
from random import random

from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Lade Umgebungsvariablen
load_dotenv()

app = Flask(__name__)
CORS(app)  # Erlaubt Cross-Origin-Anfragen für React

API_URL = os.getenv("DIFY_API_URL", "http://localhost/v1")
API_KEY = os.getenv("DIFY_API_KEY", "app-Ea0MYTfWhjxI4cf7lSlI3ErD")

dify_url = "http://localhost/v1"
dify_key = "app-Ea0MYTfWhjxI4cf7lSlI3ErD"

HEADERS = {
    'Authorization': f'Bearer {dify_key}',
    'Content-Type': 'application/json'
}

conversation_local = "conversations.json"

"""
Gets the message from the user as <path> and returns it
"""
@app.route('/api/<message>', methods=['GET','POST'])
def testMessage(message):
    return message

"""
Gets the message from the user as args and returns it
"""
@app.route('/api')
def hello_world():
    page_content = request.args.get("message") # .../api?message=Hello -> Hello, World, Hello
    return 'Hello, World, ' + page_content

def load_conversation():
    if os.path.exists(conversation_local):
        try:
            with open(conversation_local, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    return data
        except json.JSONDecodeError:
            print("Fehler: Die Datei 'conversations.json' ist beschädigt und wird zurückgesetzt.")
    return {}

def save_conversation(conversation_id, reply):
    data = {}

    if os.path.exists(conversation_local):
        with open(conversation_local, "w", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print("Fehler: Die Datei 'conversations.json' ist beschädigt und wird zurückgesetzt.")
                data = {}

    if conversation_id not in data:
        data[conversation_id] = []

    # Füge die Antwort zur Konversation hinzu
    data[conversation_id].append({"reply": reply})

    with open(conversation_local, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# TODO: Stellt euch die Frage: Für welche Interaktionen braucht der Nutzer Daten vom Backend? Dann wisst ihr welche Endpoints wir brauchen.

@app.route('/api/postTest', methods=['GET','POST'])
def post_test():
    data = request.get_json()
    user_entry = data["user_entry"]

    return jsonify({"message": f"Hello World, user says: {user_entry}"})

"""
Gets all conversation (ID, Title) to Display on the Sidebar
"""

"""
@app.route('/api/getConversations', method=['GET', 'POST'])
def getConversations():
    return None
"""

"""
Gets a single Chat (history) with a conversation_id 
"""

"""
@app.route('api/getChat', method=['GET', 'POST'])
def getChat():
    return None
"""





# sample call: /appi/send-message?query=Hello, Dify&conversation_id=123
"""
SAMPLE REQUEST DATA
{
    "inputs": {},
    "query": "What are the specs of the iPhone 13 Pro Max?",
    "response_mode": "streaming",
    "conversation_id": "",
    "user": "abc-123",
    "files": [
      {
        "type": "image",
        "transfer_method": "remote_url",
        "url": "https://cloud.dify.ai/logo/logo-site.png"
      }
    ]
}
"""

#TODO: If conversation_id == Null, make new chat
#TODO: Return entire chat history with every http response?
"""
Sends a message to the AI-chat, returns the AI's response, Adds the messages to chat history
"""
@app.route('/api/send-message', methods=['GET','POST'])
def send_message():
    user_query = request.args.get("query")
    conversation_id = request.args.get("conversation_id")
    # Request BODY
    """
    data = request.json
    user_query = data.get("query")
    conversation_id = data.get("conversation_id")
    """


    print("Sending message to dify", user_query)
    if not user_query:
        return jsonify({"error": "Query ist erforderlich"}), 400

    payload = {
        "inputs": {},
        "query": user_query,
        "response_mode": "blocking",
        "conversation_id": "",
        "user": "user-123"
    }


    response = requests.post(f"{dify_url}/chat-messages", headers=HEADERS, json=payload)
    if response.status_code == 200:
        response_data = response.json()
        new_conversation_id = response_data.get("conversation_id")
        reply = response_data.get("answer", "Keine Antwort erhalten.")

        # TODO: Load conversation into database
        # conversations = load_conversation()
        save_conversation(new_conversation_id, reply)
        return new_conversation_id, reply
    else:
        return jsonify({"error": f"Fehler bei der Kommunikation mit Dify, {response.status_code}"}), response.status_code

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "running"})

# BROKE AF
@app.route('/api/test', methods=['POST'])
def test():
    data = request.get_json()
    user_entry = data["user_entry"]

    url = "http://localhost:5000/api"

    payload = {
        "user_entry": user_entry
    }
    response = requests.post(f"{url}/test", headers=HEADERS, json=payload)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code != 200:
        return jsonify({
            "error": "Fehler bei der Kommunikation mit der externen API",
            "status_code": response.status_code,
            "response_text": response.text
        }), response.status_code
    try:
        answer = response.json()
    except ValueError:
        return jsonify({"error": "Fehler beim Parsen der API-Antwort."}), 500

    return jsonify({"message": f"Hello World, user says: {answer}"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
