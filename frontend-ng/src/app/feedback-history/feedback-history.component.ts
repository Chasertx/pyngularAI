import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { RouterModule } from '@angular/router';
import { ToolbarComponent } from '../toolbar/toolbar.component';

@Component({
  selector: 'app-feedback-history',
  standalone: true,
  imports: [CommonModule, MatToolbarModule, RouterModule, ToolbarComponent],
  templateUrl: './feedback-history.component.html',
  styleUrl: './feedback-history.component.css',
})
export class FeedbackHistoryComponent {}
