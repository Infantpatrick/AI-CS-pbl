import { api } from './client';

export const register = async (name, email, password) => {
  try {
    const res = await api.post('/auth/register', { name, email, password });
    return { success: true, data: res.data };
  } catch (error) {
    let errorMsg = 'Unable to reach the PhishGuard AI server.';
    if (error.response) {
      const status = error.response.status;
      if (status === 401) errorMsg = 'Invalid email or password.';
      else if (status === 409) errorMsg = 'An account with this email already exists.';
      else if (status === 422) errorMsg = 'Please check the entered information.';
      else if (status >= 500) errorMsg = 'Authentication server error. Please try again.';
      else errorMsg = error.response.data?.detail || 'An unexpected error occurred.';
    }
    return { success: false, error: errorMsg };
  }
};

export const login = async (email, password) => {
  try {
    // Ensure credentials are sent to set cookies
    const res = await api.post('/auth/login', { email, password }, { withCredentials: true });
    return { success: true, data: res.data };
  } catch (error) {
    let errorMsg = 'Unable to reach the PhishGuard AI server.';
    if (error.response) {
      const status = error.response.status;
      if (status === 401) errorMsg = 'Invalid email or password.';
      else if (status === 409) errorMsg = 'An account with this email already exists.';
      else if (status === 422) errorMsg = 'Please check the entered information.';
      else if (status >= 500) errorMsg = 'Authentication server error. Please try again.';
      else errorMsg = 'An unexpected error occurred during login.';
    }
    return { success: false, error: errorMsg };
  }
};

export const logout = async () => {
  try {
    await api.post('/auth/logout', {}, { withCredentials: true });
    return { success: true };
  } catch (error) {
    return { success: false, error: 'Logout failed' };
  }
};

export const getMe = async () => {
  try {
    const res = await api.get('/auth/me', { withCredentials: true });
    return { success: true, data: res.data };
  } catch (error) {
    return { success: false };
  }
};
