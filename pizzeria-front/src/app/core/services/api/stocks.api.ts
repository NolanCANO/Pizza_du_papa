import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { StockItem } from '../../models/stock.model';

@Injectable({
  providedIn: 'root'
})
export class StocksApiService {
  private readonly endpoint = '/stocks';

  constructor(private http: HttpClient) {}

  getAll(): Observable<StockItem[]> {
    return this.http.get<StockItem[]>(this.endpoint);
  }
}
