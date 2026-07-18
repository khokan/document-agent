/**
 * Configuration
 * Application-wide configuration constants
 */

export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000, // 1 second
};

export const APP_CONFIG = {
  APP_NAME: 'PDF Knowledge Assistant',
  APP_VERSION: '1.0.0',
  LOG_LEVEL: import.meta.env.VITE_LOG_LEVEL || 'info',
};

export const UI_CONFIG = {
  ITEMS_PER_PAGE: 10,
  TOAST_DURATION: 3000,
  ANIMATION_DURATION: 300,
};

export const FILE_CONFIG = {
  MAX_FILE_SIZE: 100 * 1024 * 1024, // 100MB
  MAX_FILES_BATCH: 5,
  ALLOWED_EXTENSIONS: ['.pdf'],
};

export const ENDPOINTS = {
  // Documents
  DOCUMENTS: '/documents',
  DOCUMENTS_LIST: '/documents',
  DOCUMENTS_UPLOAD: '/documents/upload',
  DOCUMENTS_DELETE: (id) => `/documents/${id}`,
  DOCUMENTS_REINDEX: (id) => `/documents/reindex/${id}`,
  DOCUMENTS_STATS: '/documents/stats',
  DOCUMENTS_CLEANUP: '/documents/cleanup',
  DOCUMENTS_HEALTH: '/documents/health',

  // Search
  SEARCH: '/search',

  // RAG
  RAG_QUERY: '/rag/query',
  RAG_CHAT: '/rag/chat',
  RAG_SUMMARIZE: '/rag/summarize',
  RAG_STREAM: '/rag/stream',

  // Conversations
  CONVERSATIONS: '/conversations',
  CONVERSATIONS_GET: (id) => `/conversations/${id}`,
  CONVERSATIONS_UPDATE: (id) => `/conversations/${id}`,
  CONVERSATIONS_DELETE: (id) => `/conversations/${id}`,
  CONVERSATIONS_MESSAGES: (id) => `/conversations/${id}/messages`,

  // Health
  HEALTH: '/health',
};
