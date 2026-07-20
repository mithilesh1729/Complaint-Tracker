import { useState, useEffect, useCallback } from "react";
import api from "../api/axios";

export default function useStudents() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [pagination, setPagination] = useState({
    next: null,
    previous: null,
    currentPage: 1
  });

  const fetchStudents = useCallback(async (url = "/students/", params = {}) => {
    try {
      setLoading(true);
      setError(null);
      
      const config = url === "/students/" ? { params } : {};
      const response = await api.get(url, config);
      
      setStudents(response.data.results || response.data);
      
      if (response.data.results) {
        setPagination({
          next: response.data.next,
          previous: response.data.previous,
          currentPage: extractPageNumber(url, params)
        });
      }
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load students");
    } finally {
      setLoading(false);
    }
  }, []);
  
  const extractPageNumber = (url, params) => {
    if (params?.page) return params.page;
    try {
      const match = url.match(/page=(\d+)/);
      if (match) return parseInt(match[1], 10);
    } catch (e) {}
    return 1;
  };

  useEffect(() => {
    fetchStudents();
  }, [fetchStudents]);

  return { students, loading, error, pagination, fetchStudents };
}
