import { useState, useEffect, useCallback } from "react";
import api from "../api/axios";

export default function useDepartments() {
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDepartments = useCallback(async (search = "") => {
    try {
      setLoading(true);
      setError(null);
      
      const config = search ? { params: { search } } : {};
      const response = await api.get("/admin/departments/", config);
      
      // DRF PageNumberPagination returns results inside .results, check for it
      const results = response.data.results || response.data;
      setDepartments(results);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load departments");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDepartments();
  }, [fetchDepartments]);

  return { departments, loading, error, fetchDepartments };
}
