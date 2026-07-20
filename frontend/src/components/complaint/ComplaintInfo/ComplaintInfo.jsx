import "./ComplaintInfo.css";

function ComplaintInfo({ complaint }) {
  if (!complaint) return null;

  return (
    <section className="complaint-info-card">
      <h3>Student Information</h3>

      <div className="complaint-info-grid">
        <div>
          <strong>Name</strong>
          <p>{complaint.user.name}</p>
        </div>

        <div>
          <strong>Roll No.</strong>
          <p>{complaint.user.roll_no}</p>
        </div>

        <div>
          <strong>Hostel</strong>
          <p>{complaint.user.hostel}</p>
        </div>

        <div>
          <strong>Room</strong>
          <p>{complaint.user.room_no}</p>
        </div>

        <div>
          <strong>Email</strong>
          <p>{complaint.user.email}</p>
        </div>
      </div>

      <hr />

      <h3>Complaint Information</h3>

      <div className="complaint-info-grid">
        <div>
          <strong>Category</strong>
          <p>{complaint.category.name}</p>
        </div>

        <div>
          <strong>Priority</strong>
          <p>{complaint.priority}</p>
        </div>

        <div>
          <strong>Location</strong>
          <p>{complaint.location_details || "-"}</p>
        </div>

        <div>
          <strong>Created</strong>
          <p>{complaint.created_at_human}</p>
        </div>

        {complaint.resolved_at && (
          <div>
            <strong>Resolved</strong>
            <p>{new Date(complaint.resolved_at).toLocaleString()}</p>
          </div>
        )}
      </div>

      <div className="complaint-description">
        <strong>Description</strong>

        <p>{complaint.description}</p>
      </div>
    </section>
  );
}

export default ComplaintInfo;
