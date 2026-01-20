import api from "./axios";

export const downloadComplaintSlip = async (complaintId) => {
  const response = await api.get(`/complaints/${complaintId}/slip/`, {
    responseType: "blob", // 🔑 IMPORTANT
  });

  // Create file URL
  const url = window.URL.createObjectURL(
    new Blob([response.data], { type: "application/pdf" })
  );

  // Create temporary <a>
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `complaint_${complaintId}.pdf`);

  document.body.appendChild(link);
  link.click();

  // Cleanup
  link.remove();
  window.URL.revokeObjectURL(url);
};
