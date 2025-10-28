import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { StocksApiService } from './stocks.api';
import { StockItem } from '../../models/stock.model';

describe('StocksApiService', () => {
  let service: StocksApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [StocksApiService]
    });
    service = TestBed.inject(StocksApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('getAll', () => {
    it('should return an array of stock items', () => {
      const mockStocks: StockItem[] = [
        { id: 1, ingredient: 'dough', quantity: 50 },
        { id: 2, ingredient: 'tomato', quantity: 40 },
        { id: 3, ingredient: 'mozzarella', quantity: 60 }
      ];

      service.getAll().subscribe(stocks => {
        expect(stocks).toEqual(mockStocks);
        expect(stocks.length).toBe(3);
      });

      const req = httpMock.expectOne('/stocks');
      expect(req.request.method).toBe('GET');
      req.flush(mockStocks);
    });
  });
});
