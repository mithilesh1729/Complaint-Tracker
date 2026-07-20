import { useEffect, useState } from "react";

import complaintService from "../services/complaintService";

export default function useComplaints() {
  const [complaints, setComplaints] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState(null);

  async function fetchComplaints() {
    try {
      setLoading(true);

      //   await new Promise((resolve) => setTimeout(resolve, 3000));

      const data = await complaintService.getMyComplaints();
    
      
      // DRF pagination support
      setComplaints(data.results ?? data);

      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchComplaints();
  }, []);

  return {
    complaints,
    loading,
    error,
    refresh: fetchComplaints,
  };
}
