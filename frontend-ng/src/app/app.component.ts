import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FeedbackFormComponent } from './feedback-form/feedback-form.component';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, FeedbackFormComponent, RouterModule],
  standalone: true,
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {}
