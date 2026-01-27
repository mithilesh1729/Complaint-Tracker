import { useEffect, useState } from "react";
import api from "../api/axios";
import { downloadComplaintSlip } from "../api/downloadSlip";

function AdminComplaintModal({ complaint, onClose, onUpdated }) {
  const [status, setStatus] = useState(complaint.status);
  const [priority, setPriority] = useState(complaint.priority);
  const [remark, setRemark] = useState("");
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch status logs
  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await api.get(
          `/complaints/${complaint.complaint_id}/logs/`,
        );
        setLogs(res.data);
      } catch {
        console.error("Failed to fetch logs");
      }
    };

    fetchLogs();
  }, [complaint.complaint_id]);

  // Update complaint
  const handleUpdate = async () => {
    setLoading(true);
    try {
      await api.patch(`/complaints/${complaint.complaint_id}/update/`, {
        status,
        priority,
        message: remark || "Status updated",
      });

      onUpdated(); // refresh list
      onClose(); // close modal
    } catch {
      alert("Update failed");
    } finally {
      setLoading(false);
    }
  };

  // Render
  return (
    <div
      className="modal fade show"
      style={{ display: "block", background: "rgba(0,0,0,0.5)" }}
    >
      <div className="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
        <div className="modal-content">
          {/* Header */}
          <div className="modal-header">
            <h5 className="modal-title">Complaint Details</h5>
            <button className="btn-close" onClick={onClose}></button>
          </div>

          {/* Body */}
          <div className="modal-body">
            {/* Basic Info */}
            <div className="row g-3 mb-3">
              <div className="col-md-6">
                <strong>Complaint ID</strong>
                <p>{complaint.complaint_id}</p>
              </div>

              <div className="col-md-6">
                <strong>Student</strong>
                <p>
                  {complaint.name} ({complaint.user.roll_no})
                </p>
              </div>

              <div className="col-md-6">
                <strong>Hostel / Room</strong>
                <p>
                  {complaint.hostel} - {complaint.room_no}
                </p>
              </div>

              <div className="col-md-6">
                <strong>Type</strong>
                <p className="text-capitalize">{complaint.complaint_type}</p>
              </div>

              <div className="col-md-6">
                <strong>Created On</strong>
                <p>{new Date(complaint.created_at).toLocaleString()}</p>
              </div>

              <div className="col-md-6">
                <strong>Resolved On</strong>
                <p>
                  {complaint.resolved_at
                    ? new Date(complaint.resolved_at).toLocaleString()
                    : "—"}
                </p>
              </div>

              <div className="col-md-6">
                <strong>Student Confirmation</strong>
                <p>
                  {complaint.is_confirmed ? (
                    <>
                      <span className="badge bg-success">Confirmed</span>
                      <br />
                      <small className="text-muted">
                        {complaint.confirmed_at
                          ? new Date(complaint.confirmed_at).toLocaleString()
                          : ""}
                      </small>
                    </>
                  ) : (
                    <span className="badge bg-warning text-dark">Pending</span>
                  )}
                </p>
              </div>
            </div>

            {/* Description */}
            <div className="mb-3">
              <strong>Description</strong>
              <p className="border rounded p-2 bg-light">
                {complaint.description}
              </p>
            </div>

            {/* Editable Controls */}
            <div className="row g-3 mb-3">
              <div className="col-md-6">
                <label className="form-label">Status</label>
                <select
                  className="form-select"
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                >
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="resolved">Resolved</option>
                </select>
              </div>

              <div className="col-md-6">
                <label className="form-label">Priority</label>
                <select
                  className="form-select"
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
            </div>

            <div className="mb-3">
              <label className="form-label">Admin Remark</label>
              <textarea
                className="form-control"
                rows="3"
                value={remark}
                onChange={(e) => setRemark(e.target.value)}
                placeholder="Action taken / instructions"
              />
            </div>

            {complaint.student_feedback && (
              <div className="mb-3">
                <strong>Student Feedback</strong>
                <p className="border rounded p-2 bg-light">
                  {complaint.student_feedback}
                </p>
              </div>
            )}

            {/* Logs */}
            <div>
              <strong>Status History</strong>
              <ul className="list-group mt-2">
                {logs.map((log, idx) => (
                  <li key={idx} className="list-group-item">
                    <strong>{log.status}</strong> — {log.message}
                    <br />
                    <small className="text-muted">
                      {new Date(log.timestamp).toLocaleString()}
                    </small>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Footer */}
          <div className="modal-footer">
            <button
              className="btn btn-outline-secondary"
              onClick={() => downloadComplaintSlip(complaint.complaint_id)}
            >
              Download Slip
            </button>

            <button className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>

            <button
              className="btn btn-primary"
              onClick={handleUpdate}
              disabled={loading}
            >
              {loading ? "Saving..." : "Save Changes"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminComplaintModal;
