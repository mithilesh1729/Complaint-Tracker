import { useState } from "react";
import useHostels from "../../hooks/useHostels";
import DataTable from "../../components/common/DataTable/DataTable";
import PageHeader from "../../components/layout/PageHeader";
import Modal from "../../components/common/Modal/Modal";
import api from "../../api/axios";
import useToast from "../../hooks/useToast";
import Toast from "../../components/common/Toast/Toast";

function AdminHostels() {
  const { hostels, loading, fetchHostels } = useHostels();
  const { toast, showToast } = useToast();
  
  const [search, setSearch] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingHostel, setEditingHostel] = useState(null);
  const [formData, setFormData] = useState({ name: "", office_phone: "" });

  const handleSearch = (e) => {
    e.preventDefault();
    fetchHostels(search);
  };

  const handleOpenModal = (hostel = null) => {
    if (hostel) {
      setEditingHostel(hostel);
      setFormData({ name: hostel.name, office_phone: hostel.office_phone });
    } else {
      setEditingHostel(null);
      setFormData({ name: "", office_phone: "" });
    }
    setIsModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingHostel) {
        await api.patch(`/admin/hostels/${editingHostel.id}/`, formData);
        showToast("Hostel updated successfully", "success");
      } else {
        await api.post("/admin/hostels/", formData);
        showToast("Hostel created successfully", "success");
      }
      setIsModalOpen(false);
      fetchHostels(search);
    } catch (err) {
      showToast(err.response?.data?.detail || "Failed to save hostel", "error");
    }
  };

  const handleToggleActive = async (id, currentState) => {
    try {
      await api.delete(`/admin/hostels/${id}/`);
      showToast(currentState ? "Hostel deactivated" : "Hostel activated", "success");
      fetchHostels(search);
    } catch (err) {
      showToast("Failed to change hostel status", "error");
    }
  };

  const columns = [
    { header: "ID", field: "id" },
    { header: "Hostel Name", field: "name" },
    { header: "Office Phone", field: "office_phone" },
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
          title="Hostel Management" 
          subtitle="Manage hostel master data and infrastructure"
        />
        <button className="table-action-button primary" onClick={() => handleOpenModal()} style={{ padding: "10px 20px" }}>
          + New Hostel
        </button>
      </div>

      <div className="complaint-table-container mb-4" style={{ padding: "20px" }}>
        <form style={{ display: "flex", gap: "8px" }} onSubmit={handleSearch}>
          <input 
            type="text" 
            className="search-input" 
            placeholder="Search hostels by name..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button className="table-action-button primary" type="submit" style={{ padding: "0 24px" }}>Search</button>
        </form>
      </div>

      <DataTable
        columns={columns}
        data={hostels}
        keyField="id"
        loading={loading}
      />

      <Modal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingHostel ? "Edit Hostel" : "Add New Hostel"}
      >
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Hostel Name</label>
            <input 
              type="text" 
              required
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              placeholder="e.g. Ganga Hostel"
            />
          </div>
          <div className="form-group mb-4">
            <label>Office Phone Number (Optional)</label>
            <input 
              type="text" 
              value={formData.office_phone}
              onChange={(e) => setFormData({...formData, office_phone: e.target.value})}
              placeholder="e.g. +91 9876543210"
            />
          </div>
          
          <div style={{ display: "flex", justifyContent: "flex-end", gap: "8px" }}>
            <button 
              type="button" 
              className="table-action-button secondary" 
              onClick={() => setIsModalOpen(false)}
              style={{ padding: "10px 20px" }}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="table-action-button primary"
              style={{ padding: "10px 20px" }}
            >
              {editingHostel ? "Update Hostel" : "Create Hostel"}
            </button>
          </div>
        </form>
      </Modal>

      <Toast {...toast} />
    </div>
  );
}

export default AdminHostels;
