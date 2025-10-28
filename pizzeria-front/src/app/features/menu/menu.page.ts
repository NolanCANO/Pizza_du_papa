import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Pizza } from '../../core/models/pizza.model';
import { PizzasApiService } from '../../core/services/api/pizzas.api';
import { CartService } from '../../core/services/cart.service';
import { LoggerService } from '../../core/services/logger.service';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './menu.page.html'
})
export class MenuPage implements OnInit {
  pizzas = signal<Pizza[]>([]);
  loading = signal(true);
  error = signal<string | null>(null);

  constructor(
    private pizzasApi: PizzasApiService,
    private cartService: CartService,
    private logger: LoggerService
  ) {}

  ngOnInit(): void {
    this.loadPizzas();
  }

  loadPizzas(): void {
    this.loading.set(true);
    this.pizzasApi.getAll().subscribe({
      next: (pizzas) => {
        this.pizzas.set(pizzas);
        this.loading.set(false);
        this.logger.info('Pizzas loaded successfully', { count: pizzas.length });
      },
      error: (err) => {
        this.error.set('Impossible de charger les pizzas');
        this.loading.set(false);
        this.logger.error('Failed to load pizzas', err);
      }
    });
  }

  addToCart(pizza: Pizza): void {
    this.cartService.add(pizza, 1);
    this.logger.info('Pizza added to cart', { pizzaId: pizza.id, pizzaName: pizza.name });
    alert(`${pizza.name} ajoutée au panier !`);
  }
}
