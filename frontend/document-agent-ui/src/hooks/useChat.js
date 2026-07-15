/**
 * useChat Hook
 * Custom hook for multi-turn chat functionality with conversation persistence
 */

import { useState, useCallback, useEffect } from 'react';
import { ragAPI } from '../services/api/rag';
import { conversationsAPI } from '../services/api/conversations';
import { conversationStore } from '../stores/conversationStore';
import { createLogger } from '../utils';

const logger = createLogger('useChat');

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load messages when conversationId changes
  useEffect(() => {
    if (conversationId) {
      loadConversationMessages(conversationId);
    } else {
      setMessages([]);
    }
  }, [conversationId]);

  const loadConversationMessages = useCallback(async (id) => {
    try {
      const response = await conversationsAPI.getMessages(id);
      const loadedMessages = (response.messages || []).map((m) => ({
        role: m.role,
        content: m.content,
        sources: m.sources || [],
      }));
      setMessages(loadedMessages);
    } catch (err) {
      logger.error('Failed to load conversation messages', err);
      setMessages([]);
    }
  }, []);

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

      const result = await ragAPI.chat(message, history, {
        ...options,
        conversation_id: conversationId,
      });

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

      // Store conversation_id from response (for new conversations)
      if (result.conversation_id) {
        if (!conversationId) {
          setConversationId(result.conversation_id);
          // Reload conversation list to show new conversation
          conversationStore.loadConversations();
        } else {
          // Update the conversation's updated_at in the list
          conversationStore.updateConversationInList(conversationId, {
            updated_at: new Date().toISOString(),
          });
        }
      }

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
  }, [messages, conversationId]);

  const createNewConversation = useCallback(() => {
    setConversationId(null);
    setMessages([]);
    setError(null);
  }, []);

  const setActiveConversation = useCallback((id) => {
    setConversationId(id);
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    conversationId,
    loading,
    error,
    sendMessage,
    createNewConversation,
    setActiveConversation,
    loadConversationMessages,
  };
};
