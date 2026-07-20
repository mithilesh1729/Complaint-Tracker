import { useState, useEffect, useCallback } from "react";
import api from "../api/axios";

export default function useHostels() {
  const [hostels, setHostels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchHostels = useCallback(async (search = "") => {
    try {
      setLoading(true);
      setError(null);
      
      const config = search ? { params: { search } } : {};
      const response = await api.get("/admin/hostels/", config);
      
      setHostels(response.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load hostels");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchHostels();
  }, [fetchHostels]);

  return { hostels, loading, error, fetchHostels };
}
