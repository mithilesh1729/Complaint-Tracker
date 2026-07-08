import "./ComplaintInfo.css";

function ComplaintInfo({ complaint }) {
  return (
    <div className="complaint-info">
      <div>
        <strong>Priority</strong>
        <p>{complaint.priority}</p>
      </div>

      <div>
        <strong>Location</strong>
        <p>{complaint.location_details || "-"}</p>
      </div>

      <div>
        <strong>Description</strong>
        <p>{complaint.description}</p>
      </div>

      <div>
        <strong>Created</strong>
        <p>{new Date(complaint.created_at).toLocaleString()}</p>
      </div>

      {complaint.resolved_at && (
        <div>
          <strong>Resolved</strong>
          <p>{new Date(complaint.resolved_at).toLocaleString()}</p>
        </div>
      )}
    </div>
  );
}

export default ComplaintInfo;
