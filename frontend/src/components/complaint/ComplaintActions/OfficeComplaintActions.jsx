import { useState } from "react";

import ConfirmDialog from "../../common/ConfirmDialog";
import TextareaDialog from "../../common/TextareaDialog";
import Toast from "../../common/Toast";

import useToast from "../../../hooks/useToast";
import useOfficeComplaintActions from "../../../hooks/useOfficeComplaintActions";

import "./ComplaintActions.css";

function OfficeComplaintActions({ complaint, refresh }) {
  const [assignOpen, setAssignOpen] = useState(false);

  const [progressOpen, setProgressOpen] = useState(false);
  const [resolveOpen, setResolveOpen] = useState(false);
  const [escalateOpen, setEscalateOpen] = useState(false);

  const { toast, showToast } = useToast();

  const {
    loading,
    assignComplaint,
    updateProgress,
    resolveComplaint,
    escalateComplaint,
    downloadSlip,
  } = useOfficeComplaintActions(refresh);

  async function handleAssign(remark) {
    const result = await assignComplaint(complaint.complaint_id, {
      remark,
    });

    if (result.success) {
      showToast("Complaint assigned successfully.");
      setAssignOpen(false);
    } else {
      showToast(result.message || "Unable to assign complaint.", "error");
    }
  }

  async function handleProgress(remark) {
    const result = await updateProgress(complaint.complaint_id, {
      priority: complaint.priority,
      remark,
    });

    if (result.success) {
      showToast("Progress updated.");
      setProgressOpen(false);
    } else {
      showToast(result.message || "Unable to update progress.", "error");
    }
  }

  async function handleResolve(remark) {
    const result = await resolveComplaint(complaint.complaint_id, {
      remark,
    });

    if (result.success) {
      showToast("Complaint resolved successfully.");
      setResolveOpen(false);
    } else {
      showToast(result.message || "Unable to resolve complaint.", "error");
    }
  }

  async function handleEscalate(remark) {
    const result = await escalateComplaint(complaint.complaint_id, {
      remark,
    });

    if (result.success) {
      showToast("Complaint escalated to Warden.");
      setEscalateOpen(false);
    } else {
      showToast(result.message || "Unable to escalate complaint.", "error");
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
      showToast("Unable to download complaint slip.", "error");
    }
  }

  return (
    <section className="complaint-actions">
      <h2>Office Actions</h2>

      <div className="action-card">
        <h3>Download Complaint Slip</h3>

        <p>Download a PDF copy of this complaint.</p>

        <button disabled={loading} onClick={handleDownload}>
          Download PDF
        </button>
      </div>

      {complaint.status === "pending" && (
        <div className="action-card">
          <h3>Assign Complaint</h3>

          <p>Accept responsibility for this complaint.</p>

          <button disabled={loading} onClick={() => setAssignOpen(true)}>
            Assign to Me
          </button>
        </div>
      )}

      {complaint.status === "in_progress" && (
        <>
          {/* <div className="action-card">
            <h3>Update Progress</h3>

            <p>Add a progress update for the student.</p>

            <button disabled={loading} onClick={() => setProgressOpen(true)}>
              Update Progress
            </button>
          </div> */}

          <div className="action-card success">
            <h3>Resolve Complaint</h3>
            <p>Mark this complaint as resolved.</p>
            <button disabled={loading} onClick={() => setResolveOpen(true)}>
              Resolve Complaint
            </button>
          </div>

          <div className="action-card error mt-3" style={{ borderLeft: '4px solid #f44336' }}>
            <h3>Escalate to Warden</h3>
            <p>If you cannot resolve this complaint, push it to the Warden.</p>
            <button disabled={loading} onClick={() => setEscalateOpen(true)}>
              Escalate Complaint
            </button>
          </div>
        </>
      )}

      <TextareaDialog
        open={assignOpen}
        title="Assign Complaint"
        label="Initial Remark"
        placeholder="Complaint accepted. Work has been scheduled..."
        confirmText="Assign"
        required
        loading={loading}
        onCancel={() => setAssignOpen(false)}
        onConfirm={handleAssign}
      />

      <TextareaDialog
        open={progressOpen}
        title="Update Progress"
        label="Progress Remark"
        placeholder="Describe the current progress..."
        confirmText="Update"
        required
        loading={loading}
        onCancel={() => setProgressOpen(false)}
        onConfirm={handleProgress}
      />

      <TextareaDialog
        open={resolveOpen}
        title="Resolve Complaint"
        label="Resolution Remark"
        placeholder="Describe how the complaint was resolved..."
        confirmText="Resolve"
        required
        loading={loading}
        onCancel={() => setResolveOpen(false)}
        onConfirm={handleResolve}
      />

      <TextareaDialog
        open={escalateOpen}
        title="Escalate to Warden"
        label="Escalation Remark"
        placeholder="Why are you escalating this complaint..."
        confirmText="Escalate"
        required
        loading={loading}
        onCancel={() => setEscalateOpen(false)}
        onConfirm={handleEscalate}
      />

      <Toast open={toast.open} type={toast.type} message={toast.message} />
    </section>
  );
}

export default OfficeComplaintActions;
