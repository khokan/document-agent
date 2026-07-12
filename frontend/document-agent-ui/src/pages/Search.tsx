/**
 * Search Page
 * Page for searching documents
 */

import React, { useState } from 'react';
import { Card, CardBody, Button, Input, Spinner } from '../components/ui';
import { useSearch } from '../hooks';
import { formatDuration } from '../utils';

export const SearchPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const { results, loading, error, performSearch, clearSearch } = useSearch();

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      await performSearch(query);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">Search</h1>
        <p className="text-gray-600 dark:text-gray-400">Search your PDF documents</p>
      </div>

      <Card>
        <CardBody>
          <form onSubmit={handleSearch} className="space-y-4">
            <div className="flex gap-4">
              <Input
                type="text"
                placeholder="Enter your search query..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="flex-1"
              />
              <Button type="submit" isLoading={loading}>
                🔍 Search
              </Button>
              {results.length > 0 && (
                <Button variant="outline" onClick={clearSearch}>
                  Clear
                </Button>
              )}
            </div>
          </form>
        </CardBody>
      </Card>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg p-4">
          <p className="text-red-800 dark:text-red-200">{error.message}</p>
        </div>
      )}

      {loading && <Spinner size="lg" message="Searching documents..." />}

      {results.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Found {results.length} results
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">Search completed in {formatDuration(0)}ms</p>
          </div>

          <div className="space-y-3">
            {results.map((result) => (
              <Card key={result.id}>
                <CardBody className="space-y-2">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 dark:text-white">{result.document_name}</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        📄 Page {result.page_number} • Score: {(result.score * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">{result.content}</p>
                </CardBody>
              </Card>
            ))}
          </div>
        </div>
      )}

      {!loading && results.length === 0 && query && (
        <div className="text-center py-8 text-gray-500 dark:text-gray-400">
          <p className="text-lg">No results found for "{query}"</p>
          <p className="text-sm">Try using different keywords</p>
        </div>
      )}

      {!loading && results.length === 0 && !query && (
        <div className="text-center py-8 text-gray-500 dark:text-gray-400">
          <p className="text-lg">Enter a search query to get started</p>
        </div>
      )}
    </div>
  );
};
