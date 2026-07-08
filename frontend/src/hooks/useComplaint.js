import { useEffect, useState } from "react";

import complaintService from "../services/complaintService";

export default function useComplaint(complaintId) {
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function fetchComplaint() {
    try {
      setLoading(true);

      const data = await complaintService.getComplaint(complaintId);

      setComplaint(data);

      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (complaintId) {
      fetchComplaint();
    }
  }, [complaintId]);

  return {
    complaint,
    loading,
    error,
    refresh: fetchComplaint,
  };
}
