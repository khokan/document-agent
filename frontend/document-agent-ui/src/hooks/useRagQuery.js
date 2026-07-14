/**
 * useRagQuery Hook
 * Custom hook for RAG query functionality
 */

import { useState, useCallback } from 'react';
import { ragAPI } from '../services/api/rag';
import { createLogger } from '../utils';

const logger = createLogger('useRagQuery');

export const useRagQuery = () => {
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [timing, setTiming] = useState(null);

  const ask = useCallback(async (question, options = {}) => {
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    setAnswer('');
    setSources([]);
    setTiming(null);

    try {
      logger.info('Asking question', { question });
      const result = await ragAPI.query(question, options);

      setAnswer(result.answer || '');
      setSources(result.sources || []);
      setTiming({
        total: result.response_time_ms || 0,
        retrieval: result.retrieval_time_ms || 0,
        generation: result.generation_time_ms || 0,
        cached: result.cached || false,
      });

      logger.info('RAG query completed', {
        answerLength: (result.answer || '').length,
        sourceCount: (result.sources || []).length,
      });

      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('RAG query failed');
      setError(error);
      logger.error('RAG query failed', error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const clear = useCallback(() => {
    setAnswer('');
    setSources([]);
    setError(null);
    setTiming(null);
  }, []);

  return {
    answer,
    sources,
    loading,
    error,
    timing,
    ask,
    clear,
  };
};
