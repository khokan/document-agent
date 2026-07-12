/**
 * HTTP Client
 * Fetch-based HTTP client for API communication
 */

class HttpClient {
  constructor(baseURL, timeout = 30000) {
    this.baseURL = baseURL;
    // timeout parameter available for future use with AbortController
    void timeout;
  }

  async get(url, options = {}) {
    const response = await fetch(`${this.baseURL}${url}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(`HTTP ${response.status}: ${error.message || response.statusText}`);
    }

    return response.json();
  }

  async post(url, data, options = {}) {
    const response = await fetch(`${this.baseURL}${url}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      body: data ? JSON.stringify(data) : undefined,
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(`HTTP ${response.status}: ${error.message || response.statusText}`);
    }

    return response.json();
  }

  async delete(url, options = {}) {
    const response = await fetch(`${this.baseURL}${url}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(`HTTP ${response.status}: ${error.message || response.statusText}`);
    }

    return response.json();
  }

  async uploadFile(url, file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseURL}${url}`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(`HTTP ${response.status}: ${error.message || response.statusText}`);
    }

    return response.json();
  }
}

export default HttpClient;
