import { TestBed } from '@angular/core/testing';
import { MenuPage } from './menu.page';
import { PizzasApiService } from '../../core/services/api/pizzas.api';
import { CartService } from '../../core/services/cart.service';
import { LoggerService } from '../../core/services/logger.service';
import { of, throwError } from 'rxjs';

describe('MenuPage', () => {
  let component: MenuPage;
  let pizzasApiSpy: jasmine.SpyObj<PizzasApiService>;
  let cartServiceSpy: jasmine.SpyObj<CartService>;
  let loggerServiceSpy: jasmine.SpyObj<LoggerService>;

  beforeEach(() => {
    const apiSpy = jasmine.createSpyObj('PizzasApiService', ['getAll']);
    const cartSpy = jasmine.createSpyObj('CartService', ['add']);
    const logSpy = jasmine.createSpyObj('LoggerService', ['info', 'error']);

    TestBed.configureTestingModule({
      imports: [MenuPage],
      providers: [
        { provide: PizzasApiService, useValue: apiSpy },
        { provide: CartService, useValue: cartSpy },
        { provide: LoggerService, useValue: logSpy }
      ]
    });

    pizzasApiSpy = TestBed.inject(PizzasApiService) as jasmine.SpyObj<PizzasApiService>;
    cartServiceSpy = TestBed.inject(CartService) as jasmine.SpyObj<CartService>;
    loggerServiceSpy = TestBed.inject(LoggerService) as jasmine.SpyObj<LoggerService>;
    
    component = TestBed.createComponent(MenuPage).componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load pizzas on init', () => {
    const mockPizzas = [
      { id: 1, name: 'Margherita', description: 'Classic', price: 8.5, is_available: true }
    ];
    pizzasApiSpy.getAll.and.returnValue(of(mockPizzas));

    component.ngOnInit();

    expect(pizzasApiSpy.getAll).toHaveBeenCalled();
    expect(component.pizzas()).toEqual(mockPizzas);
    expect(component.loading()).toBe(false);
  });

  it('should handle error when loading pizzas', () => {
    pizzasApiSpy.getAll.and.returnValue(throwError(() => new Error('API Error')));

    component.ngOnInit();

    expect(component.error()).toBeTruthy();
    expect(component.loading()).toBe(false);
  });

  it('should add pizza to cart', () => {
    const mockPizza = { id: 1, name: 'Margherita', description: 'Classic', price: 8.5, is_available: true };
    spyOn(window, 'alert');

    component.addToCart(mockPizza);

    expect(cartServiceSpy.add).toHaveBeenCalledWith(mockPizza, 1);
    expect(loggerServiceSpy.info).toHaveBeenCalled();
  });
});
