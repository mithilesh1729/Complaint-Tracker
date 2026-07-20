import { useNavigate } from "react-router-dom";

import { FiArrowRight } from "react-icons/fi";

import StatusBadge from "../common/StatusBadge";
import PriorityBadge from "../common/PriorityBadge";

import "./RecentComplaints.css";

function RecentComplaints({ complaints = [] }) {
  const navigate = useNavigate();

  return (
    <section className="recent-complaints">
      <div className="recent-header">
        <h2>Recent Complaints</h2>

        <span
          className="view-all-link"
          onClick={() => navigate("/office/queue")}
        >
          View All →
        </span>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Complaint</th>
              <th>Category</th>
              <th>Priority</th>
              <th>Status</th>
              <th>Created</th>
              <th></th>
            </tr>
          </thead>

          <tbody>
            {complaints.map((complaint) => (
              <tr
                key={complaint.complaint_id}
                className="clickable-row"
                onClick={() =>
                  navigate(`/office/complaints/${complaint.complaint_id}`)
                }
              >
                <td>{complaint.complaint_number}</td>

                <td>{complaint.category.name}</td>

                <td>
                  <PriorityBadge priority={complaint.priority} />
                </td>

                <td>
                  <StatusBadge status={complaint.status === "resolved" && complaint.is_confirmed ? "confirmed" : complaint.status} />
                </td>

                <td>{complaint.created_at_human}</td>

                <td>
                  <span
                    className="open-link"
                    onClick={(e) => {
                      e.stopPropagation();

                      navigate(`/office/complaints/${complaint.complaint_id}`);
                    }}
                  >
                    View
                    <FiArrowRight />
                  </span>
                </td>
              </tr>
            ))}

            {!complaints.length && (
              <tr>
                <td colSpan="6" className="empty-row">
                  No recent complaints.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default RecentComplaints;
