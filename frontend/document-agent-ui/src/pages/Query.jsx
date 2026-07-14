/**
 * Query Page
 * RAG query — ask a question and get an answer with sources
 */

import { useState } from 'react';
import { Card, CardBody, Button, Input, Spinner } from '../components/ui';
import { useRagQuery } from '../hooks';
import { formatDuration } from '../utils';

export const QueryPage = () => {
  const [question, setQuestion] = useState('');
  const { answer, sources, loading, error, timing, ask, clear } = useRagQuery();

  const handleAsk = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    await ask(question);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">Ask a Question</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Get AI-powered answers with source citations from your documents
        </p>
      </div>

      {/* Question Input */}
      <Card>
        <CardBody>
          <form onSubmit={handleAsk} className="space-y-4">
            <div className="flex gap-4">
              <Input
                type="text"
                placeholder="Ask a question about your documents..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="flex-1"
              />
              <Button type="submit" isLoading={loading}>
                Ask
              </Button>
              {(answer || error) && (
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

      {loading && <Spinner size="lg" message="Searching and generating answer..." />}

      {/* Answer */}
      {answer && (
        <Card>
          <CardBody className="space-y-4">
            <div>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Answer</h2>
              <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed">
                {answer}
              </p>
            </div>

            {timing && (
              <div className="flex gap-4 text-sm text-gray-500 dark:text-gray-400 pt-2 border-t border-gray-200 dark:border-gray-700">
                <span>Total: {formatDuration(timing.total)}ms</span>
                <span>Retrieval: {formatDuration(timing.retrieval)}ms</span>
                <span>Generation: {formatDuration(timing.generation)}ms</span>
                {timing.cached && <span className="text-green-600">Cached</span>}
              </div>
            )}
          </CardBody>
        </Card>
      )}

      {/* Sources */}
      {sources && sources.length > 0 && (
        <Card>
          <CardBody className="space-y-3">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              Sources ({sources.length})
            </h2>
            <div className="space-y-3">
              {sources.map((src, index) => (
                <div
                  key={index}
                  className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-semibold text-gray-900 dark:text-white text-sm">
                      {src.filename}
                    </span>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      Page {src.page} | Score: {(src.score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
                    {src.text}
                  </p>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>
      )}

      {!loading && !answer && !error && (
        <div className="text-center py-16 text-gray-500 dark:text-gray-400">
          <p className="text-4xl mb-4">🤖</p>
          <p className="text-lg">Ask a question to get started</p>
          <p className="text-sm mt-2">The AI will search your documents and provide an answer with citations</p>
        </div>
      )}
    </div>
  );
};
