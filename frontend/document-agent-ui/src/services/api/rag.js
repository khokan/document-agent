/**
 * RAG API Service
 * Handles all RAG-related API calls (query, chat, summarize, stream)
 */

import HttpClient from './client';
import { API_CONFIG, ENDPOINTS } from '../../config';
import { createLogger } from '../../utils';

const logger = createLogger('RAGAPI');
const client = new HttpClient(API_CONFIG.BASE_URL, API_CONFIG.TIMEOUT);

export const ragAPI = {
  /**
   * Perform a RAG query — get answer + sources
   */
  async query(question, options = {}) {
    logger.info('RAG query', { question });
    try {
      const request = {
        question,
        top_k: options.top_k || 5,
        score_threshold: options.score_threshold || null,
        filters: options.filters || null,
      };
      const response = await client.post(ENDPOINTS.RAG_QUERY, request);
      return response;
    } catch (error) {
      logger.error('RAG query failed', error instanceof Error ? error : { error });
      throw error;
    }
  },

  /**
   * Multi-turn chat with RAG context
   */
  async chat(message, history = [], options = {}) {
    logger.info('RAG chat', { message, historyLength: history.length });
    try {
      const request = {
        message,
        history,
        conversation_id: options.conversation_id || null,
        top_k: options.top_k || 5,
        score_threshold: options.score_threshold || null,
        filters: options.filters || null,
      };
      const response = await client.post(ENDPOINTS.RAG_CHAT, request);
      return response;
    } catch (error) {
      logger.error('RAG chat failed', error instanceof Error ? error : { error });
      throw error;
    }
  },

  /**
   * Summarize a document
   */
  async summarize(documentId, options = {}) {
    logger.info('RAG summarize', { documentId });
    try {
      const request = {
        document_id: documentId,
        max_chunks: options.max_chunks || 20,
        filters: options.filters || null,
      };
      const response = await client.post(ENDPOINTS.RAG_SUMMARIZE, request);
      return response;
    } catch (error) {
      logger.error('RAG summarize failed', error instanceof Error ? error : { error });
      throw error;
    }
  },

  /**
   * Stream a RAG response via SSE
   */
  async stream(question, onToken, options = {}) {
    logger.info('RAG stream', { question });
    try {
      const request = {
        question,
        top_k: options.top_k || 5,
        score_threshold: options.score_threshold || null,
        filters: options.filters || null,
      };

      const response = await fetch(`${API_CONFIG.BASE_URL}${ENDPOINTS.RAG_STREAM}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop();

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') {
              return;
            }
            onToken(data);
          }
        }
      }
    } catch (error) {
      logger.error('RAG stream failed', error instanceof Error ? error : { error });
      throw error;
    }
  },
};
