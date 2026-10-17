import { apiClient } from './analyzerApi';

export const register = async ({ email, display_name, password }) => {
  try {
    const response = await apiClient.post('/auth/register', {
      email,
      display_name,
      password,
    });
    return response.data;
  } catch (error) {
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error);
    }
    if (error.request) {
      throw new Error('Unable to connect to server. Please ensure the backend is running.');
    }
    throw new Error(error.message || 'Registration failed.');
  }
};

export const login = async ({ email, password }) => {
  try {
    const response = await apiClient.post('/auth/login', {
      email,
      password,
    });
    return response.data;
  } catch (error) {
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error);
    }
    if (error.request) {
      throw new Error('Unable to connect to server. Please ensure the backend is running.');
    }
    throw new Error(error.message || 'Login failed.');
  }
};

export const logout = async () => {
  try {
    const response = await apiClient.post('/auth/logout');
    return response.data;
  } catch (error) {
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error);
    }
    throw new Error(error.message || 'Logout failed.');
  }
};

export const getCurrentUser = async () => {
  try {
    const response = await apiClient.get('/auth/me');
    return response.data?.user || null;
  } catch (error) {
    // 401 simply means unauthenticated (guest)
    if (error.response?.status === 401) {
      return null;
    }
    throw error;
  }
};

export default {
  register,
  login,
  logout,
  getCurrentUser,
};
