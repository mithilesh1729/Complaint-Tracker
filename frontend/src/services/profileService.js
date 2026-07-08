import api from "../api/axios";

const profileService = {
  async getProfile() {
    const response = await api.get("/profile/");

    return response.data;
  },
};

export default profileService;