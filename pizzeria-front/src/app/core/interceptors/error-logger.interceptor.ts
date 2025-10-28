import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { tap } from 'rxjs';
import { LoggerService } from '../services/logger.service';

export const errorLoggerInterceptor: HttpInterceptorFn = (req, next) => {
  const logger = inject(LoggerService);

  return next(req).pipe(
    tap({
      error: (error) => {
        if (error.status >= 400) {
          logger.error(`HTTP Error: ${error.status} ${error.statusText}`, {
            url: req.url,
            method: req.method,
            error: error.error
          });
        }
      }
    })
  );
};
