import { useState } from "react";
import api from "../../../api/axios";
import useToast from "../../../hooks/useToast";
import TextareaDialog from "../../common/TextareaDialog";
import Toast from "../../common/Toast";
import { useNavigate } from "react-router-dom";
import "./ComplaintActions.css";

function HMCComplaintActions({ complaint, refresh }) {
  const [remarkOpen, setRemarkOpen] = useState(false);
  const [returnOpen, setReturnOpen] = useState(false);
  const [forceCloseOpen, setForceCloseOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const { toast, showToast } = useToast();

  const handleAction = async (actionType, remark) => {
    try {
      setLoading(true);
      await api.post(`/hmc/complaints/${complaint.complaint_id}/action/`, {
        action: actionType,
        remark: remark
      });
      
      if (actionType !== "add_remark") {
        showToast("Complaint action performed successfully.");
        setTimeout(() => navigate("/hmc/queue"), 1000);
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
      <h2>HMC Actions</h2>

      {complaint.status === "escalated_hmc" && (
        <>
          <div className="action-card">
            <h3>Add Remark</h3>
            <p>Add a note to this complaint without changing its status.</p>
            <button disabled={loading} onClick={() => setRemarkOpen(true)}>
              Add Remark
            </button>
          </div>

          <div className="action-card success">
            <h3>Force Close</h3>
            <p>Directly resolve and close this escalated complaint globally.</p>
            <button disabled={loading} onClick={() => setForceCloseOpen(true)}>
              Force Close
            </button>
          </div>

          <div className="action-card error mt-3" style={{ borderLeft: '4px solid #f44336' }}>
            <h3>Send Back to Warden</h3>
            <p>Return this complaint down to the Hostel Warden.</p>
            <button disabled={loading} onClick={() => setReturnOpen(true)}>
              Send Back
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
        title="Return to Warden"
        label="Reason for Return"
        placeholder="Why is this being returned to the Warden..."
        confirmText="Return Complaint"
        required
        loading={loading}
        onCancel={() => setReturnOpen(false)}
        onConfirm={(val) => handleAction("return_warden", val)}
      />

      <TextareaDialog
        open={forceCloseOpen}
        title="Force Close Complaint"
        label="Closing Remark"
        placeholder="How was this complaint resolved..."
        confirmText="Force Close"
        required
        loading={loading}
        onCancel={() => setForceCloseOpen(false)}
        onConfirm={(val) => handleAction("close", val)}
      />

      <Toast open={toast.open} type={toast.type} message={toast.message} />
    </section>
  );
}

export default HMCComplaintActions;
