/**
 * Logger Utility
 * Structured logging using Pino for browser console logging
 */

export type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogContext {
  [key: string]: unknown;
}

class Logger {
  private context: string;
  private isDevelopment: boolean;

  constructor(context: string) {
    this.context = context;
    this.isDevelopment = import.meta.env.DEV;
  }

  private format(level: LogLevel, message: string, data?: LogContext): void {
    const timestamp = new Date().toLocaleTimeString();
    const prefix = `[${timestamp}] [${level.toUpperCase()}] [${this.context}]`;

    const styles = {
      debug: 'color: #888;',
      info: 'color: #2563eb; font-weight: bold;',
      warn: 'color: #f59e0b; font-weight: bold;',
      error: 'color: #ef4444; font-weight: bold;',
    };

    if (data) {
      console.log(`%c${prefix}`, styles[level], message, data);
    } else {
      console.log(`%c${prefix}`, styles[level], message);
    }
  }

  debug(message: string, data?: LogContext): void {
    if (this.isDevelopment) {
      this.format('debug', message, data);
    }
  }

  info(message: string, data?: LogContext): void {
    this.format('info', message, data);
  }

  warn(message: string, data?: LogContext): void {
    this.format('warn', message, data);
  }

  error(message: string, error?: Error | LogContext): void {
    if (error instanceof Error) {
      this.format('error', message, { error: error.message, stack: error.stack });
    } else {
      this.format('error', message, error);
    }
  }
}

export const createLogger = (context: string): Logger => new Logger(context);
export default createLogger;
