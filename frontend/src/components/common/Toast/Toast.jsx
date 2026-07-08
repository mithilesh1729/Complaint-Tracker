import "./Toast.css";

function Toast({ open, type = "success", message }) {
  if (!open) return null;

  return <div className={`toast ${type}`}>{message}</div>;
}

export default Toast;
