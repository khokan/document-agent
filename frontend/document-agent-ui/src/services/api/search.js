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
  async search(query, limit = 5) {
    logger.info('Performing search', { query, limit });
    try {
      const request = { question: query, top_k: limit };
      const response = await client.post(ENDPOINTS.SEARCH, request);
      return response;
    } catch (error) {
      logger.error('Search failed', error instanceof Error ? error : { error });
      throw error;
    }
  },
};
