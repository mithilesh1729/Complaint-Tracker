import StatsCard from "../StatsCard";

import "./StatsGrid.css";

function StatsGrid({ stats }) {
  return (
    <div className="stats-grid">
      <StatsCard title="Active" value={stats.active} />

      <StatsCard title="Pending" value={stats.pending} />

      <StatsCard title="In Progress" value={stats.in_progress} />

      <StatsCard title="Resolved" value={stats.resolved} />
    </div>
  );
}

export default StatsGrid;
