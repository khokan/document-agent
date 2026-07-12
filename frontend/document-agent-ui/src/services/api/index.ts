/**
 * Health API Service
 * Handles health check and system status
 */

import HttpClient from './client';
import { API_CONFIG, ENDPOINTS } from '../../config';
import type { HealthCheckResponse } from '../../types';
import { createLogger } from '../../utils';

const logger = createLogger('HealthAPI');
const client = new HttpClient(API_CONFIG.BASE_URL, API_CONFIG.TIMEOUT);

export const healthAPI = {
  /**
   * Perform health check
   */
  async check(): Promise<HealthCheckResponse> {
    logger.info('Performing health check');
    try {
      return await client.get<HealthCheckResponse>(ENDPOINTS.HEALTH);
    } catch (error) {
      logger.error('Health check failed', error instanceof Error ? error : { error });
      throw error;
    }
  },
};
