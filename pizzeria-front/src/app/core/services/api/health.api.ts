import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HealthApiService {
  private readonly endpoint = '/health';

  constructor(private http: HttpClient) {}

  check(): Observable<{ status: string }> {
    return this.http.get<{ status: string }>(this.endpoint);
  }
}
