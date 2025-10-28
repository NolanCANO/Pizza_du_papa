import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StocksApiService } from '../../core/services/api/stocks.api';
import { LoggerService } from '../../core/services/logger.service';
import { StockItem } from '../../core/models/stock.model';

@Component({
  selector: 'app-stocks',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './stocks.page.html'
})
export class StocksPage implements OnInit {
  stocks = signal<StockItem[]>([]);
  loading = signal(true);
  error = signal<string | null>(null);

  constructor(
    private stocksApi: StocksApiService,
    private logger: LoggerService
  ) {}

  ngOnInit(): void {
    this.loadStocks();
  }

  loadStocks(): void {
    this.loading.set(true);
    this.stocksApi.getAll().subscribe({
      next: (stocks) => {
        this.stocks.set(stocks);
        this.loading.set(false);
        this.logger.info('Stocks loaded', { count: stocks.length });
      },
      error: (err) => {
        this.error.set('Impossible de charger les stocks');
        this.loading.set(false);
        this.logger.error('Failed to load stocks', err);
      }
    });
  }

  getStockClass(quantity: number): string {
    if (quantity === 0) return 'text-red-600';
    if (quantity < 10) return 'text-orange-600';
    return 'text-green-600';
  }
}
