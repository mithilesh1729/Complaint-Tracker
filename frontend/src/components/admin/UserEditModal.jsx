import { useState, useEffect } from "react";
import api from "../../api/axios";
import "./UserCreateModal.css"; // Reuse same CSS for layout

function UserEditModal({ isOpen, onClose, onSuccess, userType, initialData }) {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone_number: "",
    department: "",
    hostel: "",
    room_no: "",
  });

  const [hostels, setHostels] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (isOpen && initialData) {
      setFormData({
        name: initialData.name || "",
        email: initialData.email || "",
        phone_number: initialData.phone_number || "",
        department: initialData.department_id || initialData.department || "",
        hostel: initialData.hostel_id || initialData.hostel || "",
        room_no: initialData.room_no || "",
      });
      fetchHostels();
      if (userType === "student") {
        fetchDepartments();
      }
    }
  }, [isOpen, initialData, userType]);

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
      // Find the ID values if the current values are text names
      let hostelId = formData.hostel;
      if (typeof hostelId === "string" && isNaN(Number(hostelId))) {
        const found = hostels.find((h) => h.name === hostelId);
        if (found) hostelId = found.id;
      }
      
      let deptId = formData.department;
      if (typeof deptId === "string" && isNaN(Number(deptId))) {
        const found = departments.find((d) => d.code === deptId || d.name === deptId);
        if (found) deptId = found.id;
      }

      const endpoint = userType === "student" ? `/students/${initialData.roll_no}/` : `/staff/${initialData.roll_no}/`;
      
      const payload = {
        name: formData.name,
        email: formData.email,
        phone_number: formData.phone_number,
        hostel: hostelId,
      };

      if (userType === "student") {
        payload.room_no = formData.room_no;
        if (deptId) {
          payload.department = deptId;
        }
      }

      await api.patch(endpoint, payload);
      onSuccess(); 
    } catch (err) {
      const responseData = err.response?.data;
      if (responseData && typeof responseData === 'object' && !responseData.detail) {
        const firstKey = Object.keys(responseData)[0];
        const firstError = responseData[firstKey][0];
        const fieldName = firstKey.replace('_', ' ').toUpperCase();
        setError(`${fieldName}: ${firstError}`);
      } else {
        setError(responseData?.detail || "Failed to update user");
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
          <h2>Edit {userType === "student" ? "Student" : "Staff"}</h2>
          <button className="close-button" onClick={onClose}>&times;</button>
        </div>
        
        {error && <div className="error-banner">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <div className="modal-form-grid">
              
              <div className="form-group full-width" style={{ background: "var(--color-background)", padding: "12px", borderRadius: "8px" }}>
                <label style={{ margin: 0, fontSize: "12px", color: "var(--color-text-secondary)" }}>
                  {userType === "student" ? "Roll No" : "Staff ID"} (Immutable)
                </label>
                <div style={{ fontWeight: "600", fontSize: "16px", marginTop: "4px" }}>
                  {initialData?.roll_no}
                </div>
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
                  {hostels.map(h => (
                    <option key={h.id} value={h.id}>{h.name}</option>
                  ))}
                  {/* Fallback if hostel name is prefilled but not found in ID map initially */}
                  {typeof formData.hostel === "string" && isNaN(Number(formData.hostel)) && (
                    <option value={formData.hostel}>{formData.hostel}</option>
                  )}
                </select>
              </div>

              {userType === "student" && (
                <div className="form-group">
                  <label>Room Number</label>
                  <input name="room_no" value={formData.room_no} onChange={handleChange} required />
                </div>
              )}
            </div>
          </div>

          <div className="modal-actions">
            <button type="button" className="table-action-button secondary" onClick={onClose}>Cancel</button>
            <button type="submit" className="table-action-button primary" disabled={loading}>
              {loading ? "Saving..." : "Save Changes"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default UserEditModal;
