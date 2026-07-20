import { useEffect, useState } from "react";
import { getComplaintDetails } from "../services/officeService";

function useComplaintDetails(id) {
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  async function fetchComplaint() {
    try {
      setLoading(true);

      const data = await getComplaintDetails(id);

      setComplaint(data);

      setError(false);
    } catch (err) {
      console.error(err);
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchComplaint();
  }, [id]);

  return {
    complaint,
    loading,
    error,
    refresh: fetchComplaint,
  };
}

export default useComplaintDetails;
