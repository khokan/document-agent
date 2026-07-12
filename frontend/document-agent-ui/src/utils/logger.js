/**
 * Logger Utility
 * Structured logging for browser console logging
 */

class Logger {
  constructor(context) {
    this.context = context;
    this.isDevelopment = import.meta.env.DEV;
  }

  #format(level, message, data) {
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

  debug(message, data) {
    if (this.isDevelopment) {
      this.#format('debug', message, data);
    }
  }

  info(message, data) {
    this.#format('info', message, data);
  }

  warn(message, data) {
    this.#format('warn', message, data);
  }

  error(message, error) {
    if (error instanceof Error) {
      this.#format('error', message, { error: error.message, stack: error.stack });
    } else {
      this.#format('error', message, error);
    }
  }
}

export const createLogger = (context) => new Logger(context);
export default createLogger;
