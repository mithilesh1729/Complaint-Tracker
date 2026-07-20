import "./PriorityBadge.css";

function PriorityBadge({ priority }) {
  return (
    <span className={`priority-badge ${priority}`}>
      {priority?.charAt(0).toUpperCase() + priority?.slice(1)}
    </span>
  );
}

export default PriorityBadge;
