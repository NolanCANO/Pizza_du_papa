import { TestBed } from '@angular/core/testing';
import { CartPage } from './cart.page';
import { CartService } from '../../core/services/cart.service';
import { LoggerService } from '../../core/services/logger.service';
import { provideRouter } from '@angular/router';

describe('CartPage', () => {
  let component: CartPage;
  let cartService: CartService;
  let loggerService: LoggerService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [CartPage],
      providers: [
        CartService,
        { provide: LoggerService, useValue: jasmine.createSpyObj('LoggerService', ['info']) },
        provideRouter([])
      ]
    });

    component = TestBed.createComponent(CartPage).componentInstance;
    cartService = TestBed.inject(CartService);
    loggerService = TestBed.inject(LoggerService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should update quantity', () => {
    const mockPizza = { id: 1, name: 'Margherita', description: 'Classic', price: 8.5, is_available: true };
    cartService.add(mockPizza, 2);

    component.updateQuantity(1, 5);

    expect(cartService.cartItems()[0].quantity).toBe(5);
  });

  it('should remove item from cart', () => {
    const mockPizza = { id: 1, name: 'Margherita', description: 'Classic', price: 8.5, is_available: true };
    cartService.add(mockPizza, 1);

    component.remove(1);

    expect(cartService.cartItems().length).toBe(0);
  });

  it('should clear cart after confirmation', () => {
    spyOn(window, 'confirm').and.returnValue(true);
    const mockPizza = { id: 1, name: 'Margherita', description: 'Classic', price: 8.5, is_available: true };
    cartService.add(mockPizza, 1);

    component.clearCart();

    expect(cartService.cartItems().length).toBe(0);
  });
});
