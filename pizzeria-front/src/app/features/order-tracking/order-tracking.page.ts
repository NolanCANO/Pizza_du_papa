import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { OrdersApiService } from '../../core/services/api/orders.api';
import { LoggerService } from '../../core/services/logger.service';
import { Order } from '../../core/models/order.model';

@Component({
  selector: 'app-order-tracking',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './order-tracking.page.html'
})
export class OrderTrackingPage implements OnInit {
  order = signal<Order | null>(null);
  loading = signal(true);
  error = signal<string | null>(null);

  constructor(
    private route: ActivatedRoute,
    private ordersApi: OrdersApiService,
    private logger: LoggerService
  ) {}

  ngOnInit(): void {
    const orderId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadOrder(orderId);
  }

  loadOrder(orderId: number): void {
    this.loading.set(true);
    this.ordersApi.getById(orderId).subscribe({
      next: (order) => {
        this.order.set(order);
        this.loading.set(false);
        this.logger.info('Order loaded', { orderId });
      },
      error: (err) => {
        this.error.set('Commande introuvable');
        this.loading.set(false);
        this.logger.error('Failed to load order', err);
      }
    });
  }

  refresh(): void {
    if (this.order()) {
      this.loadOrder(this.order()!.id);
    }
  }

  getStatusBadgeClass(status: string): string {
    switch (status) {
      case 'PENDING': return 'badge-warning';
      case 'PREPARING': return 'badge-info';
      case 'OUT_FOR_DELIVERY': return 'badge-info';
      case 'DELIVERED': return 'badge-success';
      case 'CANCELLED': return 'badge-danger';
      default: return 'badge';
    }
  }

  getStatusLabel(status: string): string {
    const labels: Record<string, string> = {
      'PENDING': 'En attente',
      'PREPARING': 'En préparation',
      'OUT_FOR_DELIVERY': 'En livraison',
      'DELIVERED': 'Livré',
      'CANCELLED': 'Annulée'
    };
    return labels[status] || status;
  }
}
