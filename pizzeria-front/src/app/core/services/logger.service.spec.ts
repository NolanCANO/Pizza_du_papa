import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { LoggerService } from './logger.service';

describe('LoggerService', () => {
  let service: LoggerService;
  let httpMock: HttpTestingController;
  let consoleSpy: jasmine.Spy;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule]
    });
    service = TestBed.inject(LoggerService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('console logging', () => {
    it('should log debug messages to console', () => {
      consoleSpy = spyOn(console, 'debug');
      
      service.debug('Test debug message');
      
      expect(consoleSpy).toHaveBeenCalled();
      const call = consoleSpy.calls.first();
      expect(call.args[0]).toContain('DEBUG');
      expect(call.args[0]).toContain('Test debug message');
    });

    it('should log info messages to console', () => {
      consoleSpy = spyOn(console, 'info');
      
      service.info('Test info message');
      
      expect(consoleSpy).toHaveBeenCalled();
      const call = consoleSpy.calls.first();
      expect(call.args[0]).toContain('INFO');
      expect(call.args[0]).toContain('Test info message');
    });

    it('should log warn messages to console', () => {
      consoleSpy = spyOn(console, 'warn');
      
      service.warn('Test warn message');
      
      expect(consoleSpy).toHaveBeenCalled();
      const call = consoleSpy.calls.first();
      expect(call.args[0]).toContain('WARN');
      expect(call.args[0]).toContain('Test warn message');
    });

    it('should log error messages to console', () => {
      consoleSpy = spyOn(console, 'error');
      
      service.error('Test error message');
      
      expect(consoleSpy).toHaveBeenCalled();
      const call = consoleSpy.calls.first();
      expect(call.args[0]).toContain('ERROR');
      expect(call.args[0]).toContain('Test error message');
    });

    it('should include context in console logs', () => {
      consoleSpy = spyOn(console, 'info');
      const context = { userId: 123, action: 'checkout' };
      
      service.info('User action', context);
      
      expect(consoleSpy).toHaveBeenCalled();
      const call = consoleSpy.calls.first();
      expect(call.args[1]).toEqual(context);
    });
  });

  describe('remote logging', () => {
    it('should not send to remote when enableRemoteLogs is false', () => {
      spyOn(console, 'info');
      
      service.info('Test message');
      
      httpMock.expectNone('/logs');
    });
  });

  describe('log levels', () => {
    it('should include timestamp in log entry', () => {
      consoleSpy = spyOn(console, 'info');
      
      service.info('Test message');
      
      const call = consoleSpy.calls.first();
      expect(call.args[0]).toMatch(/\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);
    });
  });
});
