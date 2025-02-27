const API_URL = 'http://host.docker.internal:3104'; //"http://127.0.0.1:3104"; 
const API_user = "dev_user";

export function testConnection() {
  fetch(API_URL)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
}

//Fetches Conversation IDs and (TODO:) Titles, ** without message hisotry **

/*TODO:
Causes this error:
Access to fetch at 'http://127.0.0.1:5000//api/user/dev-user/conversations' from origin 'http://localhost:5173' has been 
blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource. 
If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.

DANGER! Muss besprochen werden, wenn das in Prod geht, weil das ein Sicherheitsrisiko sein könnte!
 */

export const fetchConversationTitles = async () => {
  const response = await fetch(`${API_URL}/api/conversations?user_id=${API_user}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }});
  const data = await response.json();
  return data;
}

export const fetchConversationMessages = async (conversation_id: string) => { 
  const response = await fetch(`${API_URL}/api/conversations/${conversation_id}/messages?user_id=${API_user}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });
  const data = await response.json();
  const messages = data.messages.map((message: { content: string }) => message.content);
  console.log('Fetched messages:', messages);
  return messages;
}

export const sendMessage = async (conversation_id: string, message: string) => {
  const response = await fetch(`${API_URL}/api/chat/send`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }, 
    body: JSON.stringify({
      query: message,
      conversation_id: conversation_id
    })
  });
  const data = await response.json();
  return data;
}


export class Chat {
    private _messages: string[];
    title: string;
    conversation_id: string;
    date: Date;
    registered: boolean = false;

  
    constructor(conversation_id: string, title: string, messages: string[], date: Date, registered: boolean = false) {
      this.title = title;
      this._messages = messages;
      this.date = date;
      this.registered = registered;
      this.conversation_id = conversation_id;
    }
  
    get messages(): string[] {
      return this._messages;
    }
  
    set messages(newMessages: string[]) {
      this._messages = newMessages;
    }
  }
  
