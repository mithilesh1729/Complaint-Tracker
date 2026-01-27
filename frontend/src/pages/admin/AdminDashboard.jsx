import { useEffect, useState, useRef } from "react";
import api from "../../api/axios";
import { useNavigate } from "react-router-dom";
import AdminComplaintModal from "../../components/AdminComplaintModal";

function AdminDashboard() {
  const navigate = useNavigate();

  // ---------------- STATE ----------------
  const [complaints, setComplaints] = useState([]);
  const [selectedComplaint, setSelectedComplaint] = useState(null);

  const [statusFilter, setStatusFilter] = useState("");
  const [typeFilter, setTypeFilter] = useState("");
  const [ordering, setOrdering] = useState("-created_at");

  const [next, setNext] = useState(null);
  const [prev, setPrev] = useState(null);
  const [currentPageUrl, setCurrentPageUrl] = useState("/complaints/");

  const didInitialFetch = useRef(false);

  // ---------------- HELPERS ----------------
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

  // ---------------- FETCH ----------------
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
      setCurrentPageUrl(url);
    } catch (err) {
      console.error("Failed to fetch complaints", err);
    }
  };

  useEffect(() => {
    if (!didInitialFetch.current) {
      didInitialFetch.current = true;
      fetchComplaints("/complaints/");
      return;
    }

    const timeout = setTimeout(() => {
      fetchComplaints("/complaints/");
    }, 300);

    return () => clearTimeout(timeout);
  }, [statusFilter, typeFilter, ordering]);

  // ---------------- RENDER ----------------
  return (
    <div
      className="py-4"
      style={{
        minHeight: "100vh",
        background: "#FFF5F2",
      }}
    >
      <div className="container" style={{ maxWidth: "1400px" }}>
        <div className="container py-4" style={{ maxWidth: "1400px" }}>
          {/* Header */}
          {/* <div className="d-flex justify-content-between align-items-center mb-4">
            <h2 className="fw-bold">Admin Dashboard</h2>
            <button
              className="btn btn-outline-danger"
              onClick={() => {
                localStorage.clear();
                navigate("/", { replace: true });
              }}
            >
              Logout
            </button>
          </div> */}

          <div className="position-relative mb-4 text-center">
            <h2 className="fw-bold">Admin Dashboard</h2>

            <button
              className="btn btn-outline-danger position-absolute end-0 top-50 translate-middle-y"
              onClick={() => {
                localStorage.clear();
                navigate("/", { replace: true });
              }}
            >
              Logout
            </button>
          </div>

          {/* Filters */}

          <div className="card shadow-sm mb-4">
            <div className="card-body row g-3">
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
          </div>

          {/* Table */}
          <div className="card shadow-sm">
            <div className="table-responsive">
              <table className="table table-hover align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>#</th>
                    <th>ID</th>
                    <th>User</th>
                    <th>Hostel</th>
                    <th>Room</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Action</th>
                    <th>Student Confirmed</th>
                  </tr>
                </thead>

                <tbody>
                  {complaints.length === 0 ? (
                    <tr>
                      <td colSpan="8" className="text-center py-4">
                        No complaints found.
                      </td>
                    </tr>
                  ) : (
                    complaints.map((c, index) => (
                      <tr key={c.complaint_id}>
                        <td>{index + 1}</td>
                        <td>{c.complaint_id.slice(0, 8)}</td>
                        <td>{c.name}</td>
                        <td>{c.hostel}</td>
                        <td>{c.room_no}</td>
                        <td>{c.complaint_type}</td>
                        <td>{statusBadge(c.status)}</td>
                        <td>
                          <button
                            className="btn btn-sm btn-outline-secondary"
                            onClick={() => setSelectedComplaint(c)}
                          >
                            Manage
                          </button>
                        </td>
                        <td>
                          {c.is_confirmed ? (
                            <span className="badge bg-success-subtle text-success">
                              ✓ Confirmed
                            </span>
                          ) : c.status === "resolved" ? (
                            <span className="badge bg-warning-subtle text-warning">
                              ⏳ Awaiting Student
                            </span>
                          ) : (
                            "—"
                          )}
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

          {/* Modal */}
          {selectedComplaint && (
            <AdminComplaintModal
              complaint={selectedComplaint}
              onClose={() => setSelectedComplaint(null)}
              onUpdated={() => fetchComplaints(currentPageUrl)}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
