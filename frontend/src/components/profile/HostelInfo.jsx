import "./HostelInfo.css";

function HostelInfo({ profile }) {
  return (
    <section className="profile-section">
      <h3 className="section-title">Organization Information</h3>

      <div className="info-grid">
        {profile?.hostel && (
          <div className="info-item">
            <span className="info-label">Hostel</span>

            <span className="info-value">{profile.hostel}</span>
          </div>
        )}

        {profile?.room_no && (
          <div className="info-item">
            <span className="info-label">Room Number</span>

            <span className="info-value">{profile.room_no}</span>
          </div>
        )}

        <div className="info-item">
          <span className="info-label">Role</span>

          <span className="info-value">{profile?.role}</span>
        </div>

        <div className="info-item">
          <span className="info-label">Portal</span>

          <span className="info-value">Hostel Complaint Tracker</span>
        </div>
      </div>
    </section>
  );
}

export default HostelInfo;
