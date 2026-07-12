/**
 * useSearch Hook
 * Custom hook for search functionality
 */

import { useState, useCallback } from 'react';
import { searchStore } from '../stores';
import { searchAPI } from '../services/api/health';
import { createLogger } from '../utils';

const logger = createLogger('useSearch');

export const useSearch = () => {
  const [results, setResults] = useState(searchStore.results);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const performSearch = useCallback(async (query: string) => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      logger.info('Performing search', { query });
      const response = await searchAPI.search(query);
      searchStore.setQuery(query);
      searchStore.setResults(response.results);
      searchStore.setSearchTime(response.search_time_ms);
      setResults(response.results);
      logger.info('Search completed', { resultCount: response.results.length });
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Search failed');
      setError(error);
      logger.error('Search failed', error);
    } finally {
      setLoading(false);
    }
  }, []);

  const clearSearch = useCallback(() => {
    searchStore.reset();
    setResults([]);
    setError(null);
  }, []);

  return {
    results,
    loading,
    error,
    performSearch,
    clearSearch,
    query: searchStore.query,
  };
};
