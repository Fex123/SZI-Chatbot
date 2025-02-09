export class Chat {
    private _messages: string[];
    title: string;
    date: Date;
    registered: boolean = false;

  
    constructor(title: string, messages: string[], date: Date, registered: boolean = false) {
      this.title = title;
      this._messages = messages;
      this.date = date;
      this.registered = registered;
    }
  
    get messages(): string[] {
      return this._messages;
    }
  
    set messages(newMessages: string[]) {
      this._messages = newMessages;
    }
  }
  