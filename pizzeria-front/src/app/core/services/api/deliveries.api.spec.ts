import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { DeliveriesApiService } from './deliveries.api';
import { Delivery } from '../../models/delivery.model';

describe('DeliveriesApiService', () => {
  let service: DeliveriesApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [DeliveriesApiService]
    });
    service = TestBed.inject(DeliveriesApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('getById', () => {
    it('should return a delivery by id', () => {
      const mockDelivery: Delivery = {
        id: 1,
        order_id: 1,
        assigned_driver: 'Pierre Martin',
        status: 'PICKED_UP',
        eta_minutes: 25,
        created_at: '2024-01-01T00:00:00'
      };

      service.getById(1).subscribe(delivery => {
        expect(delivery).toEqual(mockDelivery);
        expect(delivery.status).toBe('PICKED_UP');
      });

      const req = httpMock.expectOne('/deliveries/1');
      expect(req.request.method).toBe('GET');
      req.flush(mockDelivery);
    });

    it('should handle 404 when delivery not found', () => {
      service.getById(999).subscribe(
        () => fail('should have failed with 404 error'),
        (error) => {
          expect(error.status).toBe(404);
        }
      );

      const req = httpMock.expectOne('/deliveries/999');
      req.flush('Not found', { status: 404, statusText: 'Not Found' });
    });
  });
});
