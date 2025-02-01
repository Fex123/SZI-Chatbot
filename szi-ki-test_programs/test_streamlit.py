import streamlit as st
import requests
import json
import os
import time

# Page configuration
st.set_page_config(
    page_title="SZI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Dify API Configuration
API_URL = 'http://localhost/v1'
API_KEY = 'app-v2p2HW8CIqw5slRMfjWAkawb'
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
CONVERSATION_FILE = "conversations.json"

# Custom Styling
primary_color = "#FF4B4B"
secondary_color = "#FFE5E5"
logo_width = 270  # Adjusted logo size

custom_css = f"""
<style>
:root {{
    --primary: {primary_color};
    --secondary: {secondary_color};
}}

/* Logo styling */
.logo-container {{
    text-align: center;
    margin: 1.5rem 0 3rem 0;
    padding: 15px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}}

.logo-container:hover {{
    transform: scale(1.02);
}}

/* Sidebar title styling */
.sidebar-title {{
    font-family: 'Arial Rounded MT Bold', sans-serif;
    text-align: center;
    font-size: 2rem !important;
    margin: 1rem 0 2.5rem 0;
    padding: 0.8rem;
    background: linear-gradient(45deg, {primary_color}, #FF3333);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    position: relative;
    letter-spacing: -0.5px;
}}

.sidebar-title::before {{
    content: '';
    position: absolute;
    bottom: -12px;
    left: 50%;
    transform: translateX(-50%);
    width: 70%;
    height: 3px;
    background: linear-gradient(90deg, {primary_color}, #FF3333);
    border-radius: 2px;
}}

/* Chat message styling */
[data-testid="stChatMessage"] {{
    padding: 18px;
    border-radius: 15px;
    margin: 15px 0;
    box-shadow: 0 3px 6px rgba(0,0,0,0.05);
}}

[data-testid="stChatMessage"][aria-label="user"] {{
    background-color: var(--secondary);
    border-left: 5px solid var(--primary);
}}

[data-testid="stChatMessage"][aria-label="assistant"] {{
    background-color: #F8F9FA;
    border-left: 5px solid #666666;
}}

/* Button styling */
.stSidebar .stButton>button {{
    background-color: transparent !important;
    color: var(--primary) !important;
    border: 2px solid var(--primary) !important;
    width: 100%;
    text-align: left;
    padding: 12px 20px !important;
    border-radius: 8px !important;
    transition: all 0.2s ease;
    margin: 8px 0 !important;
}}

.stSidebar .stButton>button:hover {{
    background-color: var(--secondary) !important;
    transform: translateX(5px);
}}

/* Main title styling */
.main-title {{
    font-size: 2.5rem !important;
    color: {primary_color} !important;
    border-bottom: 3px solid {primary_color};
    padding-bottom: 12px;
    margin-bottom: 2rem;
}}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)


def generate_chat_title(prompt):
    """Generate a chat title from the first 3 words of the prompt"""
    words = prompt.split()[:3]
    return " ".join(words).title() + "..."


def load_conversations():
    """Load conversations from JSON file"""
    if os.path.exists(CONVERSATION_FILE):
        try:
            with open(CONVERSATION_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            st.error("Error loading conversations, resetting file.")
            return {}
    return {}


def save_conversations(conversations):
    """Save conversations to JSON file"""
    with open(CONVERSATION_FILE, "w", encoding="utf-8") as f:
        json.dump(conversations, f, ensure_ascii=False, indent=2)


def send_message(conversation_id, user_input):
    """Send message to Dify API with auto-titling"""
    payload = {
        "inputs": {},
        "query": user_input,
        "response_mode": "blocking",
        "conversation_id": conversation_id or None,
        "user": "user-123"
    }

    try:
        response = requests.post(
            f"{API_URL}/chat-messages",
            headers=HEADERS,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        conversations = load_conversations()
        convo_id = data.get("conversation_id", str(time.time()))

        if convo_id not in conversations:
            conversations[convo_id] = {
                "title": generate_chat_title(user_input),
                "messages": []
            }

        conversations[convo_id]["messages"].extend([
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": data.get("answer", "No response")}
        ])

        save_conversations(conversations)
        st.session_state.should_rerun = True
        return convo_id, data.get("answer", "No response received")

    except requests.exceptions.HTTPError as e:
        st.error(f"API Error: {e.response.text}")
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
    return conversation_id, None


def stream_response(text):
    """Simulate streaming response with typing effect"""
    for word in text.split():
        yield word + " "
        time.sleep(0.03)


# Initialize session state
if "current_convo" not in st.session_state:
    st.session_state.current_convo = {
        "id": None,
        "messages": []
    }

if "should_rerun" not in st.session_state:
    st.session_state.should_rerun = False

# Sidebar Implementation
with st.sidebar:
    # DHBW Logo
    st.image("assets/dhbw-logo.png", width=logo_width)
    st.markdown('</div>', unsafe_allow_html=True)

    # Styled sidebar title
    st.markdown(
        '<div class="sidebar-title">SZI Chatbot</div>',
        unsafe_allow_html=True
    )

    # New chat button
    if st.button("✨ Start New Chat", use_container_width=True):
        st.session_state.current_convo = {"id": None, "messages": []}
        st.rerun()

    # Conversation history
    conversations = load_conversations()
    if conversations:
        st.subheader("Chat History", divider="red")
        for convo_id, convo in conversations.items():
            btn_label = f"{convo['title']} ({len(convo['messages']) // 2} messages)"
            if st.button(btn_label, key=convo_id, use_container_width=True):
                st.session_state.current_convo = {
                    "id": convo_id,
                    "messages": convo["messages"]
                }
                st.rerun()

# Main Chat Interface
# Dynamic title showing current chat name
conversations = load_conversations()
current_title = "New Chat"
if st.session_state.current_convo["id"] and st.session_state.current_convo["id"] in conversations:
    current_title = conversations[st.session_state.current_convo["id"]]["title"]

st.markdown(
    f'<div class="main-title">{current_title}</div>',
    unsafe_allow_html=True
)

# Display messages
for msg in st.session_state.current_convo["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    st.session_state.current_convo["messages"].append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    new_id, response = send_message(
        st.session_state.current_convo["id"],
        prompt
    )

    if response:
        st.session_state.current_convo["id"] = new_id

        with st.chat_message("assistant"):
            response_container = st.empty()
            full_response = ""

            for chunk in stream_response(response):
                full_response += chunk
                response_container.markdown(full_response + "▌")

            response_container.markdown(full_response)

        st.session_state.current_convo["messages"].append({
            "role": "assistant",
            "content": full_response.strip()
        })

# Automatic sidebar update
if st.session_state.should_rerun:
    st.session_state.should_rerun = False
    st.rerun()