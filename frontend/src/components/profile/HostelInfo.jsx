import "./HostelInfo.css";

function HostelInfo({ profile }) {
  return (
    <section className="profile-section">
      <h3 className="section-title">Hostel Information</h3>

      <div className="info-grid">
        <div className="info-item">
          <span className="info-label">Hostel</span>

          <span className="info-value">{profile?.hostel || "-"}</span>
        </div>

        <div className="info-item">
          <span className="info-label">Room Number</span>

          <span className="info-value">{profile?.room_no || "-"}</span>
        </div>

        <div className="info-item">
          <span className="info-label">Account Type</span>

          <span className="info-value">Student</span>
        </div>

        <div className="info-item">
          <span className="info-label">Complaint Portal</span>

          <span className="info-value">Hostel Complaint Tracker</span>
        </div>
      </div>
    </section>
  );
}

export default HostelInfo;
