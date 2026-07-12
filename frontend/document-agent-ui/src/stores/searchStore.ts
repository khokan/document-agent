/**
 * Search Store
 * Zustand store for search results and filters
 */

interface SearchResult {
  id: string;
  document_id: string;
  document_name: string;
  page_number: number;
  score: number;
  content: string;
}

interface SearchState {
  query: string;
  results: SearchResult[];
  loading: boolean;
  error: Error | null;
  totalResults: number;
  searchTime: number;
}

interface SearchActions {
  setQuery: (query: string) => void;
  setResults: (results: SearchResult[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: Error | null) => void;
  setTotalResults: (total: number) => void;
  setSearchTime: (time: number) => void;
  reset: () => void;
}

export type SearchStoreType = SearchState & SearchActions;

const initialState: SearchState = {
  query: '',
  results: [],
  loading: false,
  error: null,
  totalResults: 0,
  searchTime: 0,
};

class SearchStore implements SearchStoreType {
  query: string = initialState.query;
  results: SearchResult[] = initialState.results;
  loading: boolean = initialState.loading;
  error: Error | null = initialState.error;
  totalResults: number = initialState.totalResults;
  searchTime: number = initialState.searchTime;

  private listeners = new Set<() => void>();

  subscribe(listener: () => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  private notifyListeners(): void {
    this.listeners.forEach((listener) => listener());
  }

  setQuery = (query: string): void => {
    this.query = query;
    this.notifyListeners();
  };

  setResults = (results: SearchResult[]): void => {
    this.results = results;
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

  setTotalResults = (total: number): void => {
    this.totalResults = total;
    this.notifyListeners();
  };

  setSearchTime = (time: number): void => {
    this.searchTime = time;
    this.notifyListeners();
  };

  reset = (): void => {
    this.query = initialState.query;
    this.results = initialState.results;
    this.loading = initialState.loading;
    this.error = initialState.error;
    this.totalResults = initialState.totalResults;
    this.searchTime = initialState.searchTime;
    this.notifyListeners();
  };
}

export const searchStore = new SearchStore();
