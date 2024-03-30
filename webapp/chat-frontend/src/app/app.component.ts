import { Component, OnInit } from '@angular/core';
import { ChatService } from './chat.service';
import { Message } from './models/message.model'; 
import { CookieService } from 'ngx-cookie-service';
import 'prismjs/prism';
import 'prismjs/themes/prism-okaidia.css'; 


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  userMessage = '';
  messages: Message[] = []; 
  apiKey = "";
  modelName = '';
  models: any[] = [];

  constructor(private chatService: ChatService, private readonly cookieService: CookieService) {}

  ngOnInit(): void {
    this.chatService.fetchModels().subscribe({
      next: (models) => {
        this.models = models;
      },
      error: (error) => {
        console.error('Failed to fetch models', error);
      }
    });
    this.apiKey = this.cookieService.get('apiKey') || '';
    this.modelName = this.cookieService.get('modelName') || '';
    if (this.apiKey != '') {
      this.chatService.setApiKey(this.apiKey);
    }
    if (this.modelName != '') {
      this.chatService.setModelName(this.modelName);
    }
  }

  sendMessage(): void {
    const userMessage = this.userMessage.trim();
    if (!userMessage) return;

    const messageToSend: Message = { role: 'user', content: userMessage }; 
    this.messages.push(messageToSend);

    this.chatService.sendMessage(userMessage).subscribe(response => {
      const responseMessage: Message = { role: 'assistant', content: response.response };
      this.messages.push(responseMessage);
    });

    this.userMessage = '';
  }

  setApiKey(): void {
    this.chatService.setApiKey(this.apiKey);
    this.cookieService.set('apiKey', this.apiKey, 30);
  }

  setModelName(): void {
    this.chatService.setModelName(this.modelName);
    this.cookieService.set('modelName', this.modelName, 30);
  }

  resetChat(): void {
    this.chatService.resetSession();
    // Optionally clear the current chat history in the UI
    this.messages = [];
  }
  
}
