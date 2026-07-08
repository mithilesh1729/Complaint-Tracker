import { useEffect, useState } from "react";

import dashboardService from "../services/dashboardService";

export default function useDashboard() {
  const [dashboard, setDashboard] = useState(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState(null);

  async function fetchDashboard() {
    try {
      setLoading(true);

      const data = await dashboardService.getDashboard();

      setDashboard(data);

      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchDashboard();
  }, []);

  return {
    dashboard,
    loading,
    error,
    refresh: fetchDashboard,
  };
}
