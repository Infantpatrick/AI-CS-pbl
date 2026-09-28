import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeEmail = async (subject, body) => {
  try {
    const response = await api.post('/predict', { subject, body });
    return { success: true, data: response.data };
  } catch (error) {
    if (error.response) {
      // Server responded with error status
      return { 
        success: false, 
        error: error.response.data?.detail || 'Analysis failed. Please check your inputs.' 
      };
    } else if (error.request) {
      // Request made but no response
      return { 
        success: false, 
        error: 'Unable to connect to the analysis server. Please make sure the backend is running.' 
      };
    } else {
      return { 
        success: false, 
        error: 'An unexpected error occurred while processing your request.' 
      };
    }
  }
};
