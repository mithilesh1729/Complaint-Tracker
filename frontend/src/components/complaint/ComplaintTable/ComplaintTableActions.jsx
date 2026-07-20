import "./ComplaintTable.css";

function ComplaintTableActions({ complaint, actions = [] }) {
  if (!actions.length) {
    return null;
  }

  return (
    <div className="complaint-table-actions">
      {actions.map((action) => (
        <button
          key={action.label}
          className={`table-action-button ${action.variant || "secondary"}`}
          onClick={() => action.onClick(complaint)}
          disabled={action.disabled?.(complaint)}
        >
          {action.icon && <action.icon size={16} />}

          {action.label}
        </button>
      ))}
    </div>
  );
}

export default ComplaintTableActions;
