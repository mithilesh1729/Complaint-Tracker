import { useState, useMemo } from "react";
import useStaff from "../../hooks/useStaff";
import PageHeader from "../../components/layout/PageHeader";
import Toast from "../../components/common/Toast/Toast";
import api from "../../api/axios";
import useToast from "../../hooks/useToast";
import DataTable from "../../components/common/DataTable/DataTable";

function AdminStaff() {
  const { staff, loading, error, fetchStaff } = useStaff();
  const { toast, showToast } = useToast();
  
  const [search, setSearch] = useState("");

  const filteredStaff = useMemo(() => {
    if (!search) return staff;
    return staff.filter(s => 
      s.name.toLowerCase().includes(search.toLowerCase()) || 
      s.roll_no.toLowerCase().includes(search.toLowerCase())
    );
  }, [staff, search]);

  const handleToggleActive = async (rollNo, currentState) => {
    try {
      await api.delete(`/staff/${rollNo}/`);
      showToast(currentState ? "Staff deactivated" : "Staff activated", "success");
      fetchStaff();
    } catch (err) {
      showToast("Failed to change staff status", "error");
    }
  };

  const handleResetPassword = async (rollNo) => {
    try {
      const res = await api.post(`/staff/${rollNo}/reset-password/`);
      showToast(`Password reset! New Temp Pass: ${res.data.temporary_password}`, "success");
    } catch (err) {
      showToast("Failed to reset password", "error");
    }
  };

  const columns = [
    { header: "Staff ID", field: "roll_no" },
    { header: "Name", field: "name" },
    { header: "Role", field: "role" },
    { header: "Email", field: "email" },
    { header: "Phone", field: "phone_number" },
    { header: "Hostel", field: "hostel" },
    { 
      header: "Status", 
      render: (row) => (
        <span className={`status-badge ${row.is_active ? 'resolved' : 'reopened'}`}>
          {row.is_active ? "Active" : "Inactive"}
        </span>
      ) 
    },
    { 
      header: "Actions", 
      render: (row) => (
        <div className="table-actions">
          <button 
            className="table-action-button secondary" 
            onClick={() => handleResetPassword(row.roll_no)}
            title="Reset Password"
          >
            Reset
          </button>
          <button 
            className={`table-action-button ${row.is_active ? 'secondary' : 'primary'}`} 
            onClick={() => handleToggleActive(row.roll_no, row.is_active)}
            title={row.is_active ? "Deactivate" : "Activate"}
            style={row.is_active ? { color: "var(--color-danger)" } : {}}
          >
            {row.is_active ? "Disable" : "Enable"}
          </button>
        </div>
      ) 
    }
  ];

  return (
    <div className="p-4">
      <PageHeader 
        title="Staff Management" 
        subtitle="Manage hostel office and warden accounts"
      />

      <div className="complaint-table-container mb-4" style={{ padding: "20px" }}>
        <div style={{ display: "flex", gap: "8px" }}>
          <input 
            type="text" 
            className="search-input" 
            placeholder="Search by name or role..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ borderRadius: "var(--radius-md)" }}
          />
        </div>
      </div>

      <DataTable
        columns={columns}
        data={filteredStaff}
        keyField="roll_no"
        loading={loading}
      />
      
      <Toast {...toast} />
    </div>
  );
}

export default AdminStaff;
