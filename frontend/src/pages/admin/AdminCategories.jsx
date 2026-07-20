import { useState } from "react";
import useCategories from "../../hooks/useCategories";
import DataTable from "../../components/common/DataTable/DataTable";
import PageHeader from "../../components/layout/PageHeader";
import Modal from "../../components/common/Modal/Modal";
import api from "../../api/axios";
import useToast from "../../hooks/useToast";
import Toast from "../../components/common/Toast/Toast";

function AdminCategories() {
  const { categories, loading, fetchCategories } = useCategories();
  const { toast, showToast } = useToast();
  
  const [modalOpen, setModalOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState(null);
  
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    display_order: 0
  });

  const handleOpenModal = (category = null) => {
    if (category) {
      setEditingCategory(category);
      setFormData({
        name: category.name,
        description: category.description,
        display_order: category.display_order
      });
    } else {
      setEditingCategory(null);
      setFormData({ name: "", description: "", display_order: 0 });
    }
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setEditingCategory(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingCategory) {
        await api.patch(`/admin/categories/${editingCategory.id}/`, formData);
        showToast("Category updated", "success");
      } else {
        await api.post("/admin/categories/", formData);
        showToast("Category created", "success");
      }
      fetchCategories();
      handleCloseModal();
    } catch (err) {
      showToast("Failed to save category", "error");
    }
  };

  const handleToggleActive = async (id, currentState) => {
    try {
      await api.delete(`/admin/categories/${id}/`);
      showToast(currentState ? "Category deactivated" : "Category activated", "success");
      fetchCategories();
    } catch (err) {
      showToast("Failed to change category status", "error");
    }
  };

  const columns = [
    { header: "Order", field: "display_order", width: "80px" },
    { header: "Name", field: "name" },
    { header: "Description", field: "description" },
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
    <div className="p-4">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
        <PageHeader 
          title="Complaint Categories" 
          subtitle="Manage master data for complaint classification"
        />
        <button className="table-action-button primary" onClick={() => handleOpenModal()} style={{ padding: "10px 20px" }}>
          + New Category
        </button>
      </div>

      <DataTable
        columns={columns}
        data={categories}
        keyField="id"
        loading={loading}
      />

      <Modal
        open={modalOpen}
        title={editingCategory ? "Edit Category" : "New Category"}
        onClose={handleCloseModal}
      >
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Category Name</label>
            <input 
              type="text" 
              required
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              placeholder="e.g. Electrical"
            />
          </div>
          <div className="form-group">
            <label>Description</label>
            <textarea 
              rows="3"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              placeholder="Detailed description of issues in this category..."
              style={{ resize: "vertical" }}
            ></textarea>
          </div>
          <div className="form-group mb-4">
            <label>Display Order (Priority)</label>
            <input 
              type="number" 
              required
              value={formData.display_order}
              onChange={(e) => setFormData({...formData, display_order: e.target.value})}
            />
          </div>
          
          <div style={{ display: "flex", justifyContent: "flex-end", gap: "8px", marginTop: "16px" }}>
            <button 
              type="button" 
              className="table-action-button secondary" 
              onClick={handleCloseModal}
              style={{ padding: "10px 20px" }}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="table-action-button primary"
              style={{ padding: "10px 20px" }}
            >
              {editingCategory ? "Update Category" : "Save Category"}
            </button>
          </div>
        </form>
      </Modal>

      <Toast {...toast} />
    </div>
  );
}

export default AdminCategories;
