import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment.development';

export type LogLevel = 'DEBUG' | 'INFO' | 'WARN' | 'ERROR';

interface LogEntry {
  level: LogLevel;
  message: string;
  timestamp: string;
  context?: any;
}

@Injectable({
  providedIn: 'root'
})
export class LoggerService {
  private readonly logEndpoint = '/logs';

  constructor(private http: HttpClient) {}

  debug(message: string, context?: any): void {
    this.log('DEBUG', message, context);
  }

  info(message: string, context?: any): void {
    this.log('INFO', message, context);
  }

  warn(message: string, context?: any): void {
    this.log('WARN', message, context);
  }

  error(message: string, context?: any): void {
    this.log('ERROR', message, context);
  }

  private log(level: LogLevel, message: string, context?: any): void {
    const entry: LogEntry = {
      level,
      message,
      timestamp: new Date().toISOString(),
      context
    };

    // Always log to console
    this.logToConsole(entry);

    // Optionally send to remote if enabled
    if (environment.enableRemoteLogs && this.shouldLog(level)) {
      this.sendToRemote(entry);
    }
  }

  private logToConsole(entry: LogEntry): void {
    const logMessage = `[${entry.timestamp}] ${entry.level}: ${entry.message}`;
    
    switch (entry.level) {
      case 'DEBUG':
        console.debug(logMessage, entry.context);
        break;
      case 'INFO':
        console.info(logMessage, entry.context);
        break;
      case 'WARN':
        console.warn(logMessage, entry.context);
        break;
      case 'ERROR':
        console.error(logMessage, entry.context);
        break;
    }
  }

  private sendToRemote(entry: LogEntry): void {
    // Non-blocking - fire and forget
    this.http.post(this.logEndpoint, entry).subscribe({
      error: (err) => {
        // Silently fail if remote logging is unavailable
        console.debug('Remote logging failed', err);
      }
    });
  }

  private shouldLog(level: LogLevel): boolean {
    const levels: LogLevel[] = ['DEBUG', 'INFO', 'WARN', 'ERROR'];
    const configLevel = environment.logLevel;
    
    return levels.indexOf(level) >= levels.indexOf(configLevel);
  }
}
