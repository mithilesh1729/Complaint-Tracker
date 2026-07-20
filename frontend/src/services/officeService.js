import api from "../api/axios";

export async function getDashboard() {
  const { data } = await api.get("/office/dashboard/");
  return data;
}

export async function getIncomingComplaints(params = {}) {
  const { data } = await api.get("/office/queue/", {
    params,
  });

  return data;
}

// export async function assignComplaint(complaintId) {
//   const { data } = await api.post(`/office/complaints/${complaintId}/assign/`);

//   return data;
// }

export async function getAssignedComplaints(params = {}) {
  const { data } = await api.get("/office/assigned/", {
    params,
  });

  return data;
}

export async function resolveComplaint(complaintId, payload) {
  const { data } = await api.post(
    `/office/complaints/${complaintId}/resolve/`,
    payload,
  );

  return data;
}

export async function getComplaintDetails(complaintId) {
  const { data } = await api.get(`/complaints/${complaintId}/`);

  return data;
}


export async function assignComplaint(complaintId, payload) {
  const { data } = await api.post(
    `/office/complaints/${complaintId}/assign/`,
    payload,
  );

  return data;
}

export async function escalateComplaint(complaintId, payload) {
  const { data } = await api.post(
    `/office/complaints/${complaintId}/escalate/`,
    payload,
  );

  return data;
}

export async function updateProgress(complaintId, payload) {
  const { data } = await api.patch(
    `/complaints/${complaintId}/progress/`,
    payload,
  );

  return data;
}
