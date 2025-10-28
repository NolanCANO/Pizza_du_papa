import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { OrdersApiService } from './orders.api';
import { Order, OrderCreate } from '../../models/order.model';

describe('OrdersApiService', () => {
  let service: OrdersApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [OrdersApiService]
    });
    service = TestBed.inject(OrdersApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('create', () => {
    it('should create an order successfully', () => {
      const orderCreate: OrderCreate = {
        customer_name: 'John Doe',
        delivery_address: '123 Main St',
        items: [{ pizza_id: 1, quantity: 2 }]
      };

      const mockResponse: Order = {
        id: 1,
        customer_name: 'John Doe',
        delivery_address: '123 Main St',
        status: 'PENDING',
        total_price: 17,
        items: [{ pizza_id: 1, quantity: 2, unit_price: 8.5, line_total: 17 }],
        created_at: '2024-01-01T00:00:00'
      };

      service.create(orderCreate).subscribe(order => {
        expect(order).toEqual(mockResponse);
        expect(order.id).toBe(1);
        expect(order.status).toBe('PENDING');
      });

      const req = httpMock.expectOne('/orders');
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual(orderCreate);
      req.flush(mockResponse);
    });

    it('should handle insufficient stock error', () => {
      const orderCreate: OrderCreate = {
        customer_name: 'John Doe',
        delivery_address: '123 Main St',
        items: [{ pizza_id: 1, quantity: 100 }]
      };

      service.create(orderCreate).subscribe(
        () => fail('should have failed with 400 error'),
        (error) => {
          expect(error.status).toBe(400);
          expect(error.error.detail).toContain('stock');
        }
      );

      const req = httpMock.expectOne('/orders');
      req.flush(
        { detail: 'Insufficient stock for ingredient: dough' },
        { status: 400, statusText: 'Bad Request' }
      );
    });
  });

  describe('getById', () => {
    it('should return an order by id', () => {
      const mockOrder: Order = {
        id: 1,
        customer_name: 'John Doe',
        delivery_address: '123 Main St',
        status: 'PREPARING',
        total_price: 17,
        items: [{ pizza_id: 1, quantity: 2, unit_price: 8.5, line_total: 17 }],
        created_at: '2024-01-01T00:00:00'
      };

      service.getById(1).subscribe(order => {
        expect(order).toEqual(mockOrder);
        expect(order.status).toBe('PREPARING');
      });

      const req = httpMock.expectOne('/orders/1');
      expect(req.request.method).toBe('GET');
      req.flush(mockOrder);
    });
  });
});
