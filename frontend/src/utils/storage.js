const ACCESS_TOKEN = "access";
const REFRESH_TOKEN = "refresh";

export const storage = {
  getAccessToken() {
    return localStorage.getItem(ACCESS_TOKEN);
  },

  setAccessToken(token) {
    localStorage.setItem(ACCESS_TOKEN, token);
  },

  removeAccessToken() {
    localStorage.removeItem(ACCESS_TOKEN);
  },

  getRefreshToken() {
    return localStorage.getItem(REFRESH_TOKEN);
  },

  setRefreshToken(token) {
    localStorage.setItem(REFRESH_TOKEN, token);
  },

  removeRefreshToken() {
    localStorage.removeItem(REFRESH_TOKEN);
  },

  clear() {
    localStorage.removeItem(ACCESS_TOKEN);
    localStorage.removeItem(REFRESH_TOKEN);
  },
};
