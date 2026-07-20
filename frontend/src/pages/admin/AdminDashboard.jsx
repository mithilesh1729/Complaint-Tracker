import { 
  FiUsers, 
  FiShield, 
  FiFolder, 
  FiAlertCircle, 
  FiClock, 
  FiCheckCircle, 
  FiLayers 
} from "react-icons/fi";
import useAdminDashboard from "../../hooks/useAdminDashboard";
import StatCard from "../../components/common/StatCard/StatCards";
import PageHeader from "../../components/layout/PageHeader";

function AdminDashboard() {
  const { dashboard, loading, error, refresh } = useAdminDashboard();

  if (loading) {
    return <div className="p-4">Loading dashboard statistics...</div>;
  }

  if (error) {
    return (
      <div className="p-4 text-danger">
        <h4>Error loading dashboard</h4>
        <p>{error}</p>
        <button className="btn btn-outline-danger" onClick={refresh}>Retry</button>
      </div>
    );
  }

  const stats = dashboard?.stats || {};

  const cards = [
    {
      title: "Total Students",
      value: stats.total_students ?? 0,
      icon: FiUsers,
      variant: "primary"
    },
    {
      title: "Total Staff",
      value: stats.total_staff ?? 0,
      icon: FiShield,
      variant: "info"
    },
    {
      title: "Total Categories",
      value: stats.total_categories ?? 0,
      icon: FiFolder,
      variant: "secondary"
    },
    {
      title: "Total Complaints",
      value: stats.total_complaints ?? 0,
      icon: FiLayers,
      variant: "dark"
    },
    {
      title: "Pending",
      value: stats.pending ?? 0,
      icon: FiClock,
      variant: "warning"
    },
    {
      title: "In Progress",
      value: stats.in_progress ?? 0,
      icon: FiAlertCircle,
      variant: "primary"
    },
    {
      title: "Resolved",
      value: stats.resolved ?? 0,
      icon: FiCheckCircle,
      variant: "success"
    },
    {
      title: "High Priority",
      value: stats.high_priority ?? 0,
      icon: FiAlertCircle,
      variant: "danger"
    }
  ];

  return (
    <div className="p-4">
      <PageHeader 
        title="Admin Dashboard" 
        subtitle="System overview and key metrics"
      />
      
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", gap: "24px", marginTop: "24px" }}>
        {cards.map((card) => (
          <div key={card.title}>
            <StatCard
              title={card.title}
              value={card.value}
              icon={card.icon}
              variant={card.variant}
            />
          </div>
        ))}
      </div>
    </div>
  );
}

export default AdminDashboard;
