import axios from 'axios';
import { authService } from './auth';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = authService.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, logout user
      authService.logout();
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

/**
 * API Service for Wordle backend communication
 * Handles all HTTP requests to the backend using axios
 */

/**
 * Authentication API calls
 */
export const authAPI = {
  // Login user
  async login(username, password) {
    try {
      const response = await apiClient.post('/auth/login', { username, password });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Login failed');
    }
  },

  // Register new user
  async register(username, email, password) {
    try {
      const response = await apiClient.post('/auth/register', { username, email, password });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  },

  // Get user stats
  async getUserStats() {
    try {
      const response = await apiClient.get('/stats');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch user stats');
    }
  },
};

/**
 * Game API calls
 */
export const gameAPI = {
  // Get daily word
  async getDailyWord() {
    try {
      const response = await apiClient.get('/game/word');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch daily word');
    }
  },

  // Validate a guess
  async validateGuess(guess, wordId) {
    try {
      const response = await apiClient.post('/game/guess', {
        guess: guess.toUpperCase(),
        wordId
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to validate guess');
    }
  },

  // Submit game result
  async submitGameResult(gameData) {
    try {
      const response = await apiClient.post('/game/result', gameData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to submit game result');
    }
  },
};

/**
 * Utility functions
 */
export const apiUtils = {
  // Check if user is authenticated
  isAuthenticated() {
    return authService.isAuthenticated();
  },

  // Get stored username
  getStoredUsername() {
    return authService.getUsername();
  },

  // Clear authentication data
  logout() {
    authService.logout();
  },
};
