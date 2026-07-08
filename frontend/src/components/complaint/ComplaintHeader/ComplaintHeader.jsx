import StatusBadge from "../../common/StatusBadge";

import "./ComplaintHeader.css";

function ComplaintHeader({ complaint }) {
  return (
    <div className="complaint-header-card">
      <div>
        <h2>{complaint.complaint_number}</h2>

        <p>{complaint.category.name}</p>
      </div>

      <StatusBadge status={complaint.status} />
    </div>
  );
}

export default ComplaintHeader;
