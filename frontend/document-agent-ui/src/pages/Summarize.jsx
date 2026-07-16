/**
 * Summarize Page
 * Document summarization — select a document and get an AI summary
 */

import { useState, useEffect } from 'react';
import { Card, CardBody, Button, Input, Spinner } from '../components/ui';
import { useSummarize, useDocuments } from '../hooks';
import { formatDuration } from '../utils';

export const SummarizePage = () => {
  const [selectedDocId, setSelectedDocId] = useState('');
  const { documents, loading: docsLoading } = useDocuments();
  const { summary, loading, error, timing, chunksUsed, summarize, clear } = useSummarize();

  const handleSummarize = async (e) => {
    e.preventDefault();
    if (!selectedDocId) return;
    await summarize(selectedDocId);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">Summarize</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Generate an AI-powered summary of a document
        </p>
      </div>

      {/* Document Selection */}
      <Card>
        <CardBody>
          <form onSubmit={handleSummarize} className="space-y-4">
            <div className="flex gap-4">
              <select
                value={selectedDocId}
                onChange={(e) => setSelectedDocId(e.target.value)}
                className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={loading || docsLoading}
              >
                <option value="">
                  {docsLoading ? 'Loading documents...' : 'Select a document to summarize'}
                </option>
                {documents.map((doc) => (
                  <option key={doc.document_id} value={doc.document_id}>
                    {doc.filename} ({doc.chunk_count || 0} chunks)
                  </option>
                ))}
              </select>
              <Button type="submit" isLoading={loading} disabled={!selectedDocId}>
                Summarize
              </Button>
              {(summary || error) && (
                <Button variant="outline" onClick={clear}>
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

      {loading && <Spinner size="lg" message="Generating summary..." />}

      {/* Summary */}
      {summary && (
        <Card>
          <CardBody className="space-y-4">
            <div>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Summary</h2>
              <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed">
                {summary}
              </p>
            </div>

            {timing && (
              <div className="flex gap-4 text-sm text-gray-500 dark:text-gray-400 pt-2 border-t border-gray-200 dark:border-gray-700">
                <span>Total: {formatDuration(timing.total)}ms</span>
                <span>Retrieval: {formatDuration(timing.retrieval)}ms</span>
                <span>Generation: {formatDuration(timing.generation)}ms</span>
                <span>Chunks used: {chunksUsed}</span>
              </div>
            )}
          </CardBody>
        </Card>
      )}

      {!loading && !summary && !error && (
        <div className="text-center py-16 text-gray-500 dark:text-gray-400">
          <p className="text-4xl mb-4">📄</p>
          <p className="text-lg">Select a document to generate a summary</p>
          <p className="text-sm mt-2">The AI will analyze the document and provide a comprehensive summary</p>
        </div>
      )}
    </div>
  );
};
