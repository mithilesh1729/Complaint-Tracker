import { useState, useEffect } from "react";
import api from "../../api/axios";
import { FiAlertCircle, FiCheckCircle, FiTrendingUp, FiHome, FiClock } from "react-icons/fi";
import StatCard from "../../components/common/StatCard/StatCards";
import PageHeader from "../../components/layout/PageHeader";

function HMCDashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const res = await api.get("/hmc/dashboard/");
      setDashboard(res.data);
      setError(null);
    } catch (err) {
      setError("Failed to load dashboard.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-4">Loading dashboard statistics...</div>;
  if (error) return <div className="p-4 text-danger">{error}</div>;

  const stats = dashboard?.stats || {};

  const cards = [
    { title: "Total Hostels", value: stats.total_hostels ?? 0, icon: FiHome, variant: "primary" },
    { title: "Total Escalated", value: stats.total_escalated ?? 0, icon: FiTrendingUp, variant: "warning" },
    { title: "Pending Overall", value: stats.pending_overall ?? 0, icon: FiClock, variant: "secondary" },
    { title: "Resolved Overall", value: stats.resolved_overall ?? 0, icon: FiCheckCircle, variant: "success" },
    { title: "High Priority (Active)", value: stats.high_priority ?? 0, icon: FiAlertCircle, variant: "danger" },
  ];

  return (
    <div className="p-4">
      <PageHeader title="HMC Dashboard" subtitle="Global hostel performance and escalations" />
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", gap: "24px", marginTop: "24px" }}>
        {cards.map((card) => (
          <div key={card.title}>
            <StatCard title={card.title} value={card.value} icon={card.icon} variant={card.variant} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default HMCDashboard;
