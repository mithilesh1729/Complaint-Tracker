import { useState } from "react";

import useComplaintActions from "../../../hooks/useComplaintActions";
import useToast from "../../../hooks/useToast";

import ConfirmDialog from "../../common/ConfirmDialog";
import TextareaDialog from "../../common/TextareaDialog";
import Toast from "../../common/Toast";

import "./ComplaintActions.css";

function ComplaintActions({ complaint, refresh }) {
  const [confirmOpen, setConfirmOpen] = useState(false);

  const [reopenOpen, setReopenOpen] = useState(false);

  const { toast, showToast } = useToast();

  const { loading, downloadSlip, confirmComplaint, reopenComplaint } =
    useComplaintActions(refresh);

  async function handleConfirm() {
    const result = await confirmComplaint(complaint.complaint_id);

    if (result.success) {
      showToast("Complaint confirmed successfully.");

      setConfirmOpen(false);

      // refresh() already called inside hook
    } else {
      showToast("Unable to confirm complaint.", "error");
    }
  }

  async function handleReopen(feedback) {
    const result = await reopenComplaint(complaint.complaint_id, feedback);

    if (result.success) {
      showToast("Complaint reopened successfully.");

      setReopenOpen(false);
    } else {
      showToast("Unable to reopen complaint.", "error");
    }
  }

  async function handleDownload() {
    const result = await downloadSlip(
      complaint.complaint_id,
      complaint.complaint_number,
    );

    if (result.success) {
      showToast("Complaint slip downloaded.");
    } else {
      showToast("Unable to download slip.", "error");
    }
  }

  return (
    <section className="complaint-actions">
      <h2>Actions</h2>

      <div className="action-card">
        <h3>Download Complaint Slip</h3>

        <p>Download a PDF copy of this complaint.</p>

        <button onClick={handleDownload} disabled={loading}>
          Download PDF
        </button>
      </div>

      {complaint.status === "resolved" && !complaint.is_confirmed && (
        <>
          <div className="action-card success">
            <h3>Confirm Resolution</h3>

            <p>Confirm if your issue has been resolved successfully.</p>

            <button disabled={loading} onClick={() => setConfirmOpen(true)}>
              Confirm Resolution
            </button>
          </div>

          <div className="action-card warning">
            <h3>Still Facing the Issue?</h3>

            <p>Reopen this complaint if the problem still exists.</p>

            <button disabled={loading} onClick={() => setReopenOpen(true)}>
              Reopen Complaint
            </button>
          </div>
        </>
      )}

      <ConfirmDialog
        open={confirmOpen}
        title="Confirm Resolution"
        message="Are you sure your complaint has been resolved? This action cannot be undone."
        confirmText="Confirm"
        loading={loading}
        onCancel={() => setConfirmOpen(false)}
        onConfirm={handleConfirm}
      />

      <TextareaDialog
        open={reopenOpen}
        title="Reopen Complaint"
        label="Reason"
        placeholder="Describe why this complaint should be reopened..."
        confirmText="Reopen"
        required
        loading={loading}
        onCancel={() => setReopenOpen(false)}
        onConfirm={handleReopen}
      />

      <Toast open={toast.open} type={toast.type} message={toast.message} />
    </section>
  );
}

export default ComplaintActions;
