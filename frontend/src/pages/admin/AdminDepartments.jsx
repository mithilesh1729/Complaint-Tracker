import { useState } from "react";
import useDepartments from "../../hooks/useDepartments";
import DataTable from "../../components/common/DataTable/DataTable";
import PageHeader from "../../components/layout/PageHeader";
import Modal from "../../components/common/Modal/Modal";
import api from "../../api/axios";
import useToast from "../../hooks/useToast";
import Toast from "../../components/common/Toast/Toast";

function AdminDepartments() {
  const { departments, loading, fetchDepartments } = useDepartments();
  const { toast, showToast } = useToast();
  
  const [search, setSearch] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingDepartment, setEditingDepartment] = useState(null);
  const [formData, setFormData] = useState({ code: "", name: "" });

  const handleSearch = (e) => {
    e.preventDefault();
    fetchDepartments(search);
  };

  const handleOpenModal = (department = null) => {
    if (department) {
      setEditingDepartment(department);
      setFormData({ code: department.code, name: department.name });
    } else {
      setEditingDepartment(null);
      setFormData({ code: "", name: "" });
    }
    setIsModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingDepartment) {
        await api.patch(`/admin/departments/${editingDepartment.id}/`, formData);
        showToast("Department updated successfully", "success");
      } else {
        await api.post("/admin/departments/", formData);
        showToast("Department created successfully", "success");
      }
      setIsModalOpen(false);
      fetchDepartments(search);
    } catch (err) {
      showToast(err.response?.data?.detail || err.response?.data?.code?.[0] || "Failed to save department", "error");
    }
  };

  const handleToggleActive = async (id, currentState) => {
    try {
      await api.delete(`/admin/departments/${id}/`);
      showToast(currentState ? "Department deactivated" : "Department activated", "success");
      fetchDepartments(search);
    } catch (err) {
      showToast("Failed to change department status", "error");
    }
  };

  const columns = [
    { header: "ID", field: "id" },
    { header: "Code", field: "code" },
    { header: "Department Name", field: "name" },
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
            onClick={() => handleOpenModal(row)}
          >
            Edit
          </button>
          <button 
            className={`table-action-button ${row.is_active ? 'secondary' : 'primary'}`} 
            onClick={() => handleToggleActive(row.id, row.is_active)}
            style={row.is_active ? { color: "var(--color-danger)" } : {}}
          >
            {row.is_active ? "Disable" : "Enable"}
          </button>
        </div>
      ) 
    }
  ];

  return (
    <div className="admin-profile-page" style={{ padding: "32px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
        <PageHeader 
          title="Department Management" 
          subtitle="Manage department master data" 
        />
        <button className="table-action-button primary" onClick={() => handleOpenModal()} style={{ padding: "10px 20px" }}>
          + New Department
        </button>
      </div>

      <div className="complaint-table-container mb-4" style={{ padding: "20px" }}>
        <form style={{ display: "flex", gap: "8px" }} onSubmit={handleSearch}>
          <input 
            type="text" 
            className="search-input" 
            placeholder="Search departments by name or code..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button className="table-action-button primary" type="submit" style={{ padding: "0 24px" }}>Search</button>
        </form>
      </div>

      <DataTable 
        columns={columns} 
        data={departments}
        keyField="id" 
        loading={loading}
      />

      <Modal 
        open={isModalOpen} 
        onClose={() => setIsModalOpen(false)}
        title={editingDepartment ? "Edit Department" : "Add New Department"}
      >
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Department Code (e.g., CSE)</label>
            <input 
              type="text" 
              required
              value={formData.code}
              onChange={(e) => setFormData({...formData, code: e.target.value})}
            />
          </div>
          <div className="form-group">
            <label>Department Name</label>
            <input 
              type="text" 
              required 
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
            />
          </div>
          
          <div className="modal-actions" style={{ display: "flex", justifyContent: "flex-end", gap: "12px", marginTop: "24px" }}>
            <button type="button" className="table-action-button secondary" onClick={() => setIsModalOpen(false)}>
              Cancel
            </button>
            <button type="submit" className="table-action-button primary">
              {editingDepartment ? "Update" : "Create"}
            </button>
          </div>
        </form>
      </Modal>

      {toast.isVisible && (
        <Toast 
          message={toast.message} 
          type={toast.type} 
          onClose={() => showToast("", "")} 
        />
      )}
    </div>
  );
}

export default AdminDepartments;
