import "./StatCard.css";

function StatCard({
  title,

  value,

  icon,

  color = "primary",
}) {
  const Icon = icon;

  return (
    <div className={`stat-card ${color}`}>
      <div className="stat-card-top">
        <div>
          <p className="stat-title">{title}</p>

          <h2>{value}</h2>
        </div>

        {Icon && <Icon className="stat-icon" />}
      </div>
    </div>
  );
}

export default StatCard;
