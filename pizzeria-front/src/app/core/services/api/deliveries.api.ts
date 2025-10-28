import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Delivery } from '../../models/delivery.model';

@Injectable({
  providedIn: 'root'
})
export class DeliveriesApiService {
  private readonly endpoint = '/deliveries';

  constructor(private http: HttpClient) {}

  getById(id: number): Observable<Delivery> {
    return this.http.get<Delivery>(`${this.endpoint}/${id}`);
  }
}
