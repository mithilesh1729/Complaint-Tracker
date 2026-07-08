import api from "../api/axios";

const complaintService = {
  async getMyComplaints() {
    const response = await api.get("/complaints/");
    return response.data;
  },

  async getComplaint(complaintId) {
    const response = await api.get(`/complaints/${complaintId}/`);

    return response.data;
  },

  async createComplaint(formData) {
    const response = await api.post("/complaints/create/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data;
  },

  async confirmComplaint(complaintId, feedback = "") {
    const response = await api.post(`/complaints/${complaintId}/confirm/`, {
      feedback,
    });

    return response.data;
  },

  async reopenComplaint(complaintId, feedback = "") {
    const response = await api.post(`/complaints/${complaintId}/reopen/`, {
      feedback,
    });

    return response.data;
  },

  async downloadSlip(complaintId) {
    const response = await api.get(`/complaints/${complaintId}/slip/`, {
      responseType: "blob",
    });

    return response.data;
  },
};

export default complaintService;
