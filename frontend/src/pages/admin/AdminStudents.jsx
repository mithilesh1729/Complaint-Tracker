import { useState } from "react";
import useStudents from "../../hooks/useStudents";
import DataTable from "../../components/common/DataTable/DataTable";
import PageHeader from "../../components/layout/PageHeader";
import Toast from "../../components/common/Toast/Toast";
import UserCreateModal from "../../components/admin/UserCreateModal";
import UserEditModal from "../../components/admin/UserEditModal";
import api from "../../api/axios";
import useToast from "../../hooks/useToast";

function AdminStudents() {
  const { students, loading, error, pagination, fetchStudents } = useStudents();
  const { toast, showToast } = useToast();
  
  const [search, setSearch] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);

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
      showToast(res.data.message || "Password reset credentials sent via email.", "success");
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
            className="table-action-button primary" 
            onClick={() => {
              setSelectedUser(row);
              setIsEditModalOpen(true);
            }}
            title="Edit Student"
          >
            Edit
          </button>
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
        action={
          <button className="table-action-button primary" onClick={() => setIsModalOpen(true)}>
            + Add Student
          </button>
        }
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

      <UserCreateModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={() => {
          setIsModalOpen(false);
          showToast("Student created successfully. Credentials sent via email.", "success");
          fetchStudents();
        }}
        userType="student"
      />

      {selectedUser && (
        <UserEditModal 
          isOpen={isEditModalOpen}
          onClose={() => {
            setIsEditModalOpen(false);
            setSelectedUser(null);
          }}
          onSuccess={() => {
            setIsEditModalOpen(false);
            setSelectedUser(null);
            showToast("Student updated successfully.", "success");
            fetchStudents();
          }}
          userType="student"
          initialData={selectedUser}
        />
      )}
    </div>
  );
}

export default AdminStudents;
