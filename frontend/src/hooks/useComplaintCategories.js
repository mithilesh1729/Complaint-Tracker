import { useEffect, useState } from "react";

import complaintCategoryService from "../services/complaintCategoryService";

export default function useComplaintCategories() {
  const [categories, setCategories] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState(null);

  async function fetchCategories() {
    try {
      setLoading(true);

      const data = await complaintCategoryService.getCategories();

      setCategories(data);

      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchCategories();
  }, []);

  return {
    categories,
    loading,
    error,
    refresh: fetchCategories,
  };
}
