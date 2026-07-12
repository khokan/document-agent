/**
 * Error Handler Utility
 * Centralized error handling and transformation
 */

import { createLogger } from './logger';

const logger = createLogger('ErrorHandler');

export class AppError extends Error {
  constructor(status, message, detail) {
    super(message);
    this.name = 'AppError';
    this.status = status;
    this.detail = detail;
  }
}

export const handleApiError = (error) => {
  logger.error('API Error occurred', error instanceof Error ? error : { error });

  // Axios error
  if (error && typeof error === 'object' && 'response' in error) {
    const response = error.response;
    const status = response?.status || 500;
    const data = response?.data;

    return new AppError(status, data?.message || 'API request failed', data?.detail);
  }

  // Network error
  if (error && typeof error === 'object' && 'message' in error) {
    if (error.message === 'Network Error') {
      return new AppError(0, 'Network error. Please check your connection.', error.message);
    }
  }

  // Timeout error
  if (error && typeof error === 'object' && 'code' in error) {
    if (error.code === 'ECONNABORTED') {
      return new AppError(0, 'Request timeout. Please try again.', error.code);
    }
  }

  // Generic error
  const message = error instanceof Error ? error.message : 'An unexpected error occurred';
  return new AppError(500, message);
};

export const getErrorMessage = (error) => {
  if (error instanceof AppError) {
    return error.message;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unexpected error occurred';
};

export const isNetworkError = (error) => {
  if (error instanceof AppError) {
    return error.status === 0;
  }
  return false;
};

export const isTimeoutError = (error) => {
  if (error instanceof AppError) {
    return error.detail === 'ECONNABORTED';
  }
  return false;
};

export const isNotFoundError = (error) => {
  if (error instanceof AppError) {
    return error.status === 404;
  }
  return false;
};

export const isValidationError = (error) => {
  if (error instanceof AppError) {
    return error.status === 422 || error.status === 400;
  }
  return false;
};
