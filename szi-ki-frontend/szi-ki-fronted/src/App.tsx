import { useState } from 'react';
import './App.css';
import ChatComp from './ChatComp';
import Sidebar from './sidebar';
import { Chat } from './helper';



//TODO: state for chats
//TODO: Get chats from endpoint
const exampleChats = [
  new Chat("Chat 1", ["Hello", "How are you?", "I'm fine, thanks!"], new Date('2023-01-01')),
  new Chat("Chat 1", ["Hello", "How are you?", "I'm fine, thanks!"], new Date('2023-01-01')),
  new Chat("Chat 1ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss", ["Hello", "How are you?", "I'm fine, thanks!"], new Date('2023-01-01')),
  new Chat("Chat 1", ["Hello", "How are you?", "I'm fine, thanks!"], new Date('2023-01-01')),
  new Chat("Kaufmännischer Beruf", [
    "Was macht ein Kaufmann?", 
    "Ein Kaufmann (oder eine Kauffrau) ist jemand, der im Bereich Handel und Wirtschaft tätig ist und dabei Waren oder Dienstleistungen einkauft, verkauft oder organisiert. Je nach Branche und Spezialisierung können die Aufgaben stark variieren, aber hier sind einige typische Tätigkeiten, die ein Kaufmann ausführt: Ein Kaufmann (oder eine Kauffrau) ist jemand, der im Bereich Handel und Wirtschaft tätig ist und dabei Waren oder Dienstleistungen einkauft, verkauft oder organisiert. Je nach Branche und Spezialisierung können die Aufgaben stark variieren, aber hier sind einige typische Tätigkeiten, die ein Kaufmann ausführt: Ein Kaufmann (oder eine Kauffrau) ist jemand, der im Bereich Handel und Wirtschaft tätig ist und dabei Waren oder Dienstleistungen einkauft, verkauft oder organisiert. Je nach Branche und Spezialisierung können die Aufgaben stark variieren, aber hier sind einige typische Tätigkeiten, die ein Kaufmann ausführt: Ein Kaufmann (oder eine Kauffrau) ist jemand, der im Bereich Handel und Wirtschaft tätig ist und dabei Waren oder Dienstleistungen einkauft, verkauft oder organisiert. Je nach Branche und Spezialisierung können die Aufgaben stark variieren, aber hier sind einige typische Tätigkeiten, die ein Kaufmann ausführt:", 
    "Achso, und was macht ein Verkaufmann? "
  ], new Date('2023-02-01')),
  new Chat("Chat 3", ["Good morning", "Good morning! How did you sleep?", "Very well, thank you."], new Date('2023-03-01')),
];


function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [selectedChat, setSelectedChat] = useState<Chat>(new Chat("", [], new Date()));
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  }; 
  console.log('X2 Chat selected in App :', selectedChat);

  return (
    <div className={`container ${darkMode ? 'dark' : ''}`}>
      <Sidebar setSelectedChat={setSelectedChat} toggleDarkmode={toggleDarkMode} chats={exampleChats}/>
      <ChatComp chat={selectedChat} toggleDarkmode={toggleDarkMode}/>
    </div>
  );
}

export default App;


