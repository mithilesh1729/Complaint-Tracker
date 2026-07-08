import api from "../api/axios";

const complaintCategoryService = {
  async getCategories() {
    const response = await api.get("/complaint-categories/");

    return response.data;
  },
};

export default complaintCategoryService;
