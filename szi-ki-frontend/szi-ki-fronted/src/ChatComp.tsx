import React, { Component } from 'react';
import { Chat } from './helper';
import './App.css';
import DarkModeToggle from './Dmtoggle';


//TODO: Block Input if still waiting for response
//TODO: implement throbber when waiting for response (User feedback => "we're working on it")
//TODO: Create new chat in side bar when user creates a new chat
//TODO: If chat empty, show text input in middle,

interface ChatProps {
  chat: Chat | null;
  toggleDarkmode: () => void;
}

const cKiSvg = (
  <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="300" height="300" viewBox="0 0 1080 1080">
    <desc>Created with Fabric.js 5.2.4</desc>
    <defs></defs>
    <g transform="matrix(1 0 0 1 540 540)" id="4afb33f4-52ea-45e9-be78-e44c04acc839">
      <rect style={{ stroke: 'none', strokeWidth: 1, fill: 'rgb(255,255,255)', opacity: 1, visibility: 'hidden' }} x="-540" y="-540" width="300" height="300" />
    </g>
    <g transform="matrix(1 0 0 1 540 540)" id="f6e6be23-77b1-42b8-aa0b-2cf6a9aae54a"></g>
    <g transform="matrix(1.6 0 0 1 540 540)" id="019f50f9-62cd-4f7a-a11f-3ebe6fa0de55">
      <path style={{ stroke: 'rgb(0,0,0)', strokeWidth: 8, fill: 'rgb(255,255,255)', opacity: 1 }} transform="translate(-50, -50)" d="M 90.375 90.375 L 9.625 90.375 L 9.625 9.625 L 90.375 9.625 L 90.375 90.375 z M 11.625 88.375 L 88.375 88.375 L 88.375 11.625 L 11.625 11.625 L 11.625 88.375 z" />
    </g>
    <g transform="matrix(0.29 0 0 0.29 504.98 540)" id="f94b85ea-fb32-428e-88f3-cc39e7a3c4d6">
      <circle style={{ stroke: 'rgb(0,0,0)', strokeWidth: 0, fill: 'rgb(0,0,0)', opacity: 1 }} cx="0" cy="0" r="35" />
    </g>
    <g transform="matrix(0.29 0 0 0.29 577.86 552.45)" id="f94b85ea-fb32-428e-88f3-cc39e7a3c4d6">
      <circle style={{ stroke: 'rgb(0,0,0)', strokeWidth: 0, fill: 'rgb(0,0,0)', opacity: 1 }} cx="0" cy="0" r="35" />
    </g>
    <g transform="matrix(-0.99 0.15 -0.15 -0.99 568.57 474.2)" id="dfde464e-9ec8-4c4b-8bde-3f3c13263d61">
      <path style={{ stroke: 'rgb(0,0,0)', strokeWidth: 0, fill: 'rgb(0,0,0)', opacity: 1 }} transform="translate(-50, -50)" d="M 14.148 44.105 L 18.091 40.162 C 20.01 38.242 23.176000000000002 38.242 25.096 40.162 L 42.164 57.230999999999995 L 74.904 24.440999999999995 C 76.823 22.521999999999995 79.98899999999999 22.521999999999995 81.90899999999999 24.440999999999995 L 85.851 28.383999999999997 C 87.771 30.302999999999997 87.771 33.415 85.851 35.334999999999994 L 45.641 75.54499999999999 L 45.537 75.64899999999999 L 45.433 75.75299999999999 L 45.329 75.80499999999999 L 45.277 75.90899999999999 L 45.173 75.961 L 45.069 76.065 L 44.965 76.117 L 44.861000000000004 76.16900000000001 L 44.757000000000005 76.27400000000002 L 44.653000000000006 76.32400000000001 L 44.54900000000001 76.37800000000001 L 44.44500000000001 76.43000000000002 L 44.34100000000001 76.48200000000003 L 44.23700000000001 76.53400000000003 L 44.08000000000001 76.58600000000004 L 43.97600000000001 76.63800000000005 L 43.872000000000014 76.69000000000005 L 43.768000000000015 76.74200000000006 L 43.664000000000016 76.74200000000006 L 43.56000000000002 76.79400000000007 L 43.405000000000015 76.84700000000007 L 43.301000000000016 76.84700000000007 L 43.19700000000002 76.89900000000007 L 42.93800000000002 76.89900000000007 L 42.83400000000002 76.95100000000008 L 42.62600000000002 76.95100000000008 L 42.47100000000002 77.00300000000009 L 41.795000000000016 77.00300000000009 L 41.640000000000015 76.95100000000008 L 41.432000000000016 76.95100000000008 L 41.32800000000002 76.89900000000007 L 41.06900000000002 76.89900000000007 L 40.96500000000002 76.84700000000007 L 40.86100000000002 76.84700000000007 L 40.70600000000002 76.79400000000007 L 40.60200000000002 76.74200000000006 L 40.49800000000002 76.74200000000006 L 40.39400000000002 76.69000000000005 L 40.29000000000002 76.63800000000005 L 40.185000000000024 76.58600000000004 L 40.081000000000024 76.53400000000003 L 40.029000000000025 76.53400000000003 C 39.563000000000024 76.32500000000003 39.096000000000025 75.96200000000003 38.630000000000024 75.54800000000003 L 14.140000000000025 51.059000000000026 C 12.229 49.137 12.229 46.025 14.148 44.105 z" />
    </g>
    <g transform="matrix(0.47 0 0 0.47 607.79 473.6)" id="f570ad6b-0351-4402-b142-333e4fea0dad">
      <circle style={{ stroke: 'rgb(0,0,0)', strokeWidth: 0, fill: 'rgb(0,0,0)', opacity: 1 }} cx="0" cy="0" r="35" />
    </g>
  </svg>
)

const kiSvg = (
<svg className="ki-svg" width="28px" height="28px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" clip-rule="evenodd" d="M14 2C14 2.74028 13.5978 3.38663 13 3.73244V4H20C21.6569 4 23 5.34315 23 7V19C23 20.6569 21.6569 22 20 22H4C2.34315 22 1 20.6569 1 19V7C1 5.34315 2.34315 4 4 4H11V3.73244C10.4022 3.38663 10 2.74028 10 2C10 0.895431 10.8954 0 12 0C13.1046 0 14 0.895431 14 2ZM4 6H11H13H20C20.5523 6 21 6.44772 21 7V19C21 19.5523 20.5523 20 20 20H4C3.44772 20 3 19.5523 3 19V7C3 6.44772 3.44772 6 4 6ZM15 11.5C15 10.6716 15.6716 10 16.5 10C17.3284 10 18 10.6716 18 11.5C18 12.3284 17.3284 13 16.5 13C15.6716 13 15 12.3284 15 11.5ZM16.5 8C14.567 8 13 9.567 13 11.5C13 13.433 14.567 15 16.5 15C18.433 15 20 13.433 20 11.5C20 9.567 18.433 8 16.5 8ZM7.5 10C6.67157 10 6 10.6716 6 11.5C6 12.3284 6.67157 13 7.5 13C8.32843 13 9 12.3284 9 11.5C9 10.6716 8.32843 10 7.5 10ZM4 11.5C4 9.567 5.567 8 7.5 8C9.433 8 11 9.567 11 11.5C11 13.433 9.433 15 7.5 15C5.567 15 4 13.433 4 11.5ZM10.8944 16.5528C10.6474 16.0588 10.0468 15.8586 9.55279 16.1056C9.05881 16.3526 8.85858 16.9532 9.10557 17.4472C9.68052 18.5971 10.9822 19 12 19C13.0178 19 14.3195 18.5971 14.8944 17.4472C15.1414 16.9532 14.9412 16.3526 14.4472 16.1056C13.9532 15.8586 13.3526 16.0588 13.1056 16.5528C13.0139 16.7362 12.6488 17 12 17C11.3512 17 10.9861 16.7362 10.8944 16.5528Z" fill="none"></path> </g></svg>
);

const sendSvg = (
  <svg width="28px" height="28px" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" id="send" className="send-svg">
    <path d="M21.66,12a2,2,0,0,1-1.14,1.81L5.87,20.75A2.08,2.08,0,0,1,5,21a2,2,0,0,1-1.82-2.82L5.46,13H11a1,1,0,0,0,0-2H5.46L3.18,5.87A2,2,0,0,1,5.86,3.25h0l14.65,6.94A2,2,0,0,1,21.66,12Z" fill="none"></path></svg>
);

const studentSvg = (
  <svg className="student-svg" height="28px" width="28px" version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xmlSpace="preserve">
    <g>
      <path className="st0" d="M505.837,180.418L279.265,76.124c-7.349-3.385-15.177-5.093-23.265-5.093c-8.088,0-15.914,1.708-23.265,5.093
        L6.163,180.418C2.418,182.149,0,185.922,0,190.045s2.418,7.896,6.163,9.627l226.572,104.294c7.349,3.385,15.177,5.101,23.265,5.101
        c8.088,0,15.916-1.716,23.267-5.101l178.812-82.306v82.881c-7.096,0.8-12.63,6.84-12.63,14.138c0,6.359,4.208,11.864,10.206,13.618
        l-12.092,79.791h55.676l-12.09-79.791c5.996-1.754,10.204-7.259,10.204-13.618c0-7.298-5.534-13.338-12.63-14.138v-95.148
        l21.116-9.721c3.744-1.731,6.163-5.504,6.163-9.627S509.582,182.149,505.837,180.418z"/>
      <path className="st0" d="M256,346.831c-11.246,0-22.143-2.391-32.386-7.104L112.793,288.71v101.638
        c0,22.314,67.426,50.621,143.207,50.621c75.782,0,143.209-28.308,143.209-50.621V288.71l-110.827,51.017
        C278.145,344.44,267.25,346.831,256,346.831z"/>
    </g>
  </svg>
);


interface ChatState {
  chat: Chat | null;
  inputText: string;
  }

class ChatComp extends Component<ChatProps, ChatState> {
  textareaRef = React.createRef<HTMLTextAreaElement>();

  constructor(props: ChatProps) {
    super(props);
    this.state = {
      chat: props.chat,
      inputText: '',
    };
  }

  handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    this.setState({ inputText: event.target.value }, this.adjustTextareaHeight);
  };

  adjustTextareaHeight = () => {
    const textarea = this.textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto'; // Reset height to recalculate
      textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px'; // Grow up to max-height
    }
  };

  handleButtonClick = () => {
    const { chat, inputText } = this.state;
    const trimmedInput = inputText.trim();
    if (trimmedInput === '') {
      return;
    }

    let newChat = chat;
    if (!chat) {
      newChat = new Chat('New Chat', [], new Date());
    }

    const newMessages = newChat ? [...newChat.messages, trimmedInput] : [trimmedInput];
    if (newChat) {
      newChat.messages = newMessages;
    }

    this.setState({
      chat: newChat,
      inputText: ''
    },() => {
      this.adjustTextareaHeight(); // Reset the textarea height after clearing the input
    });
  };

  render() {
    const { chat, inputText } = this.state;

    return (
      <div className="content">
        <div className="chat-top-bar">
          <p>SZI Assistent</p>
          
          {/*Replace with Profile Picture / generic Avatar if Nutzerkonzept is ever added.
           For that: Remove DarkModeToggle from here and add it back to the component where the dark mode toggle is supposed to be.
           Sidebar is a good candidate for that.
          */}

            <DarkModeToggle isDark={false} toggleDarkMode={this.props.toggleDarkmode} />
          
        </div>

        <div className="chat-wrapper">
          <div className="chat-content">
          {chat && chat.messages.map((message, index) => (
          <div className="chat-message-wrapper" key={index}>
            {index % 2 !== 0 ? (
              <div className="chat-profile-pic">
                {kiSvg}
              </div>
            ) : (
              <div className="chat-profile-pic">
                {studentSvg}
              </div>
            )}
            <div className={index % 2 === 0 ? 'user-message' : 'bot-message'}>
              {message}
            </div>
          </div>
        ))}
          </div>
        </div>
        <div className="chat-text-input-wrapper">
            <div className="chat-input-box">
            <textarea
                        ref={this.textareaRef}

            className="chat-text-input"
            placeholder="Frag mich etwas!"
            value={inputText}
            onChange={this.handleInputChange}
          />            <button className="send-button" onClick={this.handleButtonClick}>{sendSvg}</button>
            </div>
          </div>
      </div>
    );
  }
}

export default ChatComp;