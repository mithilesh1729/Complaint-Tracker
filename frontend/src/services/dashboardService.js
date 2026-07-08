// import complaintService from "./complaintService";

// const dashboardService = {
//   async studentDashboard() {
//     const response = await complaintService.getMyComplaints();

//     return response.data;
//   },
// };

// export default dashboardService;


import api from "../api/axios";

const dashboardService = {
  async getDashboard() {
    const response = await api.get("/student/dashboard/");
    return response.data;
  },
};

export default dashboardService;
