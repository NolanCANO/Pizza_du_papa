import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Pizza } from '../../models/pizza.model';

@Injectable({
  providedIn: 'root'
})
export class PizzasApiService {
  private readonly endpoint = '/pizzas';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Pizza[]> {
    return this.http.get<Pizza[]>(this.endpoint);
  }

  getById(id: number): Observable<Pizza> {
    return this.http.get<Pizza>(`${this.endpoint}/${id}`);
  }
}
