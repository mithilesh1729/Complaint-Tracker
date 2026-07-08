import "./ComplaintTimeline.css";

function ComplaintTimeline({ complaint }) {
  if (!complaint.status_history?.length) {
    return null;
  }

  return (
    <div className="complaint-timeline">
      <h3>Status Timeline</h3>

      {complaint.status_history.map((item, index) => (
        <div key={index} className="timeline-item">
          <strong>{item.status}</strong>

          <p>{item.message}</p>

          <small>{new Date(item.timestamp).toLocaleString()}</small>
        </div>
      ))}
    </div>
  );
}

export default ComplaintTimeline;
