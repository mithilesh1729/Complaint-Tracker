import { useState } from "react";

import { toast } from "react-hot-toast";

import complaintService from "../services/complaintService";

export default function useCreateComplaint() {
  const [loading, setLoading] = useState(false);

  const [error, setError] = useState(null);

  async function createComplaint(formData) {
    try {
      setLoading(true);

      setError(null);

      const complaint = await complaintService.createComplaint(formData);

      toast.success("Complaint submitted successfully.");

      return complaint;
    } catch (err) {
      setError(err);

      toast.error("Unable to submit complaint.");

      throw err;
    } finally {
      setLoading(false);
    }
  }

  return {
    createComplaint,
    loading,
    error,
  };
}
