/**
 * API Type Definitions
 * Defines all API request/response types for type safety
 */

export interface ApiError {
  status: number;
  message: string;
  detail?: string | Record<string, string[]>;
  timestamp?: string;
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface HealthCheckResponse {
  status: string;
  version: string;
  timestamp: string;
}
