import { useState } from 'react';
import './App.css';
import ChatComp from './ChatComp';
import Sidebar from './sidebar';
import { Chat } from './helper';



//TODO: If chat empty, show text input in middle, 


function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [selectedChat, setSelectedChat] = useState<Chat | null>(null);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  }; 

  return (
    <div className={`container ${darkMode ? 'dark' : ''}`}>
      <Sidebar setSelectedChat={setSelectedChat} toggleDarkmode={toggleDarkMode}/>
      <ChatComp chat={selectedChat ? selectedChat : new Chat("Kaufmännischer Beruf", [
    "Was macht ein Kaufmann?", 
    "Ein Kaufmann (oder eine Kauffrau) ist jemand, der im Bereich Handel und Wirtschaft tätig ist und dabei Waren oder Dienstleistungen einkauft, verkauft oder organisiert. Je nach Branche und Spezialisierung können die Aufgaben stark variieren, aber hier sind einige typische Tätigkeiten, die ein Kaufmann ausführt: Ein Kaufmann (oder eine Kauffrau) ist jemand, der im Bereich Handel und Wirtschaft tätig ist und dabei Waren oder Dienstleistungen einkauft, verkauft oder organisiert. Je nach Branche und Spezialisierung können die Aufgaben stark variieren, aber hier sind einige typische Tätigkeiten, die ein Kaufmann ausführt: Ein Kaufmann (oder eine Kauffrau) ist jemand, der im Bereich Handel und Wirtschaft tätig ist und dabei Waren oder Dienstleistungen einkauft, verkauft oder organisiert. Je nach Branche und Spezialisierung können die Aufgaben stark variieren, aber hier sind einige typische Tätigkeiten, die ein Kaufmann ausführt: Ein Kaufmann (oder eine Kauffrau) ist jemand, der im Bereich Handel und Wirtschaft tätig ist und dabei Waren oder Dienstleistungen einkauft, verkauft oder organisiert. Je nach Branche und Spezialisierung können die Aufgaben stark variieren, aber hier sind einige typische Tätigkeiten, die ein Kaufmann ausführt:", 
    "Achso, und was macht ein Verkaufmann?"
  ], new Date('2023-02-01'))} toggleDarkmode={toggleDarkMode}/>
    </div>
  );
}

export default App;


