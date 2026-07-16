/**
 * useSummarize Hook
 * Custom hook for document summarization
 */

import { useState, useCallback } from 'react';
import { ragAPI } from '../services/api/rag';
import { createLogger } from '../utils';

const logger = createLogger('useSummarize');

export const useSummarize = () => {
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [timing, setTiming] = useState(null);
  const [chunksUsed, setChunksUsed] = useState(0);

  const summarize = useCallback(async (documentId, options = {}) => {
    if (!documentId) return;

    setLoading(true);
    setError(null);
    setSummary('');
    setTiming(null);
    setChunksUsed(0);

    try {
      logger.info('Summarizing document', { documentId });
      const result = await ragAPI.summarize(documentId, options);

      setSummary(result.summary || '');
      setChunksUsed(result.chunks_used || 0);
      setTiming({
        total: result.response_time_ms || 0,
        retrieval: result.retrieval_time_ms || 0,
        generation: result.generation_time_ms || 0,
      });

      logger.info('Document summary completed', {
        summaryLength: (result.summary || '').length,
        chunksUsed: result.chunks_used || 0,
      });

      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Summarization failed');
      setError(error);
      logger.error('Document summarization failed', error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const clear = useCallback(() => {
    setSummary('');
    setTiming(null);
    setChunksUsed(0);
    setError(null);
  }, []);

  return {
    summary,
    loading,
    error,
    timing,
    chunksUsed,
    summarize,
    clear,
  };
};
