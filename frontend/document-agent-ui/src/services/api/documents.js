/**
 * Document API Service
 * Handles all document-related API calls
 */

import HttpClient from './client';
import { API_CONFIG, ENDPOINTS } from '../../config';
import { createLogger } from '../../utils';

const logger = createLogger('DocumentAPI');
const client = new HttpClient(API_CONFIG.BASE_URL, API_CONFIG.TIMEOUT);

export const documentAPI = {
  /**
   * Fetch all documents with pagination
   */
  async list(page = 1, pageSize = 10) {
    logger.info('Fetching document list', { page, pageSize });
    try {
      const url = `${ENDPOINTS.DOCUMENTS_LIST}?page=${page}&page_size=${pageSize}`;
      return await client.get(url);
    } catch (error) {
      logger.error('Failed to fetch documents', error instanceof Error ? error : { error });
      throw error;
    }
  },

  /**
   * Upload a single PDF file
   */
  async upload(file) {
    logger.info('Uploading document', { filename: file.name, size: file.size });
    try {
      return await client.uploadFile(ENDPOINTS.DOCUMENTS_UPLOAD, file);
    } catch (error) {
      logger.error('Failed to upload document', error instanceof Error ? error : { error });
      throw error;
    }
  },

  /**
   * Upload multiple PDF files
   */
  async uploadBatch(files) {
    logger.info('Uploading batch of documents', { count: files.length });
    try {
      return Promise.all(files.map((file) => this.upload(file)));
    } catch (error) {
      logger.error('Failed to upload batch', error instanceof Error ? error : { error });
      throw error;
    }
  },

  /**
   * Delete a document by ID
   */
  async delete(documentId) {
    logger.info('Deleting document', { documentId });
    try {
      return await client.delete(ENDPOINTS.DOCUMENTS_DELETE(documentId));
    } catch (error) {
      logger.error('Failed to delete document', error instanceof Error ? error : { error });
      throw error;
    }
  },

  /**
   * Get document statistics
   */
  async getStats() {
    logger.info('Fetching document statistics');
    try {
      return await client.get(ENDPOINTS.DOCUMENTS_STATS);
    } catch (error) {
      logger.error('Failed to fetch statistics', error instanceof Error ? error : { error });
      throw error;
    }
  },

  /**
   * Get a single document by ID
   */
  async getById(documentId) {
    logger.info('Fetching document', { documentId });
    try {
      return await client.get(`${ENDPOINTS.DOCUMENTS}/${documentId}`);
    } catch (error) {
      logger.error('Failed to fetch document', error instanceof Error ? error : { error });
      throw error;
    }
  },
};
