import axios from 'axios';

// Use environment variable if available, otherwise fall back to localhost for development
const API_BASE_URL = "https://book-slots.onrender.com/api";

console.log('API Base URL:', API_BASE_URL); // For debugging

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add a response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);