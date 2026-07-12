/**
 * Search API Service
 * Handles all search-related API calls
 */

import HttpClient from './client';
import { API_CONFIG, ENDPOINTS } from '../../config';
import type { SearchResponse, SearchRequest, GeneratedAnswer } from '../../types';
import { createLogger } from '../../utils';

const logger = createLogger('SearchAPI');
const client = new HttpClient(API_CONFIG.BASE_URL, API_CONFIG.TIMEOUT);

export const searchAPI = {
  /**
   * Perform a semantic search
   */
  async search(query: string, limit: number = 10): Promise<SearchResponse> {
    logger.info('Performing search', { query, limit });
    try {
      const request: SearchRequest = { query, limit };
      return await client.post<SearchResponse>(ENDPOINTS.SEARCH, request);
    } catch (error) {
      logger.error('Search failed', error instanceof Error ? error : { error });
      throw error;
    }
  },

  /**
   * Perform an advanced search with filters
   */
  async advancedSearch(request: SearchRequest): Promise<SearchResponse> {
    logger.info('Performing advanced search', { query: request.query });
    try {
      return await client.post<SearchResponse>(ENDPOINTS.SEARCH_ADVANCED, request);
    } catch (error) {
      logger.error('Advanced search failed', error instanceof Error ? error : { error });
      throw error;
    }
  },

  /**
   * Generate an answer based on search results
   */
  async generateAnswer(query: string): Promise<GeneratedAnswer> {
    logger.info('Generating answer', { query });
    try {
      return await client.post<GeneratedAnswer>(`${ENDPOINTS.SEARCH}/answer`, { query });
    } catch (error) {
      logger.error('Failed to generate answer', error instanceof Error ? error : { error });
      throw error;
    }
  },
};
