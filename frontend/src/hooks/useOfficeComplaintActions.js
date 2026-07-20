import { useState } from "react";

import { resolveComplaint, escalateComplaint, assignComplaint, updateProgress } from "../services/officeService";
import complaintService from "../services/complaintService";

function useOfficeComplaintActions(refresh) {
  const [loading, setLoading] = useState(false);

  async function resolve(complaintId, payload = {}) {
    try {
      setLoading(true);
      await resolveComplaint(complaintId, payload);
      if (refresh) await refresh();
      return { success: true };
    } catch (error) {
      console.error(error);
      return { success: false };
    } finally {
      setLoading(false);
    }
  }

  async function escalate(complaintId, payload = {}) {
    try {
      setLoading(true);
      await escalateComplaint(complaintId, payload);
      if (refresh) await refresh();
      return { success: true };
    } catch (error) {
      console.error(error);
      return { success: false };
    } finally {
      setLoading(false);
    }
  }
  
  async function assign(complaintId, payload = {}) {
    try {
      setLoading(true);
      await assignComplaint(complaintId, payload);
      if (refresh) await refresh();
      return { success: true };
    } catch (error) {
      console.error(error);
      return { success: false };
    } finally {
      setLoading(false);
    }
  }
  
  async function progress(complaintId, payload = {}) {
    try {
      setLoading(true);
      await updateProgress(complaintId, payload);
      if (refresh) await refresh();
      return { success: true };
    } catch (error) {
      console.error(error);
      return { success: false };
    } finally {
      setLoading(false);
    }
  }
  
  async function download(complaintId, complaintNumber) {
    try {
      setLoading(true);
      const blob = await complaintService.downloadSlip(complaintId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `Complaint_Slip_${complaintNumber}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      return { success: true };
    } catch (error) {
      return { success: false };
    } finally {
      setLoading(false);
    }
  }

  return {
    loading,
    resolveComplaint: resolve,
    escalateComplaint: escalate,
    assignComplaint: assign,
    updateProgress: progress,
    downloadSlip: download,
  };
}

export default useOfficeComplaintActions;
