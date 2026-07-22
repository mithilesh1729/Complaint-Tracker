import { useState } from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import api from "../../api/axios";

function ChangePasswordForm() {
  const [formData, setFormData] = useState({
    old_password: "",
    new_password: "",
    confirm_password: ""
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [showOldPassword, setShowOldPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    if (formData.new_password !== formData.confirm_password) {
      setError("New passwords do not match.");
      setLoading(false);
      return;
    }

    try {
      await api.post("/profile/password/", {
        old_password: formData.old_password,
        new_password: formData.new_password,
      });
      setSuccess("Password successfully changed!");
      setFormData({ old_password: "", new_password: "", confirm_password: "" });
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to change password. Ensure it's at least 8 chars with a letter and a number.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: "500px", marginTop: "20px" }}>
      <h3 style={{ marginBottom: "16px", fontWeight: "600" }}>Change Password</h3>
      
      {error && <div className="error-banner mb-3">{error}</div>}
      {success && <div className="success-banner mb-3" style={{ background: "var(--color-success-bg)", color: "var(--color-success-text)", padding: "12px", borderRadius: "var(--radius-md)" }}>{success}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group" style={{ position: "relative" }}>
          <label>Old Password</label>
          <input 
            type={showOldPassword ? "text" : "password"} 
            name="old_password" 
            value={formData.old_password} 
            onChange={handleChange} 
            required 
            style={{ paddingRight: "40px" }}
          />
          <button 
            type="button" 
            onClick={() => setShowOldPassword(!showOldPassword)}
            style={{ position: "absolute", right: "12px", top: "38px", background: "none", border: "none", cursor: "pointer", color: "var(--color-text-light)" }}
          >
            {showOldPassword ? <FaEyeSlash /> : <FaEye />}
          </button>
        </div>
        
        <div className="form-group" style={{ position: "relative" }}>
          <label>New Password</label>
          <input 
            type={showNewPassword ? "text" : "password"} 
            name="new_password" 
            value={formData.new_password} 
            onChange={handleChange} 
            required 
            style={{ paddingRight: "40px" }}
          />
          <button 
            type="button" 
            onClick={() => setShowNewPassword(!showNewPassword)}
            style={{ position: "absolute", right: "12px", top: "38px", background: "none", border: "none", cursor: "pointer", color: "var(--color-text-light)" }}
          >
            {showNewPassword ? <FaEyeSlash /> : <FaEye />}
          </button>
        </div>
        
        <div className="form-group">
          <label>Confirm New Password</label>
          <input 
            type="password" 
            name="confirm_password" 
            value={formData.confirm_password} 
            onChange={handleChange} 
            required 
          />
        </div>
        
        <button type="submit" className="table-action-button primary" disabled={loading} style={{ width: "100%", justifyContent: "center" }}>
          {loading ? "Updating..." : "Update Password"}
        </button>
      </form>
    </div>
  );
}

export default ChangePasswordForm;
