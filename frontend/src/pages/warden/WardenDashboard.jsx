import { useState, useEffect } from "react";
import api from "../../api/axios";
import { FiClock, FiAlertCircle, FiCheckCircle, FiUsers } from "react-icons/fi";
import StatCard from "../../components/common/StatCard/StatCards";
import PageHeader from "../../components/layout/PageHeader";

function WardenDashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const res = await api.get("/warden/dashboard/");
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
    { title: "Escalated to Me", value: stats.escalated ?? 0, icon: FiAlertCircle, variant: "warning" },
    { title: "Pending Overall", value: stats.pending ?? 0, icon: FiClock, variant: "secondary" },
    { title: "Resolved Today", value: stats.resolved_today ?? 0, icon: FiCheckCircle, variant: "success" },
    { title: "Overdue Complaints", value: stats.overdue ?? 0, icon: FiAlertCircle, variant: "danger" },
    { title: "Office Staff Count", value: stats.office_staff ?? 0, icon: FiUsers, variant: "info" },
  ];

  return (
    <div className="p-4">
      <PageHeader title="Warden Dashboard" subtitle="Hostel performance and escalated metrics" />
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

export default WardenDashboard;
