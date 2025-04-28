import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { ToolbarComponent } from '../toolbar/toolbar.component';

@Component({
  selector: 'app-contact',
  imports: [CommonModule, FormsModule, ToolbarComponent],
  templateUrl: './contact.component.html',
  styleUrl: './contact.component.css',
})
export class ContactComponent {
  name = '';
  email = '';
  message = '';
  success = false;
  error = '';

  constructor(private http: HttpClient) {}

  submitForm() {
    const payload = {
      name: this.name,
      email: this.email,
      message: this.message,
    };
    this.http.post('http://127.0.0.1:8000/api/contact/', payload).subscribe({
      next: () => {
        this.success = true;
        this.error = '';
        this.name = '';
        this.email = '';
        this.message = '';
      },
      error: (err) => {
        this.error = 'Failed to send message. Please try again later.';
        console.error(err);
      },
    });
  }
}
