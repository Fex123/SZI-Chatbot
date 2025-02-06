import React, { useState } from 'react';
import { Chat } from './helper';
import DarkModeToggle from './Dmtoggle';
import logo from './assets/logo.svg';



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

interface SidebarProps {
  setSelectedChat: (chat: Chat) => void;
  toggleDarkmode: () => void;

}

const plusSvg = (
<svg width="28px" height="28px" className="plus-svg" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M6 12H18M12 6V18" stroke="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
)

const newChatSvg = (
  <svg width="28px" height="28px" className="plus-svg" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" clip-rule="evenodd" d="M12 3C7.02944 3 3 7.02944 3 12C3 16.9706 7.02944 21 12 21H16.5C17.8978 21 18.5967 21 19.1481 20.7716C19.8831 20.4672 20.4672 19.8831 20.7716 19.1481C21 18.5967 21 17.8978 21 16.5V12C21 7.02944 16.9706 3 12 3ZM12 16.0002C11.4477 16.0002 11 15.5525 11 15.0002V13H9C8.44772 13 8 12.5523 8 12C8 11.4477 8.44772 11 9 11H11V9.00024C11 8.44795 11.4477 8.00024 12 8.00024C12.5523 8.00024 13 8.44795 13 9.00024V11H15C15.5523 11 16 11.4477 16 12C16 12.5523 15.5523 13 15 13H13V15.0002C13 15.5525 12.5523 16.0002 12 16.0002Z" fill="none"></path> </g></svg>
)

const Sidebar: React.FC<SidebarProps> = ({ setSelectedChat, toggleDarkmode }) => {
  const [chats, setChats] = useState<Chat[]>(exampleChats);

  const formatDate = (date: Date) => {
    return `${date.getDate().toString().padStart(2, '0')}.${(date.getMonth() + 1).toString().padStart(2, '0')}.${date.getFullYear()}`;
  };

  let lastDate: string | null = null;

  return (
    <div className="sidebar">
      <div className="sidebar-top-logo">
      <img src={logo} alt="Logo" className="dhbw-logo"/>
      </div>
      <div className="sidebar-top-bar">
      <DarkModeToggle isDark={false} toggleDarkMode={toggleDarkmode} />
      {newChatSvg}
      </div>
      {chats.map((chat, index) => {
        const chatDate = formatDate(chat.date);
        const showDateTitle = chatDate !== lastDate;
        lastDate = chatDate;

        return (
          <React.Fragment key={index}>
            {showDateTitle && (
              <div className="sidebar-date-title">
                {chatDate}
              </div>
            )}
            <div className="chat-sidebar-item" onClick={() => setSelectedChat(chat)}>
              {chat.title}
            </div>
          </React.Fragment>
        );
      })}
    </div>
  );
};

export default Sidebar;