import "./StatCard.css";

function StatCard({ title, subtitle, value, icon: Icon, variant = "primary" }) {
  return (
    <article className={`stat-card ${variant}`}>
      <div className="stat-card-header">
        <div>
          <h3>{title}</h3>

          {subtitle && <span>{subtitle}</span>}
        </div>

        {Icon && (
          <div className="stat-icon">
            <Icon />
          </div>
        )}
      </div>

      <h2>{value}</h2>
    </article>
  );
}

export default StatCard;
