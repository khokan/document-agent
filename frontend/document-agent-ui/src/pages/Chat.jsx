/**
 * Chat Page
 * Multi-turn conversation with RAG context
 */

import { useState, useRef, useEffect } from 'react';
import { Card, CardBody, Button, Input, Spinner } from '../components/ui';
import { useChat } from '../hooks';
import { formatDuration } from '../utils';

export const ChatPage = () => {
  const [input, setInput] = useState('');
  const { messages, loading, error, sendMessage, clearChat } = useChat();
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;
    const msg = input;
    setInput('');
    await sendMessage(msg);
  };

  return (
    <div className="space-y-6 flex flex-col h-[calc(100vh-120px)]">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">Chat</h1>
          <p className="text-gray-600 dark:text-gray-400">Have a conversation with your documents</p>
        </div>
        {messages.length > 0 && (
          <Button variant="outline" onClick={clearChat}>
            Clear Chat
          </Button>
        )}
      </div>

      {/* Messages Area */}
      <Card className="flex-1 overflow-hidden flex flex-col">
        <CardBody className="flex-1 overflow-y-auto space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-16 text-gray-500 dark:text-gray-400">
              <p className="text-4xl mb-4">💬</p>
              <p className="text-lg">Ask anything about your documents</p>
              <p className="text-sm mt-2">The AI will search relevant chunks and answer using them</p>
            </div>
          )}

          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-4 ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>

                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                    <p className="text-xs font-semibold mb-1 opacity-70">Sources:</p>
                    {msg.sources.map((src, i) => (
                      <p key={i} className="text-xs opacity-60">
                        {src.filename} (page {src.page}, score: {(src.score * 100).toFixed(0)}%)
                      </p>
                    ))}
                  </div>
                )}

                {msg.timing && (
                  <p className="text-xs mt-2 opacity-50">
                    {formatDuration(msg.timing.total)}ms
                  </p>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
                <Spinner size="sm" message="Thinking..." />
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </CardBody>
      </Card>

      {/* Input Area */}
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg p-4">
          <p className="text-red-800 dark:text-red-200">{error.message}</p>
        </div>
      )}

      <form onSubmit={handleSend} className="flex gap-4">
        <Input
          type="text"
          placeholder="Ask a question about your documents..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1"
          disabled={loading}
        />
        <Button type="submit" isLoading={loading} disabled={!input.trim()}>
          Send
        </Button>
      </form>
    </div>
  );
};
