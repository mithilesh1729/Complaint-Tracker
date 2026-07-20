import { useEffect, useState } from "react";

import { getAssignedComplaints } from "../services/officeService";
import { useSearchParams } from "react-router-dom";
import { PAGE_SIZE } from "../constants/pagination";

function useAssignedComplaints() {
  const [complaints, setComplaints] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState(false);

  const [pagination, setPagination] = useState(null);

  const [page, setPage] = useState(1);

  const [searchParams] = useSearchParams();

  const [filters, setFilters] = useState({
    search: searchParams.get("search") || "",
    priority: searchParams.get("priority") || "",
    status: searchParams.get("status") || "",
    category: searchParams.get("category") || "",
    ordering: searchParams.get("ordering") || "-created_at",
  });

  async function fetchComplaints() {
    try {
      setLoading(true);

      setError(false);

      const data = await getAssignedComplaints({
        page,
        ...filters,
      });

      setComplaints(data.results);

      setPagination({
        count: data.count,
        next: data.next,
        previous: data.previous,
        currentPage: page,
        totalPages: Math.ceil(data.count / PAGE_SIZE),
      });
    } catch (error) {
      console.error(error);

      setError(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchComplaints();
  }, [page, filters]);

  function updateFilters(values) {
    setFilters((prev) => ({
      ...prev,
      ...values,
    }));

    setPage(1);
  }

  return {
    complaints,
    loading,
    error,
    pagination,
    page,
    setPage,
    filters,
    updateFilters,
    refresh: fetchComplaints,
  };
}

export default useAssignedComplaints;
