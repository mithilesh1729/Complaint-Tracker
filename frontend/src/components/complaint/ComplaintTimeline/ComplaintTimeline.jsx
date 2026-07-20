import StatusBadge from "../../common/StatusBadge";

import "./ComplaintTimeline.css";

function ComplaintTimeline({ complaint }) {
  if (!complaint?.status_history?.length) {
    return null;
  }

  return (
    <section className="complaint-timeline">
      <h3>Status Timeline</h3>

      <div className="timeline">
        {complaint.status_history.map((item, index) => (
          <div key={index} className="timeline-item">
            <div className="timeline-dot" />

            <div className="timeline-content">
              <div className="timeline-header">
                <StatusBadge status={item.status} />

                <small>{new Date(item.timestamp).toLocaleString()}</small>
              </div>

              <p>{item.message}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default ComplaintTimeline;
