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
