import api from "../api/axios";

const authService = {
  login(credentials) {
    return api.post("/token/", credentials);
  },

  refresh(refresh) {
    return api.post("/token/refresh/", {
      refresh,
    });
  },

  profile() {
    return api.get("/profile/");
  },

  logout(refreshToken) {
    return api.post("/token/logout/", {
      refresh_token: refreshToken
    });
  },
};

export default authService;
