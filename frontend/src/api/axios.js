import axios from "axios";
import { storage } from "../utils/storage";

const API_BASE_URL = import.meta.env.VITE_API_URL || "/api/";

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = storage.getAccessToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refresh = storage.getRefreshToken();

        const response = await axios.post(
          `${API_BASE_URL}token/refresh/`,

          {
            refresh,
          },
        );

        storage.setAccessToken(response.data.access);

        originalRequest.headers.Authorization = `Bearer ${response.data.access}`;

        return api(originalRequest);
      } catch {
        storage.clear();

        window.location.href = "/";
      }
    }

    return Promise.reject(error);
  },
);

export default api;
