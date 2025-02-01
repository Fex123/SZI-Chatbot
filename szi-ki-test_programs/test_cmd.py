import requests
import json
import os

API_URL = 'http://localhost/v1'
API_KEY = 'app-v2p2HW8CIqw5slRMfjWAkawb'

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

CONVERSATION_FILE = "conversations.json"

def load_conversations():
    """Lädt gespeicherte Konversationen und stellt sicher, dass es ein Dictionary ist."""
    if os.path.exists(CONVERSATION_FILE):
        try:
            with open(CONVERSATION_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, dict):  # Sicherstellen, dass es ein Dictionary ist
                    return data
        except json.JSONDecodeError:
            print("⚠️ Fehler: Die Datei 'conversations.json' ist beschädigt und wird zurückgesetzt.")

    return {}  # Falls die Datei nicht existiert oder fehlerhaft ist, ein leeres Dictionary zurückgeben

def save_conversations(conversations):
    """Speichert Konversationen in einer JSON-Datei."""
    with open(CONVERSATION_FILE, "w", encoding="utf-8") as file:
        json.dump(conversations, file, ensure_ascii=False, indent=4)

def send_message(conversation_id, user_query):
    """Sendet eine Nachricht an Dify und speichert den Verlauf lokal."""
    data = {
        "inputs": {},
        "query": user_query,
        "response_mode": "blocking",
        "conversation_id": conversation_id,
        "user": "user-123"
    }

    response = requests.post(f"{API_URL}/chat-messages", headers=HEADERS, json=data)

    if response.status_code == 200:
        response_data = response.json()
        new_conversation_id = response_data.get("conversation_id")
        assistant_reply = response_data.get("answer", "Keine Antwort erhalten.")

        # Lade aktuelle Konversationen
        conversations = load_conversations()

        # Falls die Datei fälschlicherweise eine Liste war, korrigieren
        if not isinstance(conversations, dict):
            print("⚠️ Fehler: 'conversations.json' hatte falsches Format und wurde zurückgesetzt.")
            conversations = {}

        # Falls die Konversation noch nicht existiert, erstelle sie
        if new_conversation_id not in conversations:
            conversations[new_conversation_id] = {"title": f"Chat {len(conversations) + 1}", "messages": []}

        # Speichere Nachricht im Verlauf
        conversations[new_conversation_id]["messages"].append({"role": "user", "content": user_query})
        conversations[new_conversation_id]["messages"].append({"role": "assistant", "content": assistant_reply})

        save_conversations(conversations)

        return new_conversation_id, assistant_reply
    else:
        print(f"Fehler: {response.status_code} - {response.text}")
        return conversation_id, None

def show_conversation_history():
    """Zeigt eine Liste aller Konversationen und erlaubt die Auswahl einer zum Anzeigen."""
    conversations = load_conversations()

    if not conversations:
        print("⚠️ Keine gespeicherten Konversationen gefunden.")
        return

    print("\n📜 Verfügbare Konversationen:")
    conversation_list = list(conversations.items())

    for index, (convo_id, convo_data) in enumerate(conversation_list):
        print(f"{index + 1}. {convo_data['title']} (ID: {convo_id})")

    while True:
        try:
            selection = int(input("\nWählen Sie eine Konversation zum Anzeigen (Nummer eingeben, 0 zum Abbrechen): "))
            if selection == 0:
                return
            if 1 <= selection <= len(conversation_list):
                convo_id, convo_data = conversation_list[selection - 1]
                print(f"\n📜 Chatverlauf für: {convo_data['title']}\n")
                for message in convo_data["messages"]:
                    role = "👤 Sie" if message["role"] == "user" else "🤖 Assistent"
                    print(f"{role}: {message['content']}")

                input("\n🔙 Drücken Sie ENTER, um zum Chat zurückzukehren...")
                return
            else:
                print("⚠️ Ungültige Auswahl. Bitte eine gültige Nummer eingeben.")
        except ValueError:
            print("⚠️ Bitte eine Nummer eingeben.")

def main():
    """Einfache Konsolenanwendung für den Dify-Chat."""
    conversation_id = None

    print("📢 Geben Sie Ihre Nachricht ein.")
    print("💡 Befehle: 'neue konversation' | 'verlauf' | 'beenden'")

    while True:
        user_input = input("\nSie: ").strip().lower()

        if user_input == "neue konversation":
            conversation_id = None
            print("🔄 Neue Konversation gestartet.")
            continue
        elif user_input == "verlauf":
            show_conversation_history()
            continue
        elif user_input == "beenden":
            print("👋 Programm beendet.")
            break

        conversation_id, assistant_reply = send_message(conversation_id, user_input)

        if assistant_reply:
            print(f"🤖 Assistent: {assistant_reply}")
        else:
            print("⚠️ Keine Antwort erhalten. Versuchen Sie es erneut.")

if __name__ == "__main__":
    main()
