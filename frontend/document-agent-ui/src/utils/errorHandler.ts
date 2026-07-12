/**
 * Error Handler Utility
 * Centralized error handling and transformation
 */

import type { ApiError } from '../types';
import { createLogger } from './logger';

const logger = createLogger('ErrorHandler');

export class AppError extends Error {
  status: number;
  detail?: string | Record<string, string[]>;

  constructor(status: number, message: string, detail?: string | Record<string, string[]>) {
    super(message);
    this.name = 'AppError';
    this.status = status;
    this.detail = detail;
  }
}

export const handleApiError = (error: unknown): AppError => {
  logger.error('API Error occurred', error instanceof Error ? error : { error });

  // Axios error
  if (error && typeof error === 'object' && 'response' in error) {
    const response = (error as Record<string, unknown>).response;
    const status = (response as Record<string, unknown>)?.status || 500;
    const data = (response as Record<string, unknown>)?.data as ApiError;

    return new AppError(status as number, data?.message || 'API request failed', data?.detail);
  }

  // Network error
  if (error && typeof error === 'object' && 'message' in error) {
    const message = (error as Record<string, unknown>).message;
    if (message === 'Network Error') {
      return new AppError(0, 'Network error. Please check your connection.', String(message));
    }
  }

  // Timeout error
  if (error && typeof error === 'object' && 'code' in error) {
    const code = (error as Record<string, unknown>).code;
    if (code === 'ECONNABORTED') {
      return new AppError(0, 'Request timeout. Please try again.', String(code));
    }
  }

  // Generic error
  const message = error instanceof Error ? error.message : 'An unexpected error occurred';
  return new AppError(500, message);
};

export const getErrorMessage = (error: unknown): string => {
  if (error instanceof AppError) {
    return error.message;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unexpected error occurred';
};

export const isNetworkError = (error: unknown): boolean => {
  if (error instanceof AppError) {
    return error.status === 0;
  }
  return false;
};

export const isTimeoutError = (error: unknown): boolean => {
  if (error instanceof AppError) {
    return error.detail === 'ECONNABORTED';
  }
  return false;
};

export const isNotFoundError = (error: unknown): boolean => {
  if (error instanceof AppError) {
    return error.status === 404;
  }
  return false;
};

export const isValidationError = (error: unknown): boolean => {
  if (error instanceof AppError) {
    return error.status === 422 || error.status === 400;
  }
  return false;
};
