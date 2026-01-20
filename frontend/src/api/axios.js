import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/",
});

// 🔐 Attach access token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 🔁 Handle token expiry
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refresh = localStorage.getItem("refresh");

        const res = await axios.post(
          "http://localhost:8000/api/token/refresh/",
          { refresh }
        );

        localStorage.setItem("access", res.data.access);

        originalRequest.headers.Authorization = `Bearer ${res.data.access}`;

        return api(originalRequest); // 🔁 retry
      } catch {
        localStorage.clear();
        window.location.href = "/";
      }
    }

    return Promise.reject(error);
  }
);

export default api;
