/**
 * Conversations API Service
 * Handles conversation CRUD and message retrieval
 */

import HttpClient from './client';
import { API_CONFIG, ENDPOINTS } from '../../config';
import { createLogger } from '../../utils';

const logger = createLogger('ConversationsAPI');
const client = new HttpClient(API_CONFIG.BASE_URL, API_CONFIG.TIMEOUT);

export const conversationsAPI = {
  async list(limit = 50, offset = 0) {
    logger.info('List conversations');
    try {
      const response = await client.get(
        `${ENDPOINTS.CONVERSATIONS}?limit=${limit}&offset=${offset}`
      );
      return response;
    } catch (error) {
      logger.error('List conversations failed', error);
      throw error;
    }
  },

  async create(title = 'New Chat') {
    logger.info('Create conversation', { title });
    try {
      const response = await client.post(ENDPOINTS.CONVERSATIONS, { title });
      return response;
    } catch (error) {
      logger.error('Create conversation failed', error);
      throw error;
    }
  },

  async get(id) {
    logger.info('Get conversation', { id });
    try {
      const response = await client.get(ENDPOINTS.CONVERSATIONS_GET(id));
      return response;
    } catch (error) {
      logger.error('Get conversation failed', error);
      throw error;
    }
  },

  async update(id, title) {
    logger.info('Update conversation', { id, title });
    try {
      const response = await client.patch(ENDPOINTS.CONVERSATIONS_UPDATE(id), { title });
      return response;
    } catch (error) {
      logger.error('Update conversation failed', error);
      throw error;
    }
  },

  async delete(id) {
    logger.info('Delete conversation', { id });
    try {
      await client.delete(ENDPOINTS.CONVERSATIONS_DELETE(id));
    } catch (error) {
      logger.error('Delete conversation failed', error);
      throw error;
    }
  },

  async getMessages(id, limit = 100, offset = 0) {
    logger.info('Get conversation messages', { id });
    try {
      const response = await client.get(
        `${ENDPOINTS.CONVERSATIONS_MESSAGES(id)}?limit=${limit}&offset=${offset}`
      );
      return response;
    } catch (error) {
      logger.error('Get messages failed', error);
      throw error;
    }
  },
};
