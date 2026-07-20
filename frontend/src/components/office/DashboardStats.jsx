import {
  FiClock,
  FiBriefcase,
  FiCheckCircle,
  FiAlertTriangle,
} from "react-icons/fi";

import { useNavigate } from "react-router-dom";

import "./DashboardStats.css";

function DashboardStats({ stats }) {
  const navigate = useNavigate();

  const cards = [
    {
      title: "Pending",
      value: stats?.pending ?? 0,
      subtitle: "Waiting for assignment",
      icon: FiClock,
      variant: "warning",
      onClick: () => navigate("/office/queue"),
    },
    {
      title: "Assigned",
      value: stats?.assigned ?? 0,
      subtitle: "Currently assigned",
      icon: FiBriefcase,
      variant: "primary",
      onClick: () => navigate("/office/assigned"),
    },
    {
      title: "Resolved",
      value: stats?.resolved_today ?? 0,
      subtitle: "Completed today",
      icon: FiCheckCircle,
      variant: "success",
      onClick: () => navigate("/office/assigned?status=resolved"),
    },
    {
      title: "High Priority",
      value: stats?.high_priority ?? 0,
      subtitle: "Requires attention",
      icon: FiAlertTriangle,
      variant: "danger",
      onClick: () => navigate("/office/queue?priority=high"),
    },
  ];

  return (
    <section className="dashboard-stats">
      {cards.map((card) => {
        const Icon = card.icon;

        return (
          <article
            key={card.title}
            className={`stats-card ${card.variant} clickable`}
            onClick={card.onClick}
          >
            <div className="stats-card-header">
              <div>
                <h3>{card.title}</h3>

                <span>{card.subtitle}</span>
              </div>

              <div className="stats-icon">
                <Icon />
              </div>
            </div>

            <h2>{card.value}</h2>
          </article>
        );
      })}
    </section>
  );
}

export default DashboardStats;
