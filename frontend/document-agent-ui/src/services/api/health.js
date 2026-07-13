/**
 * Search API Service
 * Handles all search-related API calls
 */

import HttpClient from './client';
import { API_CONFIG, ENDPOINTS } from '../../config';
import { createLogger } from '../../utils';

const logger = createLogger('SearchAPI');
const client = new HttpClient(API_CONFIG.BASE_URL, API_CONFIG.TIMEOUT);

export const searchAPI = {
  /**
   * Perform a semantic search
   */
  async search(query, limit = 10) {
    logger.info('Performing search', { query, limit });
    try {
      const request = { question: query, top_k: limit };
      console.log('🔍 Search request payload:', JSON.stringify(request));
      const response = await client.post(ENDPOINTS.SEARCH, request);
      console.log('✅ Search response:', response);
      return response;
    } catch (error) {
      console.error('❌ Search error:', error);
      logger.error('Search failed', error instanceof Error ? error : { error });
      throw error;
    }
  },

  /**
   * Perform an advanced search with filters
   */
  async advancedSearch(request) {
    logger.info('Performing advanced search', { query: request.query });
    try {
      return await client.post(ENDPOINTS.SEARCH_ADVANCED, request);
    } catch (error) {
      logger.error('Advanced search failed', error instanceof Error ? error : { error });
      throw error;
    }
  },

  /**
   * Generate an answer based on search results
   */
  async generateAnswer(query) {
    logger.info('Generating answer', { query });
    try {
      return await client.post(`${ENDPOINTS.SEARCH}/answer`, { query });
    } catch (error) {
      logger.error('Failed to generate answer', error instanceof Error ? error : { error });
      throw error;
    }
  },
};
