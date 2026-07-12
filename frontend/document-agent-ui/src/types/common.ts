/**
 * Common Type Definitions
 * Shared types used across the application
 */

export type AsyncStatus = 'idle' | 'loading' | 'success' | 'error';

export interface LoadingState {
  isLoading: boolean;
  error: Error | null;
  data?: unknown;
}

export interface PaginationState {
  page: number;
  pageSize: number;
  total: number;
}

export interface SortState {
  field: string;
  order: 'asc' | 'desc';
}

export interface ToastNotification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

export interface Theme {
  mode: 'light' | 'dark' | 'auto';
}

export interface SystemStats {
  total_documents: number;
  total_pages: number;
  total_size_mb: number;
  total_searches: number;
  average_search_time_ms: number;
  last_updated: string;
}
