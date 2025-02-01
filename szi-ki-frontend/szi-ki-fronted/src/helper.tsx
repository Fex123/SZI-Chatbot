export class Chat {
    private _messages: string[];
    title: string;
    date: Date;

  
    constructor(title: string, messages: string[], date: Date) {
      this.title = title;
      this._messages = messages;
      this.date = date;

    }
  
    get messages(): string[] {
      return this._messages;
    }
  
    set messages(newMessages: string[]) {
      this._messages = newMessages;
    }
  }
  