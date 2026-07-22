import "./PageHeader.css";

function PageHeader({
  title,
  subtitle,
  action,
}) {
  return (
    <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div>
        <h1 style={{ marginBottom: "8px" }}>{title}</h1>
        <p style={{ color: "var(--color-text-secondary)" }}>{subtitle}</p>
      </div>
      {action && (
        <div className="page-header-action">
          {action}
        </div>
      )}
    </div>
  );
}

export default PageHeader;
