import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHealth = async () => {
  try {
    const res = await api.get('/health', { timeout: 8000 });
    return { success: true, data: res.data };
  } catch (error) {
    return { success: false, error };
  }
};

export const getModelInfo = async () => {
  try {
    const res = await api.get('/model-info', { timeout: 8000 });
    return { success: true, data: res.data };
  } catch (error) {
    return { success: false, error };
  }
};

export const predict = async (subject, body, signal) => {
  try {
    const res = await api.post('/predict', { subject, body }, { signal, timeout: 60000, withCredentials: true });
    return { success: true, data: res.data };
  } catch (error) {
    if (axios.isCancel(error)) {
      return { success: false, error: 'Analysis cancelled', cancelled: true };
    }
    return { 
      success: false, 
      error: error.response?.data?.detail || 'Can\'t reach the analysis service. Check that the backend is running and try again.' 
    };
  }
};

export const analyzeEmail = async (emailData, signal) => {
  try {
    const res = await api.post('/api/analyze-email', emailData, { signal, timeout: 60000, withCredentials: true });
    return { success: true, data: res.data };
  } catch (error) {
    if (axios.isCancel(error)) {
      return { success: false, error: 'Analysis cancelled', cancelled: true };
    }
    return { 
      success: false, 
      error: error.response?.data?.detail || 'Analysis failed. Please try again.' 
    };
  }
};
export const getDashboardStats = async () => {
  try {
    const res = await api.get('/api/analysis/stats', { withCredentials: true });
    return { success: true, data: res.data };
  } catch (error) {
    return { success: false, error: 'Failed to fetch statistics' };
  }
};

export const getAnalysisHistory = async () => {
  try {
    const res = await api.get('/api/analysis/history', { withCredentials: true });
    return { success: true, data: res.data };
  } catch (error) {
    return { success: false, error: 'Failed to fetch analysis history' };
  }
};
