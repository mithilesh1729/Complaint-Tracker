import { useState } from "react";

import toast from "react-hot-toast";

import { assignComplaint } from "../services/officeService";

function useAssignComplaint(refresh) {
  const [loading, setLoading] = useState(false);

  async function assign(complaintId, payload) {
    try {
      setLoading(true);

      await assignComplaint(complaintId, payload);

      toast.success("Complaint assigned successfully.");

      refresh();

      return {
        success: true,
      };
    } catch {
      toast.error("Unable to assign complaint.");

      return {
        success: false,
      };
    } finally {
      setLoading(false);
    }
  }

  return {
    loading,
    assign,
  };
}

export default useAssignComplaint;
