import React, { useState } from 'react';
import { Chat } from './helper';

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
}

const newChatSvg = (
<svg width="28px" height="28px" className="plus-svg" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M6 12H18M12 6V18" stroke="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
)

const Sidebar: React.FC<SidebarProps> = ({ setSelectedChat }) => {
  const [chats, setChats] = useState<Chat[]>(exampleChats);

  const formatDate = (date: Date) => {
    return `${date.getDate().toString().padStart(2, '0')}.${(date.getMonth() + 1).toString().padStart(2, '0')}.${date.getFullYear()}`;
  };

  let lastDate: string | null = null;

  return (
    <div className="sidebar">
      <div className="sidebar-top-logo">
        <p>Placeholder for logo</p>
      </div>
      <div className="sidebar-top-bar">
      {newChatSvg}
      <div className="new-chat">Neuer Chat</div>
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