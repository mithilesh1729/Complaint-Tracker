import { Link } from "react-router-dom";
import { FiArrowRight } from "react-icons/fi";

import StatusBadge from "../../../common/StatusBadge";
import EmptyState from "../../../common/EmptyState";

import "./RecentComplaints.css";

function RecentComplaints({ complaints = [] }) {
  if (!complaints.length) {
    return (
      <EmptyState
        title="No Complaints Yet"
        message="Raise your first complaint and track its progress in real time."
        actionText="Raise Complaint"
        actionLink="/student/complaints/new"
      />
    );
  }

  return (
    <section className="recent-complaints">
      <div className="section-header">
        <h2>Recent Complaints</h2>

        <Link to="/student/complaints" className="view-all">
          View All
        </Link>
      </div>

      {complaints.map((complaint) => (
        <div key={complaint.complaint_id} className="complaint-card">
          <div className="complaint-header">
            <div>
              <h3>{complaint.complaint_number}</h3>

              <p>{complaint.category}</p>
            </div>

            <StatusBadge status={complaint.status} />
          </div>

          <div className="complaint-footer">
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
      ))}
    </section>
  );
}

export default RecentComplaints;
