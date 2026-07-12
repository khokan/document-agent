/**
 * Document Store
 * Zustand store for document management state
 */

interface DocumentState {
  documents: unknown[];
  loading: boolean;
  error: Error | null;
  currentPage: number;
  pageSize: number;
  total: number;
  stats: Record<string, unknown> | null;
}

interface DocumentActions {
  setDocuments: (documents: unknown[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: Error | null) => void;
  setCurrentPage: (page: number) => void;
  setPageSize: (pageSize: number) => void;
  setTotal: (total: number) => void;
  setStats: (stats: Record<string, unknown>) => void;
  reset: () => void;
}

export type DocumentStoreType = DocumentState & DocumentActions;

// Create a simple reactive store
const initialState: DocumentState = {
  documents: [],
  loading: false,
  error: null,
  currentPage: 1,
  pageSize: 10,
  total: 0,
  stats: null,
};

class DocumentStore implements DocumentStoreType {
  documents: unknown[] = initialState.documents;
  loading: boolean = initialState.loading;
  error: Error | null = initialState.error;
  currentPage: number = initialState.currentPage;
  pageSize: number = initialState.pageSize;
  total: number = initialState.total;
  stats: Record<string, unknown> | null = initialState.stats;

  private listeners = new Set<() => void>();

  subscribe(listener: () => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  private notifyListeners(): void {
    this.listeners.forEach((listener) => listener());
  }

  setDocuments = (documents: unknown[]): void => {
    this.documents = documents;
    this.notifyListeners();
  };

  setLoading = (loading: boolean): void => {
    this.loading = loading;
    this.notifyListeners();
  };

  setError = (error: Error | null): void => {
    this.error = error;
    this.notifyListeners();
  };

  setCurrentPage = (page: number): void => {
    this.currentPage = page;
    this.notifyListeners();
  };

  setPageSize = (pageSize: number): void => {
    this.pageSize = pageSize;
    this.notifyListeners();
  };

  setTotal = (total: number): void => {
    this.total = total;
    this.notifyListeners();
  };

  setStats = (stats: Record<string, unknown>): void => {
    this.stats = stats;
    this.notifyListeners();
  };

  reset = (): void => {
    this.documents = initialState.documents;
    this.loading = initialState.loading;
    this.error = initialState.error;
    this.currentPage = initialState.currentPage;
    this.pageSize = initialState.pageSize;
    this.total = initialState.total;
    this.stats = initialState.stats;
    this.notifyListeners();
  };
}

export const documentStore = new DocumentStore();
