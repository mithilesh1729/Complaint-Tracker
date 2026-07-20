import { useState } from "react";
import api from "../../../api/axios";
import useToast from "../../../hooks/useToast";
import ConfirmDialog from "../../common/ConfirmDialog";
import TextareaDialog from "../../common/TextareaDialog";
import Toast from "../../common/Toast";
import { useNavigate } from "react-router-dom";
import "./ComplaintActions.css";

function WardenComplaintActions({ complaint, refresh }) {
  const [remarkOpen, setRemarkOpen] = useState(false);
  const [returnOpen, setReturnOpen] = useState(false);
  const [escalateOpen, setEscalateOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const { toast, showToast } = useToast();

  const handleAction = async (actionType, remark) => {
    try {
      setLoading(true);
      await api.post(`/warden/complaints/${complaint.complaint_id}/action/`, {
        action: actionType,
        remark: remark
      });
      
      if (actionType !== "add_remark") {
        showToast("Complaint action performed successfully.");
        setTimeout(() => navigate("/warden/queue"), 1000);
      } else {
        showToast("Remark added successfully.");
        setRemarkOpen(false);
        refresh();
      }
    } catch (err) {
      showToast("Failed to perform action", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="complaint-actions">
      <h2>Warden Actions</h2>

      {complaint.status === "escalated_warden" && (
        <>
          <div className="action-card">
            <h3>Add Remark</h3>
            <p>Add a note to this complaint without changing its status.</p>
            <button disabled={loading} onClick={() => setRemarkOpen(true)}>
              Add Remark
            </button>
          </div>

          <div className="action-card success">
            <h3>Send Back to Office</h3>
            <p>Return this complaint to the hostel office to resolve.</p>
            <button disabled={loading} onClick={() => setReturnOpen(true)}>
              Send Back
            </button>
          </div>

          <div className="action-card error mt-3" style={{ borderLeft: '4px solid #f44336' }}>
            <h3>Escalate to HMC</h3>
            <p>Push this complaint up to the Hostel Management Committee.</p>
            <button disabled={loading} onClick={() => setEscalateOpen(true)}>
              Escalate to HMC
            </button>
          </div>
        </>
      )}

      <TextareaDialog
        open={remarkOpen}
        title="Add Remark"
        label="Remark"
        placeholder="Enter your note..."
        confirmText="Add Remark"
        required
        loading={loading}
        onCancel={() => setRemarkOpen(false)}
        onConfirm={(val) => handleAction("add_remark", val)}
      />

      <TextareaDialog
        open={returnOpen}
        title="Return to Office"
        label="Reason for Return"
        placeholder="Why is this being returned to the office..."
        confirmText="Return Complaint"
        required
        loading={loading}
        onCancel={() => setReturnOpen(false)}
        onConfirm={(val) => handleAction("send_back", val)}
      />

      <TextareaDialog
        open={escalateOpen}
        title="Escalate to HMC"
        label="Escalation Reason"
        placeholder="Why are you escalating this complaint..."
        confirmText="Escalate"
        required
        loading={loading}
        onCancel={() => setEscalateOpen(false)}
        onConfirm={(val) => handleAction("escalate_hmc", val)}
      />

      <Toast open={toast.open} type={toast.type} message={toast.message} />
    </section>
  );
}

export default WardenComplaintActions;
