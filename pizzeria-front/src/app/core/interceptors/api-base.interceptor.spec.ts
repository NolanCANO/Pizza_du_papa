import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { HttpClient, provideHttpClient, withInterceptors } from '@angular/common/http';
import { apiBaseInterceptor } from './api-base.interceptor';

describe('apiBaseInterceptor', () => {
  let httpMock: HttpTestingController;
  let httpClient: HttpClient;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        provideHttpClient(withInterceptors([apiBaseInterceptor]))
      ]
    });
    
    httpMock = TestBed.inject(HttpTestingController);
    httpClient = TestBed.inject(HttpClient);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should prepend base URL to relative URLs', () => {
    httpClient.get('/pizzas').subscribe();

    const req = httpMock.expectOne('http://localhost:8000/pizzas');
    expect(req.request.url).toBe('http://localhost:8000/pizzas');
    req.flush([]);
  });

  it('should not modify absolute URLs', () => {
    httpClient.get('https://external-api.com/data').subscribe();

    const req = httpMock.expectOne('https://external-api.com/data');
    expect(req.request.url).toBe('https://external-api.com/data');
    req.flush({});
  });
});
