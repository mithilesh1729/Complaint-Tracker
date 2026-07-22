import { useEffect, useState } from "react";

import Modal from "../Modal";

import "./TextareaDialog.css";

function TextareaDialog({
  open,
  title,
  label = "Message",
  placeholder = "",
  confirmText = "Submit",
  cancelText = "Cancel",
  initialValue = "",
  loading = false,
  required = false,
  maxLength = 500,
  onConfirm,
  onCancel,
  children,
}) {
  const [value, setValue] = useState("");

  useEffect(() => {
    if (open) {
      setValue(initialValue);
    }
  }, [open, initialValue]);

  function handleSubmit() {
    const text = value.trim();

    if (required && !text) {
      return;
    }

    onConfirm(text);
  }

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
            className="dialog-btn primary"
            onClick={handleSubmit}
            disabled={loading || (required && !value.trim())}
          >
            {loading ? "Please wait..." : confirmText}
          </button>
        </>
      }
    >
      {children}
      <label className="textarea-label">{label}</label>

      <textarea
        className="dialog-textarea"
        rows={6}
        value={value}
        maxLength={maxLength}
        placeholder={placeholder}
        onChange={(e) => setValue(e.target.value)}
      />

      <div className="textarea-footer">
        <span>{required ? "Required" : "Optional"}</span>

        <span>
          {value.length}/{maxLength}
        </span>
      </div>
    </Modal>
  );
}

export default TextareaDialog;
