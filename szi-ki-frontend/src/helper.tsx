const API_URL = 'http://localhost:3104'; //"http://localhost:3104"; 

export const fetchConversationTitles = async () => {
  const token = sessionStorage.getItem('loginResponse-plaiooijdjfpakij103978128739807298312') ? JSON.parse(sessionStorage.getItem('loginResponse-plaiooijdjfpakij103978128739807298312')!).token : null;
  const response = await fetch(`${API_URL}/api/conversations`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Failed to fetch conversation titles');
  }

  const data = await response.json();
  return data;
}

export const fetchConversationMessages = async (conversation_id: string) => {
  const token = sessionStorage.getItem('loginResponse-plaiooijdjfpakij103978128739807298312') ? JSON.parse(sessionStorage.getItem('loginResponse-plaiooijdjfpakij103978128739807298312')!).token : null;
  const response = await fetch(`${API_URL}/api/conversations/${conversation_id}/messages`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Failed to fetch conversation messages');
  }

  const data = await response.json();
  const messages = data.messages.map((message: { content: string }) => message.content);
  console.log('Fetched messages:', messages);
  return messages;
}

export const sendMessage = async (conversation_id: string, message: string) => {
  const token = sessionStorage.getItem('loginResponse-plaiooijdjfpakij103978128739807298312') ? JSON.parse(sessionStorage.getItem('loginResponse-plaiooijdjfpakij103978128739807298312')!).token : null;
  const response = await fetch(`${API_URL}/api/chat/send`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      query: message,
      conversation_id: conversation_id
    })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Failed to send message');
  }

  const data = await response.json();
  return data;
}

export const loginUser = async (username: string, password: string) => {
  const response = await fetch(`${API_URL}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: username,
      password: password
    })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Login failed');
  }

  const data = await response.json();
  return data;
};

export const registerUser = async (username: string, password: string, displayName: string) => {
  const response = await fetch(`${API_URL}/api/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: username,
      password: password,
      display_name: displayName
    })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Registration failed');
  }

  const data = await response.json();
  return data;
};

export const logoutUser = async () => {
  const token = sessionStorage.getItem('loginResponse-plaiooijdjfpakij103978128739807298312') ? JSON.parse(sessionStorage.getItem('loginResponse-plaiooijdjfpakij103978128739807298312')!).token : null;
  const response = await fetch(`${API_URL}/api/auth/logout`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Logout failed');
  }

  const data = await response.json();
  return data;
};

export const fetchTopQueries = async () => {
  const token = sessionStorage.getItem('loginResponse-plaiooijdjfpakij103978128739807298312') ? JSON.parse(sessionStorage.getItem('loginResponse-plaiooijdjfpakij103978128739807298312')!).token : null;
  const response = await fetch(`${API_URL}/api/top-queries`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Failed to fetch top queries');
  }

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