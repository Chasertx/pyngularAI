import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Feedback, FeedbackService } from '../feedback.service';
import { MatToolbarModule } from '@angular/material/toolbar';
import { RouterModule } from '@angular/router';
import { ToolbarComponent } from '../toolbar/toolbar.component';

@Component({
  selector: 'app-feedback-form',
  imports: [
    CommonModule,
    FormsModule,
    MatToolbarModule,
    RouterModule,
    ToolbarComponent,
  ],
  standalone: true,
  templateUrl: './feedback-form.component.html',
  styleUrl: './feedback-form.component.css',
})
export class FeedbackFormComponent {
  text = '';
  result?: Feedback;
  loading = false;
  error = '';

  constructor(private feedbackService: FeedbackService) {}

  submit() {
    this.loading = true;
    this.result = undefined;
    this.error = '';

    // Construct a Feedback object
    const feedback: Feedback = {
      text: this.text,
    };

    this.feedbackService.submitFeedback(feedback).subscribe({
      next: (res) => {
        this.result = res;
        this.loading = false;
      },
      error: () => {
        this.error = 'Submission failed.';
        this.loading = false;
      },
    });
  }
}
