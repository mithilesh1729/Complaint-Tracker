import "./PersonalInfo.css";

function PersonalInfo({ profile }) {
  return (
    <section className="profile-section">
      <h3 className="section-title">Personal Information</h3>

      <div className="info-grid">
        <div className="info-item">
          <span className="info-label">Full Name</span>

          <span className="info-value">{profile?.name}</span>
        </div>

        <div className="info-item">
          <span className="info-label">Roll Number</span>

          <span className="info-value">{profile?.roll_no}</span>
        </div>

        <div className="info-item">
          <span className="info-label">Email Address</span>

          <span className="info-value">{profile?.email}</span>
        </div>

        <div className="info-item">
          <span className="info-label">Phone Number</span>

          <span className="info-value">{profile?.phone_number || "-"}</span>
        </div>
      </div>
    </section>
  );
}

export default PersonalInfo;
