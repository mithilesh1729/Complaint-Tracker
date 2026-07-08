import { FiInbox } from "react-icons/fi";
import { Link } from "react-router-dom";

import "./EmptyState.css";

function EmptyState({
  title = "Nothing here yet",
  message = "There is no data to display.",
  actionText,
  actionLink,
}) {
  return (
    <div className="empty-state">
      <FiInbox className="empty-icon" />

      <h2>{title}</h2>

      <p>{message}</p>

      {actionText && actionLink && (
        <Link to={actionLink} className="empty-button">
          {actionText}
        </Link>
      )}
    </div>
  );
}

export default EmptyState;
