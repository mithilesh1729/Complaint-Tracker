import Modal from "../Modal";

import "./ConfirmDialog.css";

function ConfirmDialog({
  open,
  title = "Confirmation",
  message,
  confirmText = "Confirm",
  cancelText = "Cancel",
  loading = false,
  danger = false,
  onConfirm,
  onCancel,
}) {
  return (
    <Modal
      open={open}
      title={title}
      onClose={onCancel}
      footer={
        <>
          <button
            className="dialog-btn secondary"
            onClick={onCancel}
            disabled={loading}
          >
            {cancelText}
          </button>

          <button
            className={`dialog-btn ${danger ? "danger" : "primary"}`}
            onClick={onConfirm}
            disabled={loading}
          >
            {loading ? "Please wait..." : confirmText}
          </button>
        </>
      }
    >
      <p className="dialog-message">{message}</p>
    </Modal>
  );
}

export default ConfirmDialog;
