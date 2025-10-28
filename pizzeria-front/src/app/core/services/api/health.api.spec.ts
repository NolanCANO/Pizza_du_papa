import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { HealthApiService } from './health.api';

describe('HealthApiService', () => {
  let service: HealthApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [HealthApiService]
    });
    service = TestBed.inject(HealthApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('check', () => {
    it('should return health status', () => {
      const mockResponse = { status: 'ok' };

      service.check().subscribe(response => {
        expect(response).toEqual(mockResponse);
        expect(response.status).toBe('ok');
      });

      const req = httpMock.expectOne('/health');
      expect(req.request.method).toBe('GET');
      req.flush(mockResponse);
    });

    it('should handle API down error', () => {
      service.check().subscribe(
        () => fail('should have failed'),
        (error) => {
          expect(error.status).toBe(503);
        }
      );

      const req = httpMock.expectOne('/health');
      req.flush('Service unavailable', { status: 503, statusText: 'Service Unavailable' });
    });
  });
});
