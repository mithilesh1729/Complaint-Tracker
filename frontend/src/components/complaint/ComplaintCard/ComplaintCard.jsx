import { Link } from "react-router-dom";
import { FiArrowRight } from "react-icons/fi";

import StatusBadge from "../../common/StatusBadge";

import "./ComplaintCard.css";

function ComplaintCard({ complaint }) {
  return (
    <div className="complaint-card">
      <div className="complaint-card-header">
        <div>
          <h3>{complaint.complaint_number}</h3>

          <p>{complaint.category.name}</p>
        </div>

        <StatusBadge status={complaint.status} />
      </div>

      <div className="complaint-card-footer">
        <span>{new Date(complaint.created_at).toLocaleDateString()}</span>

        <Link
          to={`/student/complaints/${complaint.complaint_id}`}
          className="details-link"
        >
          View Details
          <FiArrowRight />
        </Link>
      </div>
    </div>
  );
}

export default ComplaintCard;
