import { useEffect, useState } from "react";
import api from "../api/axios";
import LogoutButton from "../components/LogoutButton";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  const [complaints, setComplaints] = useState([]);

  // filters
  const [statusFilter, setStatusFilter] = useState("");
  const [typeFilter, setTypeFilter] = useState("");
  const [ordering, setOrdering] = useState("-created_at");

  // pagination
  const [next, setNext] = useState(null);
  const [prev, setPrev] = useState(null);
  const [pageOffset, setPageOffset] = useState(0);

  const [selectedComplaint, setSelectedComplaint] = useState(null);
  const PAGE_SIZE = 2; // munual

  const [confirmComplaint, setConfirmComplaint] = useState(null);
  const [feedback, setFeedback] = useState("");

  const fetchComplaints = async (url = "/complaints/") => {
    try {
      const response =
        url === "/complaints/"
          ? await api.get(url, {
              params: {
                ...(statusFilter && { status: statusFilter }),
                ...(typeFilter && { complaint_type: typeFilter }),
                ordering,
              },
            })
          : await api.get(url);

      setComplaints(response.data.results);
      setNext(response.data.next);
      setPrev(response.data.previous);

      // CALCULATE OFFSET
      if (url.includes("page=")) {
        const page = Number(new URL(url).searchParams.get("page"));
        setPageOffset((page - 1) * PAGE_SIZE);
      } else {
        setPageOffset(0); // first page
      }
    } catch (err) {
      console.error("Failed to fetch complaints", err);
    }
  };

  useEffect(() => {
    fetchComplaints("/complaints/");
  }, [statusFilter, typeFilter, ordering]);


  // Helpers
  // -------------------------
  const statusBadge = (status) => {
    const map = {
      pending: "warning",
      in_progress: "info",
      resolved: "success",
    };
    return (
      <span className={`badge bg-${map[status]} text-capitalize`}>
        {status.replace("_", " ")}
      </span>
    );
  };


  // Render
  // -------------------------
  return (
    // <div className="container py-4" style={{ maxWidth: "1100px" }}>

    <div
      className="py-4"
      style={{
        backgroundColor: "#FFF5F2", // same soft light bg as admin
        minHeight: "100vh",
      }}
    >
      <div className="container" style={{ maxWidth: "1100px" }}>
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h2 className="fw-bold">My Complaints</h2>

          <div className="d-flex gap-2">
            <button
              className="btn btn-primary"
              onClick={() => navigate("/create-complaint")}
            >
              + Raise Complaint
            </button>

            <LogoutButton />
          </div>
        </div>

        {/* Filters */}
        <div className="row g-3 mb-3">
          <div className="col-md-4">
            <label className="form-label">Complaint Type</label>
            <select
              className="form-select"
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
            >
              <option value="">All</option>
              <option value="mess">Mess</option>
              <option value="electricity">Electricity</option>
              <option value="water">Water</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div className="col-md-4">
            <label className="form-label">Status</label>
            <select
              className="form-select"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="">All</option>
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
            </select>
          </div>

          <div className="col-md-4">
            <label className="form-label">Order By</label>
            <select
              className="form-select"
              value={ordering}
              onChange={(e) => setOrdering(e.target.value)}
            >
              <option value="-created_at">Newest First</option>
              <option value="created_at">Oldest First</option>
            </select>
          </div>
        </div>

        {/* Table */}
        <div className="card shadow-sm">
          <div className="table-responsive">
            <table className="table table-hover align-middle mb-0">
              <thead className="table-light">
                <tr>
                  <th>#</th>
                  <th>Type</th>
                  <th>Status</th>
                  <th>Admin Remark</th>
                  <th>Resolved On</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {complaints.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="text-center py-4">
                      No complaints found.
                    </td>
                  </tr>
                ) : (
                  complaints.map((c, index) => (
                    <tr key={c.complaint_id}>
                      <td>{pageOffset + index + 1}</td>
                      <td className="text-capitalize">{c.complaint_type}</td>
                      <td>{statusBadge(c.status)}</td>
                      <td style={{ maxWidth: 300 }}>
                        {c.latest_admin_remark || "—"}
                      </td>
                      <td>
                        {c.resolved_at
                          ? new Date(c.resolved_at).toLocaleDateString()
                          : "—"}
                      </td>
                      <td>
                        <div className="d-flex gap-2">
                          <button
                            className="btn btn-sm btn-outline-secondary"
                            onClick={() => setSelectedComplaint(c)}
                          >
                            Details
                          </button>

                          {c.status === "resolved" && !c.is_confirmed && (
                            <button
                              className="btn btn-sm btn-success"
                              onClick={() => setConfirmComplaint(c)}
                            >
                              Confirm Resolution
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Pagination */}
        <div className="d-flex justify-content-between mt-3">
          <button
            className="btn btn-outline-secondary"
            disabled={!prev}
            onClick={() => fetchComplaints(prev)}
          >
            ← Previous
          </button>

          <button
            className="btn btn-outline-secondary"
            disabled={!next}
            onClick={() => fetchComplaints(next)}
          >
            Next →
          </button>
        </div>

        {/* DETAILS MODAL */}
        {selectedComplaint && (
          <div
            className="modal fade show"
            style={{ display: "block", background: "rgba(0,0,0,0.5)" }}
          >
            <div className="modal-dialog modal-lg modal-dialog-centered">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title">Complaint Details</h5>
                  <button
                    className="btn-close"
                    onClick={() => setSelectedComplaint(null)}
                  ></button>
                </div>

                <div className="modal-body">
                  <div className="row g-3">
                    <div className="col-md-6">
                      <strong>Complaint ID</strong>
                      <p>{selectedComplaint.complaint_id}</p>
                    </div>

                    <div className="col-md-6">
                      <strong>Status</strong>
                      <p>{statusBadge(selectedComplaint.status)}</p>
                    </div>

                    <div className="col-md-6">
                      <strong>Type</strong>
                      <p className="text-capitalize">
                        {selectedComplaint.complaint_type}
                      </p>
                    </div>

                    <div className="col-md-6">
                      <strong>Priority</strong>
                      <p className="text-capitalize">
                        {selectedComplaint.priority}
                      </p>
                    </div>

                    <div className="col-md-6">
                      <strong>Created On</strong>
                      <p>
                        {new Date(
                          selectedComplaint.created_at,
                        ).toLocaleString()}
                      </p>
                    </div>

                    <div className="col-md-6">
                      <strong>Resolved On</strong>
                      <p>
                        {selectedComplaint.resolved_at
                          ? new Date(
                              selectedComplaint.resolved_at,
                            ).toLocaleString()
                          : "—"}
                      </p>
                    </div>

                    <div className="col-12">
                      <strong>Description</strong>
                      <p className="border rounded p-2 bg-light">
                        {selectedComplaint.description}
                      </p>
                    </div>

                    <div className="col-12">
                      <strong>Admin Remark</strong>
                      <p>{selectedComplaint.latest_admin_remark || "—"}</p>
                    </div>
                  </div>
                </div>

                <div className="modal-footer">
                  <button
                    className="btn btn-secondary"
                    onClick={() => setSelectedComplaint(null)}
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {confirmComplaint && (
          <div
            className="modal fade show"
            style={{ display: "block", background: "rgba(0,0,0,0.5)" }}
          >
            <div className="modal-dialog modal-dialog-centered">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title">Confirm Resolution</h5>
                  <button
                    className="btn-close"
                    onClick={() => setConfirmComplaint(null)}
                  />
                </div>

                <div className="modal-body">
                  <p>
                    Are you satisfied with the resolution of this complaint?
                  </p>

                  <textarea
                    className="form-control"
                    placeholder="Optional feedback (recommended)"
                    rows="3"
                    value={feedback}
                    onChange={(e) => setFeedback(e.target.value)}
                  />
                </div>

                <div className="modal-footer">
                  <button
                    className="btn btn-secondary"
                    onClick={() => setConfirmComplaint(null)}
                  >
                    Cancel
                  </button>

                  <button
                    className="btn btn-success"
                    onClick={async () => {
                      try {
                        await api.post(
                          `/complaints/${confirmComplaint.complaint_id}/confirm/`,
                          { feedback },
                        );

                        // ✅ OPTIMISTIC UPDATE (instant UX)
                        setComplaints((prev) =>
                          prev.map((c) =>
                            c.complaint_id === confirmComplaint.complaint_id
                              ? { ...c, is_confirmed: true }
                              : c,
                          ),
                        );

                        // optional refetch (keeps backend as source of truth)
                        fetchComplaints("/complaints/");

                        setConfirmComplaint(null);
                        setFeedback("");
                      } catch (err) {
                        alert("Confirmation failed");
                      }
                    }}
                  >
                    Confirm
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
