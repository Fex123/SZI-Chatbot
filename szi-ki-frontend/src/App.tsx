import { useState, useEffect } from 'react';
import './App.css';
import ChatComp from './ChatComp';
import Sidebar from './sidebar';
import { Chat, fetchConversationTitles } from './helper';
import { useNavigate } from 'react-router-dom';

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [chats, setChats] = useState<Chat[]>([]);
  const [selectedChat, setSelectedChat] = useState<Chat>(new Chat("", "", [], new Date(), true));
  const navigate = useNavigate();
  const token = sessionStorage.getItem('loginResponse') ? JSON.parse(sessionStorage.getItem('loginResponse')!).token : null;

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  useEffect(() => {
    if (!token) {
      return;
    }

    const fetchChats = async () => {
      try {
        const response = await fetchConversationTitles();
        const conversations = response.conversations;
        const fetchedChats = conversations.map((conversation: { id: string, title: string, created_at: string, updated_at: string }) =>
          new Chat(conversation.id, conversation.title, [], new Date(conversation.created_at), false)
        );
        setChats(fetchedChats);
        console.log('Fetched chats:', fetchedChats);
      } catch (error) {
        console.error('Error fetching chats:', error);
      }
    };

    fetchChats();
    console.log(chats);
  }, [token]);

  const addChat = (chat: Chat) => {
    setChats([...chats, chat]);
    console.log('Chat added:', chat, "\n Chats:", chats);
  };

  if (!token) {
    return (
      <div className="centered-container">
        <p>Sie sind nicht angemeldet.</p>
        <button onClick={() => navigate('/login')}>Zurück zum Login</button>
      </div>
    );
  }

  return (
    <div className={`container ${darkMode ? 'dark' : ''}`}>
      <Sidebar setSelectedChat={setSelectedChat} toggleDarkmode={toggleDarkMode} chats={chats} />
      <ChatComp chat={selectedChat} toggleDarkmode={toggleDarkMode} addChat={addChat} />
    </div>
  );
}

export default App;