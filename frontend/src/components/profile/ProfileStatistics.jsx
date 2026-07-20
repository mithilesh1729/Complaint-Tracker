import "./ProfileStatistics.css";

function ProfileStatistics({ profile }) {
  const stats = [];

  if (profile?.role === "Student") {
    stats.push(
      {
        label: "Total Complaints",
        value: profile.total_complaints ?? 0,
      },
      {
        label: "Pending",
        value: profile.pending_complaints ?? 0,
      },
      {
        label: "Resolved",
        value: profile.resolved_complaints ?? 0,
      },
    );
  } else {
    stats.push(
      {
        label: "Assigned",
        value: profile.assigned_count ?? 0,
      },
      {
        label: "Pending",
        value: profile.pending_count ?? 0,
      },
      {
        label: "Resolved",
        value: profile.resolved_count ?? 0,
      },
    );
  }

  return (
    <section className="profile-section">
      <h3 className="section-title">Statistics</h3>

      <div className="profile-statistics">
        {stats.map((item) => (
          <div key={item.label} className="profile-stat-card">
            <h2>{item.value}</h2>

            <p>{item.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

export default ProfileStatistics;
