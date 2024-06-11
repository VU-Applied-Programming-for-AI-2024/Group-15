import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AppService {
  private apiUrl = 'https://fitnessai-backend.azurewebsites.net/';  // Replace with your actual backend URL

  constructor(private http: HttpClient) {}

  getData(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/data-endpoint`);
  }

  postData(data: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/data-endpoint`, data);
  }

}
