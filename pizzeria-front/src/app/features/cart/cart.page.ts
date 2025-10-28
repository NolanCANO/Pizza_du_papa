import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { CartService } from '../../core/services/cart.service';
import { LoggerService } from '../../core/services/logger.service';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './cart.page.html'
})
export class CartPage {
  constructor(
    public cartService: CartService,
    private logger: LoggerService
  ) {}

  updateQuantity(pizzaId: number, quantity: number): void {
    this.cartService.updateQuantity(pizzaId, quantity);
    this.logger.info('Cart quantity updated', { pizzaId, quantity });
  }

  remove(pizzaId: number): void {
    this.cartService.remove(pizzaId);
    this.logger.info('Item removed from cart', { pizzaId });
  }

  clearCart(): void {
    if (confirm('Voulez-vous vraiment vider le panier ?')) {
      this.cartService.clear();
      this.logger.info('Cart cleared');
    }
  }
}
