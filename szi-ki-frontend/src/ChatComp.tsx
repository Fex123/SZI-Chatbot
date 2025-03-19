import React, { Component } from 'react';
import ReactMarkdown from 'react-markdown';
import { Chat, fetchConversationMessages, sendMessage, fetchTopQueries } from './helper';
import './App.css';
import DarkModeToggle from './Dmtoggle';
import ProfilePic from './UserProfile';

interface ChatProps {
  chat: Chat | null;
  toggleDarkmode: () => void;
  addChat: (chat: Chat) => void;
}

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
      <path className="st0" d="M505.837,180.418L279.265,76.124c-7.349-3.385-15.177-5.093-23.265-5.093c-8.088,0-15.914,1.708-23.265,5.093L6.163,180.418C2.418,182.149,0,185.922,0,190.045s2.418,7.896,6.163,9.627l226.572,104.294c7.349,3.385,15.177,5.101,23.265,5.101c8.088,0,15.916-1.716,23.267-5.101l178.812-82.306v82.881c-7.096,0.8-12.63,6.84-12.63,14.138c0,6.359,4.208,11.864,10.206,13.618l-12.092,79.791h55.676l-12.09-79.791c5.996-1.754,10.204-7.259,10.204-13.618c0-7.298-5.534-13.338-12.63-14.138v-95.148l21.116-9.721c3.744-1.731,6.163-5.504,6.163-9.627S509.582,182.149,505.837,180.418z" />
      <path className="st0" d="M256,346.831c-11.246,0-22.143-2.391-32.386-7.104L112.793,288.71v101.638c0,22.314,67.426,50.621,143.207,50.621c75.782,0,143.209-28.308,143.209-50.621V288.71l-110.827,51.017C278.145,344.44,267.25,346.831,256,346.831z" />
    </g>
  </svg>
);

interface ChatState {
  inputText: string;
  isLoading: boolean;
  isError: boolean;
  errorMessage: string | null;
  lastMessage: string;
  topQueries: string[];
  topQueriesError: string | null;
}

class ChatComp extends Component<ChatProps, ChatState> {
  textareaRef = React.createRef<HTMLTextAreaElement>();
  chatContentRef = React.createRef<HTMLDivElement>();

  constructor(props: ChatProps) {
    super(props);
    this.state = {
      inputText: '',
      isLoading: false,
      isError: false,
      errorMessage: null,
      lastMessage: "",
      topQueries: [],
      topQueriesError: null,
    };
  }

  async componentDidMount() {
    try {
      const data = await fetchTopQueries();
      this.setState({ topQueries: data.queries });
    } catch (error) {
      console.error('Error fetching top queries:', error);
      this.setState({ topQueriesError: 'Failed to fetch top queries. ' + error });
    }
  }

  componentDidUpdate(prevProps: ChatProps) {
    if (this.props.chat && this.props.chat !== prevProps.chat && !this.props.chat.registered && this.props.chat.conversation_id !== "") {
      this.fetchAndAddMessages(this.props.chat);
    }
  }

  fetchAndAddMessages = async (chat: Chat) => {
    try {
      let messages = await fetchConversationMessages(chat.conversation_id);
      chat.messages = messages;
      chat.registered = true;
      this.setState({});
    } catch (error) {
      console.error('Error fetching messages:', error);

      this.setState({ errorMessage: 'Die Nachrichten dieses Chats konnten nicht geladen Werden. Bitte Lade die Seite neu. ', isError: true });
    }
  };

  handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey && !this.state.isLoading && !this.state.isError) {
      event.preventDefault();
      this.handleInputButtonClick();
    }
  };

  handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    this.setState({ inputText: event.target.value }, this.adjustTextareaHeight);
  };

  adjustTextareaHeight = () => {
    const textarea = this.textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
    }
  };

  handleInputButtonClick = async (inputText?: string, isRetry?: boolean) => {
    const { chat } = this.props;
    const isRetryFlag = isRetry ?? false;
    const textToSend = inputText || this.state.inputText;
    const trimmedInput = textToSend.trim();
    if (trimmedInput === '') {
      return;
    }

    this.setState({
      inputText: '',
      errorMessage: null,
      isError: false,
    }, () => {
      this.adjustTextareaHeight();
    });

    if (chat) {
      if (!isRetryFlag) {
        chat.messages.push(trimmedInput);
      }
      this.scrollToBottom();

      this.setState({ isLoading: true, lastMessage: trimmedInput });

      try {
        const response = await sendMessage(chat.conversation_id, trimmedInput);

        if (chat.conversation_id == "") {
          chat.conversation_id = response.conversation_id;
          chat.title = trimmedInput;
          this.props.addChat(chat);
        }

        chat.registered = true;

        chat.messages.push(response.response);
        this.scrollToBottom();

      } catch (error) {

        console.error('Error sending message:', error);
        this.setState({ errorMessage: `Error sending message. \n \n ${error}`, isError: true });
      } finally {
        this.setState({ isLoading: false });
      }
    }
  };

  scrollToBottom = () => {
    const chatContent = this.chatContentRef.current;
    if (chatContent) {
      chatContent.scrollTop = chatContent.scrollHeight - chatContent.clientHeight;
    }
  };

  render() {
    const { chat } = this.props;
    const { inputText, isLoading, isError, errorMessage, lastMessage, topQueries, topQueriesError } = this.state;

    return (
      <div className="content">
        <div className="chat-top-bar">
          <p>SZI Assistent</p>
          <div className="chat-top-bar-buttons">
            <DarkModeToggle isDark={false} toggleDarkMode={this.props.toggleDarkmode} />
            <ProfilePic />
          </div>
        </div>

        <div className="chat-wrapper" ref={this.chatContentRef}>
          <div className="chat-content">
            {chat && chat.messages.length > 0 ? (
              chat.messages.map((message, index) => (
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
                    {index % 2 === 0 ? (
                      message
                    ) : (
                      <ReactMarkdown>{message}</ReactMarkdown>
                    )}
                  </div>
                </div>
              ))
            ) : (
              <div className="no-messages">
                <h1>Willkommen!</h1>
                <div className="intro-text-wrapper">
                  <div className="intro-text">Ich bin der SZI-Assistent! <br /> Du kannst mir Fragen rund um das Studienzentrum Informatik stellen!</div>
                  <div className="intro-text faq-style"> <br />Häufig gestellte Fragen:</div>
                </div>
                <div className="example-questions">
                  {topQueriesError ? (
                    <div className="error-message">
                      <div>{topQueriesError}</div>
                    </div>
                  ) : (
                    topQueries.map((query, index) => (
                      <div className="question-panel" key={index} onClick={() => this.handleInputButtonClick(query)}>{query}</div>
                    ))
                  )}
                </div>
              </div>
            )}
            {errorMessage && (
              <div className="error-message">
                <div>
                  {errorMessage}
                </div>

                <button className="try-again-button" onClick={() => this.handleInputButtonClick(lastMessage, true)}>Erneut versuchen</button>
              </div>
            )}
            {isLoading && (
              <div className="chat-message-wrapper">
                <div className="chat-profile-pic">
                  {kiSvg}
                </div>
                <div className="user-message">
                  <div className="loading-dots">
                    <span>.</span>
                    <span>.</span>
                    <span>.</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
        <div className="chat-text-input-wrapper">
          <div className="chat-input-box">
            <textarea
              ref={this.textareaRef}
              className="chat-text-input"
              placeholder="Stell mir eine Frage..."
              value={inputText}
              onChange={this.handleInputChange}
              onKeyDown={this.handleKeyDown}
            />
            <button className={`send-button ${isLoading || isError ? 'disabled' : ''}`} onClick={() => this.handleInputButtonClick()} disabled={isLoading || isError}>
              <div className="icon-hover-wrapper">
                {sendSvg}
              </div>
            </button>
          </div>
        </div>
      </div>
    );
  }
}

export default ChatComp;