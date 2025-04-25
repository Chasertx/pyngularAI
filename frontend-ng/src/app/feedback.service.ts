import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
/**
 * facilitates composing asynchronous or callback-based code,
 * making it easier to handle asynchronous events and data streams.
 * Think of it as a way to treat data flow as a stream of information, much like a pipeline
 */
import { Observable } from 'rxjs';

//Define an interface
export interface Feedback {
  id?: number;
  text: string;
  sentiment?: string;
  category?: string;
}

@Injectable({
  providedIn: 'root',
})
export class FeedbackService {
  //Define our backends api url
  private apiUrl = 'http://127.0.0.1:8000/api/feedback/';

  constructor(private http: HttpClient) {}

  submitFeedback(feedback: Feedback): Observable<Feedback> {
    return this.http.post<Feedback>(this.apiUrl, feedback);
  }
}
