import { Component, OnInit } from '@angular/core';
import { ChatService } from './chat.service';
import { Message } from './models/message.model'; 
import { CookieService } from 'ngx-cookie-service';
import 'prismjs/prism';
import 'prismjs/themes/prism-okaidia.css'; 
import { ModelDetailsDialogComponent } from './components/model-details-dialog/model-details-dialog.component';
import { MatDialog } from '@angular/material/dialog';


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
  showUsageInfo = false;
  totalTokensUsed: number = 0;
  totalCost: number = 0;

  constructor(private chatService: ChatService, private readonly cookieService: CookieService, public readonly dialog: MatDialog) {}

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
    const showUsageInfoString = this.cookieService.get('showUsageInfo') || '';
    if (this.apiKey != '') {
      this.chatService.setApiKey(this.apiKey);
    }
    if (this.modelName != '') {
      this.chatService.setModelName(this.modelName);
    }
    if (showUsageInfoString == 'true') {
      this.showUsageInfo = true
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
      this.totalTokensUsed += response.total_tokens_used;
      this.totalCost += response.total_cost;
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
    this.messages = [];
    this.totalCost = 0;
    this.totalTokensUsed = 0;
  }

  openModelDetails(): void {
    this.chatService.fetchModelDetails(this.modelName).subscribe(details => {
      this.dialog.open(ModelDetailsDialogComponent, {
        width: '400px',
        data: details
      });
    });
  }

  toggleUsageVisibility(): void {
    this.cookieService.set('showUsageInfo', String(this.showUsageInfo), 30);
  }
  
}
