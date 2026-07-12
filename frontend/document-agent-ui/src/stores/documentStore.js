/**
 * Document Store
 * Simple reactive store for document management state
 */

const initialState = {
  documents: [],
  loading: false,
  error: null,
  currentPage: 1,
  pageSize: 10,
  total: 0,
  stats: null,
};

class DocumentStore {
  documents = initialState.documents;
  loading = initialState.loading;
  error = initialState.error;
  currentPage = initialState.currentPage;
  pageSize = initialState.pageSize;
  total = initialState.total;
  stats = initialState.stats;

  #listeners = new Set();

  subscribe(listener) {
    this.#listeners.add(listener);
    return () => this.#listeners.delete(listener);
  }

  #notifyListeners() {
    this.#listeners.forEach((listener) => listener());
  }

  setDocuments = (documents) => {
    this.documents = documents;
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

  setCurrentPage = (page) => {
    this.currentPage = page;
    this.#notifyListeners();
  };

  setPageSize = (pageSize) => {
    this.pageSize = pageSize;
    this.#notifyListeners();
  };

  setTotal = (total) => {
    this.total = total;
    this.#notifyListeners();
  };

  setStats = (stats) => {
    this.stats = stats;
    this.#notifyListeners();
  };

  reset = () => {
    this.documents = initialState.documents;
    this.loading = initialState.loading;
    this.error = initialState.error;
    this.currentPage = initialState.currentPage;
    this.pageSize = initialState.pageSize;
    this.total = initialState.total;
    this.stats = initialState.stats;
    this.#notifyListeners();
  };
}

export const documentStore = new DocumentStore();
