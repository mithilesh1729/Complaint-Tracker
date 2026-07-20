import { useState } from "react";
import useStudents from "../../hooks/useStudents";
import DataTable from "../../components/common/DataTable/DataTable";
import PageHeader from "../../components/layout/PageHeader";
import Toast from "../../components/common/Toast/Toast";
import api from "../../api/axios";
import useToast from "../../hooks/useToast";

function AdminStudents() {
  const { students, loading, error, pagination, fetchStudents } = useStudents();
  const { toast, showToast } = useToast();
  
  const [search, setSearch] = useState("");

  const handleSearch = (e) => {
    e.preventDefault();
    fetchStudents("/students/", { search });
  };

  const handleToggleActive = async (rollNo, currentState) => {
    try {
      await api.delete(`/students/${rollNo}/`);
      showToast(currentState ? "Student deactivated" : "Student activated", "success");
      fetchStudents();
    } catch (err) {
      showToast("Failed to change student status", "error");
    }
  };

  const handleResetPassword = async (rollNo) => {
    try {
      const res = await api.post(`/students/${rollNo}/reset-password/`);
      showToast(`Password reset! New Temp Pass: ${res.data.temporary_password}`, "success");
    } catch (err) {
      showToast("Failed to reset password", "error");
    }
  };

  const columns = [
    { header: "Roll No", field: "roll_no" },
    { header: "Name", field: "name" },
    { header: "Email", field: "email" },
    { header: "Phone", field: "phone_number" },
    { header: "Hostel", field: "hostel" },
    { header: "Room", field: "room_no" },
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
        title="Student Management" 
        subtitle="Manage student accounts and access"
      />

      <div className="complaint-table-container mb-4" style={{ padding: "20px" }}>
        <form style={{ display: "flex", gap: "8px" }} onSubmit={handleSearch}>
          <input 
            type="text" 
            className="search-input" 
            placeholder="Search by name or roll no..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ borderRadius: "var(--radius-md)" }}
          />
          <button className="table-action-button primary" type="submit" style={{ padding: "0 24px" }}>Search</button>
        </form>
      </div>

      <DataTable
        columns={columns}
        data={students}
        keyField="roll_no"
        loading={loading}
        pagination={pagination}
        onPageChange={(url) => fetchStudents(url)}
      />
      
      <Toast {...toast} />
    </div>
  );
}

export default AdminStudents;
