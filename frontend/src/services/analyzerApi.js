import axios from 'axios';

const getApiBaseUrl = () => {
  const envUrl = (import.meta.env.VITE_API_BASE_URL || '').trim().replace(/\/+$/, '');
  if (!envUrl) {
    return '/api';
  }
  return envUrl.endsWith('/api') ? envUrl : `${envUrl}/api`;
};

const API_BASE_URL = getApiBaseUrl();

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
  timeout: 10000,
});

let currentAbortController = null;

export const analyzeCode = async (code) => {
  // Cancel previous pending analysis request to prevent stale overwrite
  if (currentAbortController) {
    currentAbortController.abort();
  }

  currentAbortController = new AbortController();

  try {
    const response = await apiClient.post('/analyze', { code }, {
      signal: currentAbortController.signal,
    });
    return response.data;
  } catch (error) {
    if (axios.isCancel(error)) {
      throw { isCancelled: true };
    }
    if (error.response) {
      // Backend returned HTTP error
      const message = error.response.data?.error || `Server error (${error.response.status})`;
      const err = new Error(message);
      err.response = error.response;
      throw err;
    } else if (error.request) {
      // Network failure
      const err = new Error('Unable to connect to the analyzer. Check that the Flask backend is running.');
      err.isNetworkError = true;
      throw err;
    } else {
      throw new Error(error.message || 'An unexpected error occurred.');
    }
  }
};

export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    return { status: 'down', error: error.message };
  }
};

export default {
  analyzeCode,
  checkHealth,
};
