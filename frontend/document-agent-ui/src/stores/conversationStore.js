/**
 * Conversation Store
 * Reactive store for chat conversation state
 */

import { conversationsAPI } from '../services/api/conversations';

class ConversationStore {
  conversations = [];
  activeConversationId = null;
  loading = false;
  error = null;

  #listeners = new Set();

  subscribe(listener) {
    this.#listeners.add(listener);
    return () => this.#listeners.delete(listener);
  }

  #notifyListeners() {
    this.#listeners.forEach((listener) => listener());
  }

  async loadConversations() {
    this.loading = true;
    this.error = null;
    this.#notifyListeners();

    try {
      const response = await conversationsAPI.list();
      this.conversations = response.conversations || [];
    } catch (err) {
      this.error = err;
    } finally {
      this.loading = false;
      this.#notifyListeners();
    }
  }

  async createConversation(title = 'New Chat') {
    try {
      const conv = await conversationsAPI.create(title);
      this.conversations.unshift(conv);
      this.activeConversationId = conv.id;
      this.#notifyListeners();
      return conv;
    } catch (err) {
      this.error = err;
      this.#notifyListeners();
      throw err;
    }
  }

  switchConversation(id) {
    this.activeConversationId = id;
    this.#notifyListeners();
  }

  async deleteConversation(id) {
    try {
      await conversationsAPI.delete(id);
      this.conversations = this.conversations.filter((c) => c.id !== id);
      if (this.activeConversationId === id) {
        this.activeConversationId = this.conversations[0]?.id || null;
      }
      this.#notifyListeners();
    } catch (err) {
      this.error = err;
      this.#notifyListeners();
      throw err;
    }
  }

  async renameConversation(id, title) {
    try {
      const updated = await conversationsAPI.update(id, title);
      const idx = this.conversations.findIndex((c) => c.id === id);
      if (idx !== -1) {
        this.conversations[idx] = { ...this.conversations[idx], ...updated };
      }
      this.#notifyListeners();
    } catch (err) {
      this.error = err;
      this.#notifyListeners();
      throw err;
    }
  }

  updateConversationInList(id, data) {
    const idx = this.conversations.findIndex((c) => c.id === id);
    if (idx !== -1) {
      this.conversations[idx] = { ...this.conversations[idx], ...data };
      this.#notifyListeners();
    }
  }
}

export const conversationStore = new ConversationStore();
