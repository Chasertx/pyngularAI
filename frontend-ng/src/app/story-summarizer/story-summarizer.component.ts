import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Story, StoryService } from '../story.service';
import { MatToolbar } from '@angular/material/toolbar';
import { ToolbarComponent } from '../toolbar/toolbar.component';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-story-summarizer',
  imports: [
    CommonModule,
    MatToolbar,
    RouterModule,
    FormsModule,
    ToolbarComponent,
  ],
  templateUrl: './story-summarizer.component.html',
  styleUrl: './story-summarizer.component.css',
})
export class StorySummarizerComponent {
  text = '';
  result?: Story;
  loading = false;
  error = '';
  summary = '';

  constructor(private storyService: StoryService) {}

  summarize() {
    this.loading = true;
    this.result = undefined;
    this.error = '';
    this.summary = '';

    const story: Story = {
      text: this.text,
    };

    this.storyService.submitStory(story).subscribe({
      next: (res) => {
        this.result = res;
        this.summary = res.summary || 'No summary available.';
        this.loading = false;
      },
      error: () => {
        this.error = 'submission failed.';
        this.loading = false;
      },
    });
  }
}
