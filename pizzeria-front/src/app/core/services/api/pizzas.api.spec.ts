import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { PizzasApiService } from './pizzas.api';
import { Pizza } from '../../models/pizza.model';
import { environment } from '../../../../environments/environment.development';

describe('PizzasApiService', () => {
  let service: PizzasApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [PizzasApiService]
    });
    service = TestBed.inject(PizzasApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('getAll', () => {
    it('should return an array of pizzas', () => {
      const mockPizzas: Pizza[] = [
        { id: 1, name: 'Margherita', description: 'Classic', price: 8.5, is_available: true },
        { id: 2, name: 'Pepperoni', description: 'Spicy', price: 10, is_available: true }
      ];

      service.getAll().subscribe(pizzas => {
        expect(pizzas).toEqual(mockPizzas);
        expect(pizzas.length).toBe(2);
      });

      const req = httpMock.expectOne('/pizzas');
      expect(req.request.method).toBe('GET');
      req.flush(mockPizzas);
    });

    it('should handle empty array response', () => {
      service.getAll().subscribe(pizzas => {
        expect(pizzas).toEqual([]);
        expect(pizzas.length).toBe(0);
      });

      const req = httpMock.expectOne('/pizzas');
      req.flush([]);
    });
  });

  describe('getById', () => {
    it('should return a single pizza', () => {
      const mockPizza: Pizza = {
        id: 1,
        name: 'Margherita',
        description: 'Classic',
        price: 8.5,
        is_available: true
      };

      service.getById(1).subscribe(pizza => {
        expect(pizza).toEqual(mockPizza);
        expect(pizza.id).toBe(1);
      });

      const req = httpMock.expectOne('/pizzas/1');
      expect(req.request.method).toBe('GET');
      req.flush(mockPizza);
    });

    it('should handle 404 error', () => {
      service.getById(999).subscribe(
        () => fail('should have failed with 404 error'),
        (error) => {
          expect(error.status).toBe(404);
        }
      );

      const req = httpMock.expectOne('/pizzas/999');
      req.flush('Not found', { status: 404, statusText: 'Not Found' });
    });
  });
});
