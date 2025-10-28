import { Injectable, signal } from '@angular/core';
import { Pizza } from '../models/pizza.model';

export interface CartItem {
  pizza: Pizza;
  quantity: number;
}

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private items = signal<CartItem[]>([]);
  
  readonly cartItems = this.items.asReadonly();

  add(pizza: Pizza, quantity: number = 1): void {
    const currentItems = this.items();
    const existingItem = currentItems.find(item => item.pizza.id === pizza.id);

    if (existingItem) {
      this.items.set(
        currentItems.map(item =>
          item.pizza.id === pizza.id
            ? { ...item, quantity: item.quantity + quantity }
            : item
        )
      );
    } else {
      this.items.set([...currentItems, { pizza, quantity }]);
    }
  }

  remove(pizzaId: number): void {
    this.items.set(this.items().filter(item => item.pizza.id !== pizzaId));
  }

  updateQuantity(pizzaId: number, quantity: number): void {
    if (quantity <= 0) {
      this.remove(pizzaId);
      return;
    }

    this.items.set(
      this.items().map(item =>
        item.pizza.id === pizzaId
          ? { ...item, quantity }
          : item
      )
    );
  }

  clear(): void {
    this.items.set([]);
  }

  getTotal(): number {
    return this.items().reduce(
      (total, item) => total + item.pizza.price * item.quantity,
      0
    );
  }

  getItemCount(): number {
    return this.items().reduce((count, item) => count + item.quantity, 0);
  }
}
