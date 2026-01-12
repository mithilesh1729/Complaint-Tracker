import api from "./axios";

export const checkAuth = async () => {
  try {
    await api.get("/check-auth/");
    return true;
  } catch {
    return false;
  }
};
