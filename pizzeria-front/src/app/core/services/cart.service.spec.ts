import { TestBed } from '@angular/core/testing';
import { CartService } from './cart.service';
import { Pizza } from '../models/pizza.model';

describe('CartService', () => {
  let service: CartService;
  let mockPizza1: Pizza;
  let mockPizza2: Pizza;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CartService);

    mockPizza1 = {
      id: 1,
      name: 'Margherita',
      description: 'Classic',
      price: 8.5,
      is_available: true
    };

    mockPizza2 = {
      id: 2,
      name: 'Pepperoni',
      description: 'Spicy',
      price: 10,
      is_available: true
    };
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('add', () => {
    it('should add a pizza to the cart', () => {
      service.add(mockPizza1, 1);
      
      expect(service.cartItems().length).toBe(1);
      expect(service.cartItems()[0].pizza).toEqual(mockPizza1);
      expect(service.cartItems()[0].quantity).toBe(1);
    });

    it('should increment quantity if pizza already exists', () => {
      service.add(mockPizza1, 1);
      service.add(mockPizza1, 2);
      
      expect(service.cartItems().length).toBe(1);
      expect(service.cartItems()[0].quantity).toBe(3);
    });

    it('should add multiple different pizzas', () => {
      service.add(mockPizza1, 1);
      service.add(mockPizza2, 2);
      
      expect(service.cartItems().length).toBe(2);
    });
  });

  describe('remove', () => {
    it('should remove a pizza from the cart', () => {
      service.add(mockPizza1, 1);
      service.add(mockPizza2, 1);
      
      service.remove(mockPizza1.id);
      
      expect(service.cartItems().length).toBe(1);
      expect(service.cartItems()[0].pizza.id).toBe(mockPizza2.id);
    });

    it('should do nothing if pizza not in cart', () => {
      service.add(mockPizza1, 1);
      
      service.remove(999);
      
      expect(service.cartItems().length).toBe(1);
    });
  });

  describe('updateQuantity', () => {
    it('should update the quantity of a pizza', () => {
      service.add(mockPizza1, 1);
      
      service.updateQuantity(mockPizza1.id, 5);
      
      expect(service.cartItems()[0].quantity).toBe(5);
    });

    it('should remove pizza if quantity is 0', () => {
      service.add(mockPizza1, 2);
      
      service.updateQuantity(mockPizza1.id, 0);
      
      expect(service.cartItems().length).toBe(0);
    });

    it('should remove pizza if quantity is negative', () => {
      service.add(mockPizza1, 2);
      
      service.updateQuantity(mockPizza1.id, -1);
      
      expect(service.cartItems().length).toBe(0);
    });
  });

  describe('clear', () => {
    it('should clear all items from cart', () => {
      service.add(mockPizza1, 1);
      service.add(mockPizza2, 2);
      
      service.clear();
      
      expect(service.cartItems().length).toBe(0);
    });
  });

  describe('getTotal', () => {
    it('should return 0 for empty cart', () => {
      expect(service.getTotal()).toBe(0);
    });

    it('should calculate total for single item', () => {
      service.add(mockPizza1, 2);
      
      expect(service.getTotal()).toBe(17); // 8.5 * 2
    });

    it('should calculate total for multiple items', () => {
      service.add(mockPizza1, 2); // 8.5 * 2 = 17
      service.add(mockPizza2, 1); // 10 * 1 = 10
      
      expect(service.getTotal()).toBe(27);
    });
  });

  describe('getItemCount', () => {
    it('should return 0 for empty cart', () => {
      expect(service.getItemCount()).toBe(0);
    });

    it('should count total quantity of all items', () => {
      service.add(mockPizza1, 2);
      service.add(mockPizza2, 3);
      
      expect(service.getItemCount()).toBe(5);
    });
  });
});
