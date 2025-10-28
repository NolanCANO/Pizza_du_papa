import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { HttpClient, provideHttpClient, withInterceptors } from '@angular/common/http';
import { errorLoggerInterceptor } from './error-logger.interceptor';
import { LoggerService } from '../services/logger.service';

describe('errorLoggerInterceptor', () => {
  let httpMock: HttpTestingController;
  let httpClient: HttpClient;
  let loggerService: LoggerService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        LoggerService,
        provideHttpClient(withInterceptors([errorLoggerInterceptor]))
      ]
    });
    
    httpMock = TestBed.inject(HttpTestingController);
    httpClient = TestBed.inject(HttpClient);
    loggerService = TestBed.inject(LoggerService);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should log 4xx errors', () => {
    const loggerSpy = spyOn(loggerService, 'error');

    httpClient.get('/test').subscribe({
      error: () => {}
    });

    const req = httpMock.expectOne('/test');
    req.flush({ detail: 'Not found' }, { status: 404, statusText: 'Not Found' });

    expect(loggerSpy).toHaveBeenCalledWith(
      jasmine.stringContaining('404'),
      jasmine.objectContaining({ url: '/test', method: 'GET' })
    );
  });

  it('should log 5xx errors', () => {
    const loggerSpy = spyOn(loggerService, 'error');

    httpClient.get('/test').subscribe({
      error: () => {}
    });

    const req = httpMock.expectOne('/test');
    req.flush('Server error', { status: 500, statusText: 'Internal Server Error' });

    expect(loggerSpy).toHaveBeenCalled();
  });

  it('should not log successful responses', () => {
    const loggerSpy = spyOn(loggerService, 'error');

    httpClient.get('/test').subscribe();

    const req = httpMock.expectOne('/test');
    req.flush({ data: 'success' });

    expect(loggerSpy).not.toHaveBeenCalled();
  });
});
