import React, { Component } from 'react';
import { Chat } from './helper';
import DarkModeToggle from './Dmtoggle';
import logo from './assets/logo.svg';


const newChatSvg = (
  <svg width="28px" height="28px" className="plus-svg" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" clip-rule="evenodd" d="M12 3C7.02944 3 3 7.02944 3 12C3 16.9706 7.02944 21 12 21H16.5C17.8978 21 18.5967 21 19.1481 20.7716C19.8831 20.4672 20.4672 19.8831 20.7716 19.1481C21 18.5967 21 17.8978 21 16.5V12C21 7.02944 16.9706 3 12 3ZM12 16.0002C11.4477 16.0002 11 15.5525 11 15.0002V13H9C8.44772 13 8 12.5523 8 12C8 11.4477 8.44772 11 9 11H11V9.00024C11 8.44795 11.4477 8.00024 12 8.00024C12.5523 8.00024 13 8.44795 13 9.00024V11H15C15.5523 11 16 11.4477 16 12C16 12.5523 15.5523 13 15 13H13V15.0002C13 15.5525 12.5523 16.0002 12 16.0002Z" fill="none"></path> </g></svg>
)

interface SidebarProps {
  setSelectedChat: (chat: Chat) => void;
  toggleDarkmode: () => void;
  chats: Chat[];
}

interface SidebarState {
  lastDate: string | null;
}

class Sidebar extends Component<SidebarProps, SidebarState> {
  constructor(props: SidebarProps) {
    super(props);
    this.state = {
      lastDate: null,
    };
  }

  setChat = (chat: Chat) => {
    console.log('Chat selected:', chat);
    this.props.setSelectedChat(chat);
  }

  render() {
    const { toggleDarkmode } = this.props;

    return (
      <div className="sidebar">
        <div className="sidebar-top-logo">
          <img src={logo} alt="Logo" className="dhbw-logo" title="Create new chat"/>
        </div>
        <div className="sidebar-top-bar">
          <DarkModeToggle isDark={false} toggleDarkMode={toggleDarkmode} />
          <button className='dark-mode-button' onClick={() => this.setChat(new Chat("New Chat", [], new Date(), false))}>
            {newChatSvg}
          </button>
        </div>
        {this.props.chats.map((chat, index) => {
          return (
            <React.Fragment key={index}>
              <div className="chat-sidebar-item" onClick={() => this.setChat(chat)}>
                {chat.title}
              </div>
            </React.Fragment>
          );
        })}
      </div>
    );
  }
}

export default Sidebar;