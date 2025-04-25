import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DatabaseService } from '../database.service';
import { ToolbarComponent } from '../toolbar/toolbar.component';

@Component({
  selector: 'app-database-visualizer',
  standalone: true,
  imports: [CommonModule, FormsModule, ToolbarComponent],
  templateUrl: './database-visualizer.component.html',
  styleUrl: './database-visualizer.component.css',
})
export class DatabaseVisualizerComponent implements OnInit {
  models = ['Feedback', 'StorySummarization'];
  selectedModel = 'Feedback';
  searchTerm = '';
  data: any[] = [];
  keys: string[] = [];
  loading = false;
  error = '';

  page = 1;
  pageSize = 5;
  total = 0;

  constructor(private databaseService: DatabaseService) {}

  ngOnInit() {
    this.fetchData();
  }

  fetchData() {
    this.loading = true;
    this.error = '';

    this.databaseService
      .getModelData(
        this.selectedModel,
        this.page,
        this.pageSize,
        this.searchTerm
      )
      .subscribe({
        next: (res) => {
          this.data = res.results;
          this.total = res.count;
          this.keys = this.data.length ? Object.keys(this.data[0]) : [];
          this.loading = false;
        },
        error: () => {
          this.error = 'Failed to load data.';
          this.loading = false;
        },
      });
  }

  nextPage() {
    if (this.page * this.pageSize < this.total) {
      this.page++;
      this.fetchData();
    }
  }

  prevPage() {
    if (this.page > 1) {
      this.page--;
      this.fetchData();
    }
  }

  onSearchOrModelChange() {
    this.page = 1;
    this.fetchData();
  }
}
