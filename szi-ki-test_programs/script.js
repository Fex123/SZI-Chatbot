const API_URL = 'http://localhost/v1';
const API_KEY = 'app-v2p2HW8CIqw5slRMfjWAkawb';
const conversationStorageKey = 'conversations';
let currentConversationId = null;

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("send-button").addEventListener("click", sendMessageHandler);
    document.getElementById("user-input").addEventListener("keypress", (event) => {
        if (event.key === "Enter") sendMessageHandler();
    });
    document.getElementById("new-chat-button").addEventListener("click", startNewConversation);
    document.getElementById("toggle-sidebar").addEventListener("click", toggleSidebar);
    loadConversationHistory();
    adjustLayout(); // Ensure layout is correct when page loads
});

function startNewConversation() {
    currentConversationId = null;
    document.getElementById("chat-box").innerHTML = "";
    loadConversationHistory();
}

async function sendMessageHandler() {
    const userInputElement = document.getElementById("user-input");
    const userQuery = userInputElement.value.trim();
    if (!userQuery) return;

    userInputElement.value = "";
    displayMessage("user", userQuery);

    const { conversationId, assistantReply } = await sendMessage(currentConversationId, userQuery);
    if (assistantReply) {
        displayMessage("assistant", assistantReply);
        currentConversationId = conversationId;
        loadConversationHistory();
    }
}

async function sendMessage(conversationId, userQuery) {
    const data = {
        inputs: {},
        query: userQuery,
        response_mode: "blocking",
        conversation_id: conversationId,
        user: "user-123"
    };

    try {
        const response = await fetch(`${API_URL}/chat-messages`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error(`Fehler: ${response.status}`);
        
        const responseData = await response.json();
        const newConversationId = responseData.conversation_id;
        const assistantReply = responseData.answer || "Keine Antwort erhalten.";
        
        saveConversation(newConversationId, userQuery, assistantReply);
        return { conversationId: newConversationId, assistantReply };
    } catch (error) {
        console.error(error);
        return { conversationId, assistantReply: "❌ Fehler bei der Kommunikation mit dem Server." };
    }
}

function saveConversation(conversationId, userQuery, assistantReply) {
    let conversations = JSON.parse(localStorage.getItem(conversationStorageKey)) || {};
    if (!conversations[conversationId]) {
        conversations[conversationId] = { title: `Chat ${Object.keys(conversations).length + 1}`, messages: [] };
    }
    conversations[conversationId].messages.push({ role: "user", content: userQuery });
    conversations[conversationId].messages.push({ role: "assistant", content: assistantReply });
    localStorage.setItem(conversationStorageKey, JSON.stringify(conversations));
}

function loadConversationHistory() {
    const conversations = JSON.parse(localStorage.getItem(conversationStorageKey)) || {};
    const sidebar = document.getElementById("conversation-list");
    sidebar.innerHTML = "";

    Object.entries(conversations).forEach(([id, convo]) => {
        const convoElement = document.createElement("div");
        convoElement.className = "conversation-item";
        convoElement.textContent = convo.title;
        convoElement.onclick = () => loadConversation(id);
        sidebar.appendChild(convoElement);
    });
}

function loadConversation(conversationId) {
    currentConversationId = conversationId;
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = "";
    const conversations = JSON.parse(localStorage.getItem(conversationStorageKey)) || {};
    if (conversations[conversationId]) {
        conversations[conversationId].messages.forEach(msg => displayMessage(msg.role, msg.content));
    }
}

function displayMessage(role, content) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("div");
    messageElement.className = role;
    messageElement.innerHTML = `<strong>${role === "user" ? "👤" : "🤖"}</strong> ${content}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("hidden");
    adjustLayout();
}

function adjustLayout() {
    const container = document.querySelector('.container');
    const sidebar = document.getElementById('sidebar');
    const chatContainer = document.querySelector('.chat-container');

    // Ensure the container always takes full height and width of the page
    container.style.height = "100vh";
    container.style.width = "100%";

    // Adjust width of chat container when sidebar is toggled
    if (sidebar.classList.contains("hidden")) {
        chatContainer.style.width = "100%";  // Use full width when sidebar is hidden
    } else {
        chatContainer.style.width = "calc(100% - 280px)";  // Adjust width when sidebar is visible
    }
}
