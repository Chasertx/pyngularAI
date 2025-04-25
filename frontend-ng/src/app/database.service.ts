import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DatabaseService {
  private apiUrl = 'http://127.0.0.1:8000/api/databasevisualizer/';

  constructor(private http: HttpClient) {}

  getModelData(
    model: string,
    page = 1,
    pageSize = 10,
    search = ''
  ): Observable<any> {
    const params = new HttpParams()
      .set('model', model)
      .set('page', page)
      .set('page_size', pageSize)
      .set('search', search);
    return this.http.get(this.apiUrl, { params });
  }
}
