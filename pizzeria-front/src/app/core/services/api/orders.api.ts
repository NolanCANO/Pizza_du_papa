import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Order, OrderCreate } from '../../models/order.model';

@Injectable({
  providedIn: 'root'
})
export class OrdersApiService {
  private readonly endpoint = '/orders';

  constructor(private http: HttpClient) {}

  create(order: OrderCreate): Observable<Order> {
    return this.http.post<Order>(this.endpoint, order);
  }

  getById(id: number): Observable<Order> {
    return this.http.get<Order>(`${this.endpoint}/${id}`);
  }
}
