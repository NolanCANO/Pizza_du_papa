import { HttpInterceptorFn } from '@angular/common/http';
import { environment } from '../../../environments/environment.development';

export const apiBaseInterceptor: HttpInterceptorFn = (req, next) => {
  // Only prepend base URL if the request URL is relative
  if (!req.url.startsWith('http')) {
    const apiReq = req.clone({
      url: `${environment.apiBaseUrl}${req.url}`
    });
    return next(apiReq);
  }
  
  return next(req);
};
