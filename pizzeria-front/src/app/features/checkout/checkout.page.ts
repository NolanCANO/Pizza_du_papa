import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { OrdersApiService } from '../../core/services/api/orders.api';
import { CartService } from '../../core/services/cart.service';
import { LoggerService } from '../../core/services/logger.service';
import { OrderCreate } from '../../core/models/order.model';

@Component({
  selector: 'app-checkout',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './checkout.page.html'
})
export class CheckoutPage {
  checkoutForm: FormGroup;
  submitting = signal(false);
  error = signal<string | null>(null);

  constructor(
    private fb: FormBuilder,
    private ordersApi: OrdersApiService,
    public cartService: CartService,
    private logger: LoggerService,
    private router: Router
  ) {
    this.checkoutForm = this.fb.group({
      customer_name: ['', [Validators.required, Validators.minLength(2)]],
      delivery_address: ['', [Validators.required, Validators.minLength(5)]]
    });
  }

  submit(): void {
    if (this.checkoutForm.invalid || this.cartService.cartItems().length === 0) {
      return;
    }

    this.submitting.set(true);
    this.error.set(null);

    const orderData: OrderCreate = {
      customer_name: this.checkoutForm.value.customer_name,
      delivery_address: this.checkoutForm.value.delivery_address,
      items: this.cartService.cartItems().map(item => ({
        pizza_id: item.pizza.id,
        quantity: item.quantity
      }))
    };

    this.ordersApi.create(orderData).subscribe({
      next: (order) => {
        this.logger.info('Order created successfully', { orderId: order.id });
        this.cartService.clear();
        alert(`Commande créée avec succès ! N° ${order.id}`);
        this.router.navigate(['/orders', order.id]);
      },
      error: (err) => {
        this.error.set(err.error?.detail || 'Erreur lors de la création de la commande');
        this.submitting.set(false);
        this.logger.error('Order creation failed', err);
      }
    });
  }
}
