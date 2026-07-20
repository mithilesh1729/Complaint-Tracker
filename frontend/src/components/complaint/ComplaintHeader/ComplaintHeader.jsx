// import StatusBadge from "../../common/StatusBadge";

// import "./ComplaintHeader.css";

// function ComplaintHeader({ complaint }) {
//   return (
//     <div className="complaint-header-card">
//       <div>
//         <h2>{complaint.complaint_number}</h2>

//         <p>{complaint.category.name}</p>
//       </div>

//       <StatusBadge status={complaint.status} />
//     </div>
//   );
// }

// export default ComplaintHeader;

import StatusBadge from "../../common/StatusBadge";
import PriorityBadge from "../../common/PriorityBadge";

import "./ComplaintHeader.css";

function ComplaintHeader({ complaint }) {
  if (!complaint) return null;

  return (
    <div className="complaint-header-card">
      <div className="complaint-header-left">
        <h2>{complaint.complaint_number}</h2>

        <p>{complaint.category.name}</p>

        <small>Created {complaint.created_at_human}</small>
      </div>

      <div className="complaint-header-right">
        <PriorityBadge priority={complaint.priority} />

        <StatusBadge status={complaint.status === "resolved" && complaint.is_confirmed ? "confirmed" : complaint.status} />
      </div>
    </div>
  );
}

export default ComplaintHeader;
