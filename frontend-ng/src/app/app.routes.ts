//These are our routes to various components in our app.
import { Routes } from '@angular/router';
import { FeedbackFormComponent } from './feedback-form/feedback-form.component';
import { FeedbackHistoryComponent } from './feedback-history/feedback-history.component';
import { HomeComponent } from './home/home.component';
import { StorySummarizerComponent } from './story-summarizer/story-summarizer.component';
import { DatabaseVisualizerComponent } from './database-visualizer/database-visualizer.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'history', component: FeedbackHistoryComponent },
  { path: 'feedback', component: FeedbackFormComponent },
  { path: 'summarizer', component: StorySummarizerComponent },
  { path: 'database', component: DatabaseVisualizerComponent },
  { path: '**', redirectTo: '' },
];
