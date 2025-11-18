import axios, { AxiosInstance, AxiosError } from 'axios';
import { ApiError } from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiError>) => {
    if (error.response) {
      // Server responded with error
      const apiError: ApiError = {
        detail: error.response.data?.detail || 'An error occurred',
        status: error.response.status,
      };

      // Handle 401 Unauthorized
      if (error.response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/';
      }

      return Promise.reject(apiError);
    } else if (error.request) {
      // Request made but no response
      return Promise.reject({
        detail: 'No response from server. Please check your connection.',
      });
    } else {
      // Error in request setup
      return Promise.reject({
        detail: error.message || 'An error occurred',
      });
    }
  }
);

export default api;
