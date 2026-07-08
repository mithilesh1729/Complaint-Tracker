import { FiAlertCircle, FiRefreshCw } from "react-icons/fi";

import "./ErrorState.css";

function ErrorState({
  title = "Something went wrong",
  message = "Unable to load data.",
  onRetry,
}) {
  return (
    <div className="error-state">
      <FiAlertCircle className="error-icon" />

      <h2>{title}</h2>

      <p>{message}</p>

      {onRetry && (
        <button className="retry-button" onClick={onRetry}>
          <FiRefreshCw />
          Retry
        </button>
      )}
    </div>
  );
}

export default ErrorState;
