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
    const fullUrl = `${this.baseURL}${url}`;
    console.log('📤 POST Request:', { url, fullUrl, data, options });

    const response = await fetch(fullUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      body: data ? JSON.stringify(data) : undefined,
      ...options,
    });

    console.log('📥 POST Response:', {
      status: response.status,
      statusText: response.statusText,
      ok: response.ok,
    });

    if (!response.ok) {
      let errorData = {};
      try {
        errorData = await response.json();
        console.error('❌ Error response body:', errorData);
        if (errorData.detail && Array.isArray(errorData.detail)) {
          console.error(
            '❌ Validation errors:',
            errorData.detail.map((e) => `${e.loc?.join('.')} - ${e.msg}`).join(', ')
          );
        }
      } catch {
        console.error('❌ Could not parse error response');
      }
      throw new Error(`HTTP ${response.status}: ${errorData.message || response.statusText}`);
    }

    return response.json();
  }

	async delete(url, options = {}) {
		const fullUrl = `${this.baseURL}${url}`;
		console.log('🗑️ DELETE Request:', { url, fullUrl, options });
		
		const response = await fetch(fullUrl, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
				...(options.headers || {}),
			},
			...options,
		});

		console.log('📥 DELETE Response:', { status: response.status, statusText: response.statusText, ok: response.ok });

		if (!response.ok) {
			let errorData = {};
			try {
				errorData = await response.json();
				console.error('❌ Error response body:', errorData);
			} catch {
				console.error('❌ Could not parse error response');
			}
			throw new Error(`HTTP ${response.status}: ${errorData.message || response.statusText}`);
		}

		return response.json();
	}

  async patch(url, data, options = {}) {
    const fullUrl = `${this.baseURL}${url}`;
    const response = await fetch(fullUrl, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      body: data ? JSON.stringify(data) : undefined,
      ...options,
    });

    if (!response.ok) {
      let errorData = {};
      try {
        errorData = await response.json();
      } catch {
        // ignore
      }
      throw new Error(`HTTP ${response.status}: ${errorData.message || response.statusText}`);
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
