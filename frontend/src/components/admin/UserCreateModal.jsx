import { useState, useEffect } from "react";
import api from "../../api/axios";
import "./UserCreateModal.css";

function UserCreateModal({ isOpen, onClose, onSuccess, userType }) {
  const [formData, setFormData] = useState({
    roll_no: "",
    name: "",
    email: "",
    phone_number: "",
    department: "",
    hostel: "",
    room_no: "",
    role: userType === "staff" ? "hostel_office" : "student",
  });

  const [hostels, setHostels] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (isOpen) {
      fetchHostels();
      if (userType === "student") {
        fetchDepartments();
      }
    }
  }, [isOpen, userType]);

  const fetchHostels = async () => {
    try {
      const res = await api.get("/admin/hostels/");
      setHostels(res.data.results || res.data);
    } catch (err) {
      console.error("Failed to load hostels");
    }
  };

  const fetchDepartments = async () => {
    try {
      const res = await api.get("/admin/departments/");
      setDepartments(res.data.results || res.data);
    } catch (err) {
      console.error("Failed to load departments");
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const endpoint = userType === "student" ? "/students/" : "/staff/";
      const payload = { ...formData };

      // If it's a student, hostel is passed as an ID by the form but we might need name or ID depending on API
      // The backend StudentCreateSerializer expects hostel PrimaryKey (ID) or name?
      // Actually, looking at serializer, it expects the PrimaryKey.

      await api.post(endpoint, payload);
      onSuccess(); // Close and refresh
    } catch (err) {
      const responseData = err.response?.data;
      if (responseData && typeof responseData === 'object' && !responseData.detail) {
        // Extract the first field-level error from DRF format (e.g., {"roll_no": ["exists"]})
        const firstKey = Object.keys(responseData)[0];
        const firstError = responseData[firstKey][0];
        // Formatting field name to be slightly more readable
        const fieldName = firstKey.replace('_', ' ').toUpperCase();
        setError(`${fieldName}: ${firstError}`);
      } else {
        setError(responseData?.detail || "Failed to create user");
      }
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Create New {userType === "student" ? "Student" : "Staff"}</h2>
          <button className="close-button" onClick={onClose}>
            &times;
          </button>
        </div>

        {error && <div className="error-banner">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <div className="modal-form-grid">
              <div className="form-group">
                <label>{userType === "student" ? "Roll No" : "Staff ID"}</label>
                <input 
                  name="roll_no" 
                  value={formData.roll_no} 
                  onChange={handleChange} 
                  required 
                  pattern="[a-zA-Z0-9]+" 
                  title="Alphanumeric characters only, no spaces"
                />
              </div>

              <div className="form-group">
                <label>Full Name</label>
                <input name="name" value={formData.name} onChange={handleChange} required />
              </div>

              <div className="form-group">
                <label>Email</label>
                <input 
                  type="email" 
                  name="email" 
                  value={formData.email} 
                  onChange={handleChange} 
                  required 
                  pattern=".*@nitp\.ac\.in$"
                  title="Email must end with @nitp.ac.in"
                />
              </div>

              <div className="form-group">
                <label>Phone Number</label>
                <input 
                  name="phone_number" 
                  value={formData.phone_number} 
                  onChange={handleChange} 
                  required 
                  pattern="[0-9]{10}"
                  title="Exactly 10 digits"
                />
              </div>

              {userType === "student" && (
                <div className="form-group">
                  <label>Department</label>
                  <select name="department" value={formData.department} onChange={handleChange} required>
                    <option value="">Select Department</option>
                    {departments.map(d => (
                      <option key={d.id} value={d.id}>{d.name}</option>
                    ))}
                  </select>
                </div>
              )}

              <div className="form-group">
                <label>Hostel Assignment</label>
                <select
                  name="hostel"
                  value={formData.hostel}
                  onChange={handleChange}
                  required={!(userType === "staff" && formData.role === "hmc")}
                  disabled={userType === "staff" && formData.role === "hmc"}
                >
                  <option value="">Select Hostel</option>
                  {hostels.map((h) => (
                    <option key={h.id} value={h.id}>
                      {h.name}
                    </option>
                  ))}
                </select>
              </div>

              {userType === "student" && (
                <div className="form-group">
                  <label>Room Number</label>
                  <input
                    name="room_no"
                    value={formData.room_no}
                    onChange={handleChange}
                    required
                  />
                </div>
              )}

              {userType === "staff" && (
                <div className="form-group">
                  <label>Role</label>
                  <select
                    name="role"
                    value={formData.role}
                    onChange={handleChange}
                    required
                  >
                    <option value="hostel_office">Hostel Office</option>
                    <option value="warden">Warden</option>
                    <option value="hmc">HMC Admin</option>
                  </select>
                </div>
              )}
            </div>
          </div>

          <div className="modal-actions">
            <button
              type="button"
              className="table-action-button secondary"
              onClick={onClose}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="table-action-button primary"
              disabled={loading}
            >
              {loading ? "Creating..." : "Create User"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default UserCreateModal;
