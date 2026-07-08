import { useState } from "react";

import complaintService from "../services/complaintService";

export default function useComplaintActions(refresh) {
  const [loading, setLoading] = useState(false);

  async function downloadSlip(complaintId, complaintNumber) {
    try {
      setLoading(true);
      const blob = await complaintService.downloadSlip(complaintId);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = `${complaintNumber}.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      return {
        success: true,
      };
    } catch (error) {
      return {
        success: false,
        error,
      };
    } finally {
      setLoading(false);
    }
  }

  async function confirmComplaint(complaintId, feedback = "") {
    try {
      setLoading(true);

      await complaintService.confirmComplaint(complaintId, feedback);

      await refresh();

      return {
        success: true,
      };
    } catch (error) {
      return {
        success: false,
        error,
      };
    } finally {
      setLoading(false);
    }
  }

  async function reopenComplaint(complaintId, feedback) {
    try {
      setLoading(true);

      await complaintService.reopenComplaint(complaintId, feedback);

      await refresh();

      return {
        success: true,
      };
    } catch (error) {
      return {
        success: false,
        error,
      };
    } finally {
      setLoading(false);
    }
  }

  return {
    loading,

    downloadSlip,

    confirmComplaint,

    reopenComplaint,
  };
}
