import api from "../api/axios";

const staffService = {
  list() {
    return api.get("/staff/");
  },

  create(data) {
    return api.post("/staff/", data);
  },

  resetPassword(rollNo) {
    return api.post(`/staff/${rollNo}/reset-password/`);
  },
};

export default staffService;
