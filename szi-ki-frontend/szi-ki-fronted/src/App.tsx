import { useState } from 'react';
import './App.css';
import ChatComp from './ChatComp';
import Sidebar from './sidebar';
import { Chat } from './helper';



//TODO: state for chats
//TODO: Get chats from endpoint
const exampleChats = [
  new Chat("Chat 1", ["Hello", "How are you?", "I'm fine, thanks!"], new Date('2023-01-01'), true),
  new Chat("Chat 1", ["Hello", "How are you?", "I'm fine, thanks!"], new Date('2023-01-01'), true),
  new Chat("Chat 1ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss", ["Hello", "How are you?", "I'm fine, thanks!"], new Date('2023-01-01'), true),
  new Chat("Chat 1", ["Hello", "How are you?", "I'm fine, thanks!"], new Date('2023-01-01'), true),
  new Chat("Kaufmännischer Beruf", [
    "Was macht ein Kaufmann?", 
    "Ein Kaufmann (oder eine Kauffrau) ist jemand, der im Bereich Handel und Wirtschaft tätig ist und dabei Waren oder Dienstleistungen einkauft, verkauft oder organisiert. Je nach Branche und Spezialisierung können die Aufgaben stark variieren, aber hier sind einige typische Tätigkeiten, die ein Kaufmann ausführt: Ein Kaufmann (oder eine Kauffrau) ist jemand, der im Bereich Handel und Wirtschaft tätig ist und dabei Waren oder Dienstleistungen einkauft, verkauft oder organisiert. Je nach Branche und Spezialisierung können die Aufgaben stark variieren, aber hier sind einige typische Tätigkeiten, die ein Kaufmann ausführt: Ein Kaufmann (oder eine Kauffrau) ist jemand, der im Bereich Handel und Wirtschaft tätig ist und dabei Waren oder Dienstleistungen einkauft, verkauft oder organisiert. Je nach Branche und Spezialisierung können die Aufgaben stark variieren, aber hier sind einige typische Tätigkeiten, die ein Kaufmann ausführt: Ein Kaufmann (oder eine Kauffrau) ist jemand, der im Bereich Handel und Wirtschaft tätig ist und dabei Waren oder Dienstleistungen einkauft, verkauft oder organisiert. Je nach Branche und Spezialisierung können die Aufgaben stark variieren, aber hier sind einige typische Tätigkeiten, die ein Kaufmann ausführt:", 
    "Achso, und was macht ein Verkaufmann? "
  ], new Date('2023-02-01'), true),
  new Chat("Chat 3", ["Good morning", "Good morning! How did you sleep?", "Very well, thank you."], new Date('2023-03-01'), true),
];


function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [chats, setChats] = useState<Chat[]>(exampleChats);
  const [selectedChat, setSelectedChat] = useState<Chat>(new Chat("", [], new Date(), false));
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  }; 

  const addChat = (chat: Chat) => {
    setChats([...chats, chat]);
    console.log('Chat added:', chat, "\n Chats:", chats);
  }
  //console.log('X2 Chat selected in App :', selectedChat);

  return (
    <div className={`container ${darkMode ? 'dark' : ''}`}>
      <Sidebar setSelectedChat={setSelectedChat} toggleDarkmode={toggleDarkMode} chats={chats}/>
      <ChatComp chat={selectedChat} toggleDarkmode={toggleDarkMode} addChat={addChat}/>
    </div>
  );
}

export default App;


