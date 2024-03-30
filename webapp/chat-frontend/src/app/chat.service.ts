 
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { v4 as uuidv4 } from 'uuid';

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  private apiUrl = 'http://localhost:5000'; // Adjust if your Flask API is hosted elsewhere
  private apiKey: string = "";
  private modelName: string = 'mistralai/mistral-7b-instruct:free';
  private sessionId: string;

  constructor(private http: HttpClient) { 
    this.sessionId = uuidv4();
  }

  setApiKey(key: string): void {
    this.apiKey = key;
  }

  setModelName(model: string): void {
    this.modelName = model;
  }

  resetSession(): void {
    this.sessionId = uuidv4();
  }

  sendMessage(message: string): Observable<any> {
    return this.http.post(this.apiUrl + '/chat', {
      apiKey: this.apiKey,
      modelName: this.modelName, 
      message: message,
      sessionId: this.sessionId,
    });
  }

  fetchModels(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl + '/models');  // Adjust the URL if your Flask app is hosted elsewhere
  }

}
