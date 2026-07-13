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
  const [error, setError] = useState(null);

  const performSearch = useCallback(async (query) => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      logger.info('Performing search', { query });
      const response = await searchAPI.search(query);
      // Backend returns array directly, not wrapped in object
      let resultsArray = Array.isArray(response) ? response : response.results || [];

      console.log('📊 Raw results from backend:', resultsArray.length, resultsArray);

      // Deduplicate results based on document_id, page, and text content
      const uniqueResults = [];
      const seen = new Set();

      for (const result of resultsArray) {
        const key = `${result.document_id}-${result.page}-${result.text.substring(0, 100)}`;
        if (!seen.has(key)) {
          seen.add(key);
          uniqueResults.push(result);
        }
      }

      console.log(
        '🎯 After deduplication:',
        uniqueResults.length,
        'results (removed',
        resultsArray.length - uniqueResults.length,
        'duplicates)'
      );

      searchStore.setQuery(query);
      searchStore.setResults(uniqueResults);
      searchStore.setSearchTime(response.search_time_ms || 0);
      setResults(uniqueResults);
      logger.info('Search completed', { resultCount: uniqueResults.length });
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
