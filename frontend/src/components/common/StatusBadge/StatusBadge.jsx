import "./StatusBadge.css";

function StatusBadge({ status }) {
  const normalized = status?.toLowerCase();

  const label =
    {
      pending: "Pending",
      in_progress: "In Progress",
      resolved: "Resolved",
      confirmed: "Confirmed",
      reopened: "Reopened",
    }[normalized] || status;

  return <span className={`status-badge ${normalized}`}>{label}</span>;
}

export default StatusBadge;
