import { useNavigate } from "react-router-dom";

import { FiArrowRight, FiInbox, FiTool } from "react-icons/fi";

import "./QuickActions.css";

function QuickActions() {
  const navigate = useNavigate();

  const actions = [
    {
      title: "Incoming Complaints",

      description: "Review newly submitted complaints waiting for assignment.",

      icon: FiInbox,

      button: "View Queue",

      onClick: () => navigate("/office/queue"),
    },

    {
      title: "My Assigned Work",

      description: "Manage complaints currently assigned to you.",

      icon: FiTool,

      button: "View Assigned Work",

      onClick: () => navigate("/office/assigned"),
    },
  ];

  return (
    <section className="quick-actions">
      <h2>Quick Actions</h2>

      <div className="quick-actions-grid">
        {actions.map((action) => {
          const Icon = action.icon;

          return (
            <article
              key={action.title}
              className="action-card clickable"
              onClick={action.onClick}
            >
              <div className="action-icon">
                <Icon />
              </div>

              <div className="action-content">
                <h3>{action.title}</h3>

                <p>{action.description}</p>

                <div className="action-link">
                  {action.button}

                  <FiArrowRight />
                </div>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}

export default QuickActions;
