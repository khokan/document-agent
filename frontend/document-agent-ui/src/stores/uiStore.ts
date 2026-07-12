/**
 * UI Store
 * Zustand store for UI state
 */

interface UIState {
  sidebarOpen: boolean;
  darkMode: boolean;
  notifications: Array<{ id: string; type: string; message: string }>;
}

interface UIActions {
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  toggleDarkMode: () => void;
  setDarkMode: (dark: boolean) => void;
  addNotification: (type: string, message: string) => string;
  removeNotification: (id: string) => void;
  clearNotifications: () => void;
}

export type UIStoreType = UIState & UIActions;

const initialState: UIState = {
  sidebarOpen: true,
  darkMode: false,
  notifications: [],
};

class UIStore implements UIStoreType {
  sidebarOpen: boolean = initialState.sidebarOpen;
  darkMode: boolean = initialState.darkMode;
  notifications: Array<{ id: string; type: string; message: string }> = initialState.notifications;

  private listeners = new Set<() => void>();

  constructor() {
    // Load dark mode preference from localStorage
    const saved = localStorage.getItem('darkMode');
    if (saved !== null) {
      this.darkMode = saved === 'true';
    }
  }

  subscribe(listener: () => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  private notifyListeners(): void {
    this.listeners.forEach((listener) => listener());
  }

  toggleSidebar = (): void => {
    this.sidebarOpen = !this.sidebarOpen;
    this.notifyListeners();
  };

  setSidebarOpen = (open: boolean): void => {
    this.sidebarOpen = open;
    this.notifyListeners();
  };

  toggleDarkMode = (): void => {
    this.setDarkMode(!this.darkMode);
  };

  setDarkMode = (dark: boolean): void => {
    this.darkMode = dark;
    localStorage.setItem('darkMode', String(dark));
    this.notifyListeners();
  };

  addNotification = (type: string, message: string): string => {
    const id = `notif-${Date.now()}`;
    this.notifications.push({ id, type, message });
    this.notifyListeners();
    return id;
  };

  removeNotification = (id: string): void => {
    this.notifications = this.notifications.filter((n) => n.id !== id);
    this.notifyListeners();
  };

  clearNotifications = (): void => {
    this.notifications = [];
    this.notifyListeners();
  };
}

export const uiStore = new UIStore();
