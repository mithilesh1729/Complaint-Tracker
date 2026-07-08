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
};

export default authService;
