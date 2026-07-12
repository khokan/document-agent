/**
 * UI Store
 * Simple reactive store for UI state
 */

const initialState = {
  sidebarOpen: true,
  darkMode: false,
  notifications: [],
};

class UIStore {
  sidebarOpen = initialState.sidebarOpen;
  darkMode = initialState.darkMode;
  notifications = initialState.notifications;

  #listeners = new Set();

  constructor() {
    // Load dark mode preference from localStorage
    const saved = localStorage.getItem('darkMode');
    if (saved !== null) {
      this.darkMode = saved === 'true';
    }
  }

  subscribe(listener) {
    this.#listeners.add(listener);
    return () => this.#listeners.delete(listener);
  }

  #notifyListeners() {
    this.#listeners.forEach((listener) => listener());
  }

  toggleSidebar = () => {
    this.sidebarOpen = !this.sidebarOpen;
    this.#notifyListeners();
  };

  setSidebarOpen = (open) => {
    this.sidebarOpen = open;
    this.#notifyListeners();
  };

  toggleDarkMode = () => {
    this.setDarkMode(!this.darkMode);
  };

  setDarkMode = (dark) => {
    this.darkMode = dark;
    localStorage.setItem('darkMode', String(dark));
    this.#notifyListeners();
  };

  addNotification = (type, message) => {
    const id = `notif-${Date.now()}`;
    this.notifications.push({ id, type, message });
    this.#notifyListeners();
    return id;
  };

  removeNotification = (id) => {
    this.notifications = this.notifications.filter((n) => n.id !== id);
    this.#notifyListeners();
  };

  clearNotifications = () => {
    this.notifications = [];
    this.#notifyListeners();
  };
}

export const uiStore = new UIStore();
