import { useState, useEffect, useCallback } from "react";
import api from "../api/axios";

export default function useStaff() {
  const [staff, setStaff] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchStaff = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get("/staff/");
      setStaff(response.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load staff");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStaff();
  }, [fetchStaff]);

  return { staff, loading, error, fetchStaff };
}
