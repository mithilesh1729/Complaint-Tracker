import { useState, useEffect } from "react";
import useProfile from "../../hooks/useProfile";
import api from "../../api/axios";
import useToast from "../../hooks/useToast";
import PageHeader from "../../components/layout/PageHeader";
import Toast from "../../components/common/Toast/Toast";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import "./AdminProfile.css";

function AdminProfile() {
  const { profile, loading, refresh } = useProfile();
  const { toast, showToast } = useToast();

  const [profileData, setProfileData] = useState({
    name: "",
    phone_number: "",
  });

  const [passwordData, setPasswordData] = useState({
    old_password: "",
    new_password: "",
    confirm_password: "",
  });

  const [showOldPassword, setShowOldPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);

  useEffect(() => {
    if (profile) {
      setProfileData({
        name: profile.name || "",
        phone_number: profile.phone_number || "",
      });
    }
  }, [profile]);

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    try {
      await api.patch("/profile/", profileData);
      showToast("Profile updated successfully", "success");
      refresh();
    } catch (err) {
      showToast("Failed to update profile", "error");
    }
  };

  const handlePasswordUpdate = async (e) => {
    e.preventDefault();
    if (passwordData.new_password !== passwordData.confirm_password) {
      showToast("New passwords do not match", "error");
      return;
    }

    try {
      await api.post("/profile/password/", {
        old_password: passwordData.old_password,
        new_password: passwordData.new_password,
      });
      showToast("Password changed successfully", "success");
      setPasswordData({ old_password: "", new_password: "", confirm_password: "" });
    } catch (err) {
      showToast(err.response?.data?.detail || "Failed to change password", "error");
    }
  };

  if (loading) return <div className="p-4">Loading profile...</div>;

  return (
    <div className="admin-profile-page" style={{ padding: "32px" }}>
      <PageHeader 
        title="Admin Profile" 
        subtitle="Manage your personal details and security"
      />

      <div className="admin-profile-grid">
        <div className="admin-profile-card">
          <h3>Personal Information</h3>
          <form onSubmit={handleProfileUpdate}>
            <div className="form-group">
              <label>Admin ID / Roll No</label>
              <input type="text" value={profile?.roll_no || ""} disabled />
            </div>
            <div className="form-group">
              <label>Email Address</label>
              <input type="email" value={profile?.email || ""} disabled />
            </div>
            <div className="form-group">
              <label>Full Name</label>
              <input 
                type="text" 
                value={profileData.name} 
                onChange={(e) => setProfileData({...profileData, name: e.target.value})} 
              />
            </div>
            <div className="form-group" style={{ marginBottom: "32px" }}>
              <label>Phone Number</label>
              <input 
                type="text" 
                value={profileData.phone_number} 
                onChange={(e) => setProfileData({...profileData, phone_number: e.target.value})} 
              />
            </div>
            <button type="submit" className="table-action-button primary" style={{ width: "100%", padding: "14px", fontSize: "15px" }}>
              Update Profile
            </button>
          </form>
        </div>

        <div className="admin-profile-card">
          <h3>Change Password</h3>
          <form onSubmit={handlePasswordUpdate}>
            <div className="form-group" style={{ position: "relative" }}>
              <label>Current Password</label>
              <input 
                type={showOldPassword ? "text" : "password"} 
                required
                value={passwordData.old_password}
                onChange={(e) => setPasswordData({...passwordData, old_password: e.target.value})}
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
                required
                value={passwordData.new_password}
                onChange={(e) => setPasswordData({...passwordData, new_password: e.target.value})}
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
            <div className="form-group" style={{ marginBottom: "32px" }}>
              <label>Confirm New Password</label>
              <input 
                type="password"
                required
                value={passwordData.confirm_password}
                onChange={(e) => setPasswordData({...passwordData, confirm_password: e.target.value})}
              />
            </div>
            <button type="submit" className="table-action-button secondary" style={{ width: "100%", padding: "14px", fontSize: "15px", color: "var(--color-warning-text)", background: "var(--color-warning-bg)", borderColor: "var(--color-warning-text)" }}>
              Change Password
            </button>
          </form>
        </div>
      </div>

      <Toast {...toast} />
    </div>
  );
}

export default AdminProfile;
