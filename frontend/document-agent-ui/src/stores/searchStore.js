/**
 * Search Store
 * Simple reactive store for search results and filters
 */

const initialState = {
  query: '',
  results: [],
  loading: false,
  error: null,
  totalResults: 0,
  searchTime: 0,
};

class SearchStore {
  query = initialState.query;
  results = initialState.results;
  loading = initialState.loading;
  error = initialState.error;
  totalResults = initialState.totalResults;
  searchTime = initialState.searchTime;

  #listeners = new Set();

  subscribe(listener) {
    this.#listeners.add(listener);
    return () => this.#listeners.delete(listener);
  }

  #notifyListeners() {
    this.#listeners.forEach((listener) => listener());
  }

  setQuery = (query) => {
    this.query = query;
    this.#notifyListeners();
  };

  setResults = (results) => {
    this.results = results;
    this.#notifyListeners();
  };

  setLoading = (loading) => {
    this.loading = loading;
    this.#notifyListeners();
  };

  setError = (error) => {
    this.error = error;
    this.#notifyListeners();
  };

  setTotalResults = (total) => {
    this.totalResults = total;
    this.#notifyListeners();
  };

  setSearchTime = (time) => {
    this.searchTime = time;
    this.#notifyListeners();
  };

  reset = () => {
    this.query = initialState.query;
    this.results = initialState.results;
    this.loading = initialState.loading;
    this.error = initialState.error;
    this.totalResults = initialState.totalResults;
    this.searchTime = initialState.searchTime;
    this.#notifyListeners();
  };
}

export const searchStore = new SearchStore();
