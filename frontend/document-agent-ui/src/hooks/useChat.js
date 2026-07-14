/**
 * useChat Hook
 * Custom hook for multi-turn chat functionality
 */

import { useState, useCallback } from 'react';
import { ragAPI } from '../services/api/rag';
import { createLogger } from '../utils';

const logger = createLogger('useChat');

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = useCallback(async (message, options = {}) => {
    if (!message.trim()) return;

    const userMessage = { role: 'user', content: message };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    setError(null);

    try {
      logger.info('Sending chat message', { message });

      // Build history from previous messages
      const history = messages.map((msg) => ({
        role: msg.role,
        content: msg.content,
      }));

      const result = await ragAPI.chat(message, history, options);

      const assistantMessage = {
        role: 'assistant',
        content: result.answer || '',
        sources: result.sources || [],
        timing: {
          total: result.response_time_ms || 0,
          retrieval: result.retrieval_time_ms || 0,
          generation: result.generation_time_ms || 0,
        },
      };

      setMessages((prev) => [...prev, assistantMessage]);

      logger.info('Chat response received', {
        answerLength: (result.answer || '').length,
        sourceCount: (result.sources || []).length,
      });

      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Chat failed');
      setError(error);
      logger.error('Chat failed', error);

      // Add error message to conversation
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Sorry, an error occurred while processing your message.' },
      ]);

      throw error;
    } finally {
      setLoading(false);
    }
  }, [messages]);

  const clearChat = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    loading,
    error,
    sendMessage,
    clearChat,
  };
};
