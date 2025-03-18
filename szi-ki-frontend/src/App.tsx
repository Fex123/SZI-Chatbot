import { useState, useEffect } from 'react';
import './App.css';
import ChatComp from './ChatComp';
import Sidebar from './sidebar';
import { Chat, fetchConversationTitles } from './helper';

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [chats, setChats] = useState<Chat[]>([]);
  const [selectedChat, setSelectedChat] = useState<Chat>(new Chat("", "", [], new Date(), true));
  const [errorMessage, setErrorMessage] = useState("");
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  useEffect(() => {
    const fetchChats = async () => {
      try {
        const response = await fetchConversationTitles();
        const conversations = response.conversations;
        //TODO: Check wieso das nichts zurück gibt??? Das kann nicht sein alter
        const fetchedChats = conversations.map((conversation: { id: string, title: string, created_at: string, updated_at: string }) =>
          new Chat(conversation.id, conversation.title, [], new Date(conversation.created_at), false)
        );
        setChats(fetchedChats);
        console.log('Fetched chats:', fetchedChats);
      } catch (error) {
        console.error('Error fetching chats:', error);
        setErrorMessage('Error fetching chats: ' + error);
      }
    };

    fetchChats();
    console.log(chats);
  }, []);

  const addChat = (chat: Chat) => {
    setChats([...chats, chat]);
    console.log('Chat added:', chat, "\n Chats:", chats);
  }

  return (
    <div className={`container ${darkMode ? 'dark' : ''}`}>
      <Sidebar errorMessage={errorMessage} setSelectedChat={setSelectedChat} toggleDarkmode={toggleDarkMode} chats={chats} />
      <ChatComp chat={selectedChat} toggleDarkmode={toggleDarkMode} addChat={addChat} />
    </div>
  );
}

export default App;


