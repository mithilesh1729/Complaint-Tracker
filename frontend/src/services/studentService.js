import api from "../api/axios";

const studentService = {
  profile() {
    return api.get("/student/profile/");
  },
};

export default studentService;
