/**
 * HTTP Client
 * Axios instance with interceptors for API communication
 */

class HttpClient {
  private baseURL: string;

  constructor(baseURL: string, timeout: number = 30000) {
    this.baseURL = baseURL;
    // timeout parameter available for future use with AbortController
    void timeout;
  }

  async get<T>(url: string, options?: Record<string, unknown>): Promise<T> {
    const response = await fetch(`${this.baseURL}${url}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...((options?.headers as Record<string, string>) || {}),
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(`HTTP ${response.status}: ${error.message || response.statusText}`);
    }

    return response.json() as Promise<T>;
  }

  async post<T>(url: string, data?: unknown, options?: Record<string, unknown>): Promise<T> {
    const response = await fetch(`${this.baseURL}${url}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...((options?.headers as Record<string, string>) || {}),
      },
      body: data ? JSON.stringify(data) : undefined,
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(`HTTP ${response.status}: ${error.message || response.statusText}`);
    }

    return response.json() as Promise<T>;
  }

  async delete<T>(url: string, options?: Record<string, unknown>): Promise<T> {
    const response = await fetch(`${this.baseURL}${url}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...((options?.headers as Record<string, string>) || {}),
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(`HTTP ${response.status}: ${error.message || response.statusText}`);
    }

    return response.json() as Promise<T>;
  }

  async uploadFile<T>(url: string, file: File): Promise<T> {
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

    return response.json() as Promise<T>;
  }
}

export default HttpClient;
