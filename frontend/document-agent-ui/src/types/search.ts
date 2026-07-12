/**
 * Search Type Definitions
 * Defines all search-related types
 */

export interface SearchResult {
  id: string;
  document_id: string;
  document_name: string;
  page_number: number;
  score: number;
  content: string;
  context?: string;
}

export interface SearchResponse {
  query: string;
  results: SearchResult[];
  total_results: number;
  search_time_ms: number;
  timestamp: string;
}

export interface SearchRequest {
  query: string;
  limit?: number;
  document_ids?: string[];
  filters?: SearchFilters;
}

export interface SearchFilters {
  min_score?: number;
  document_ids?: string[];
  date_from?: string;
  date_to?: string;
}

export interface GeneratedAnswer {
  query: string;
  answer: string;
  sources: SourceReference[];
  confidence: number;
  generation_time_ms: number;
}

export interface SourceReference {
  document_id: string;
  document_name: string;
  page_number: number;
  snippet: string;
  score: number;
}

export interface SearchStats {
  total_searches: number;
  average_results: number;
  average_search_time_ms: number;
  most_common_queries: string[];
}
