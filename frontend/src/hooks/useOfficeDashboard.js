import { useEffect, useState } from "react";

import { getDashboard } from "../services/officeService";

export default function useOfficeDashboard() {
  const [dashboard, setDashboard] = useState(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState(null);

  async function fetchDashboard() {
    try {
      setLoading(true);

      const data = await getDashboard();

      setDashboard(data);

      setError(null);
    } catch (err) {
      console.error(err);

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
