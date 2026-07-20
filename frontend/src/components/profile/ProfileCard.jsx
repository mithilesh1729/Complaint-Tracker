import "./ProfileCard.css";

function ProfileCard({ profile }) {
  const initials =
    profile?.name
      ?.split(" ")
      .map((word) => word[0])
      .join("")
      .substring(0, 2)
      .toUpperCase() || "U";

  return (
    <section className="profile-card">
      <div className="profile-avatar">{initials}</div>

      <div className="profile-content">
        <h2>{profile?.name}</h2>

        {profile?.roll_no && <p className="profile-roll">{profile.roll_no}</p>}

        <span className="profile-role">{profile?.role || "User"}</span>
      </div>
    </section>
  );
}

export default ProfileCard;
