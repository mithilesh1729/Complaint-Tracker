import { FiActivity, FiClock, FiTool, FiCheckCircle } from "react-icons/fi";

import StatCard from "../../..//common/StatCard";

// import "src/pages/student/Dashboard/Dashboard.css";

function StatsGrid({ stats }) {
  const cards = [
    {
      title: "Active",
      subtitle: "Currently active",
      value: stats.active,
      icon: FiActivity,
      variant: "primary",
    },
    {
      title: "Pending",
      subtitle: "Waiting for action",
      value: stats.pending,
      icon: FiClock,
      variant: "warning",
    },
    {
      title: "In Progress",
      subtitle: "Being resolved",
      value: stats.in_progress,
      icon: FiTool,
      variant: "primary",
    },
    {
      title: "Resolved",
      subtitle: "Completed complaints",
      value: stats.resolved,
      icon: FiCheckCircle,
      variant: "success",
    },
  ];

  return (
    <section className="dashboard-stats">
      {cards.map((card) => (
        <StatCard
          key={card.title}
          title={card.title}
          subtitle={card.subtitle}
          value={card.value}
          icon={card.icon}
          variant={card.variant}
        />
      ))}
    </section>
  );
}

export default StatsGrid;
