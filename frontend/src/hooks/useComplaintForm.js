import { useState } from "react";
import { useNavigate } from "react-router-dom";

import useComplaintCategories from "./useComplaintCategories";
import useCreateComplaint from "./useCreateComplaint";

import toast from "react-hot-toast";

export default function useComplaintForm() {
  const navigate = useNavigate();

  const {
    categories,
    loading: categoriesLoading,
    error: categoriesError,
    refresh,
  } = useComplaintCategories();

  const { createComplaint, loading } = useCreateComplaint();

  const [form, setForm] = useState({
    category_id: "",
    location_details: "",
    description: "",
    priority: "medium",
    images: [],
  });

  function handleChange(field, value) {
    if (field === "description" && value.length > 500) {
      return;
    }
    setForm((prev) => ({
      ...prev,
      [field]: value,
    }));
  }

  function handleImagesChange(files) {
    setForm((prev) => ({
      ...prev,
      images: files,
    }));
  }

  function handleRemoveImage(index) {
    setForm((prev) => ({
      ...prev,
      images: prev.images.filter((_, i) => i !== index),
    }));
  }

  async function handleSubmit(e) {
    e.preventDefault();

    // if (!form.category_id) {
    //   showToast("Please select a complaint category.", "error");
    //   return;
    // }

    // if (!form.description.trim()) {
    //   showToast("Please enter a complaint description.", "error");
    //   return;
    // }

    const formData = new FormData();

    formData.append("category_id", form.category_id);
    formData.append("location_details", form.location_details);
    formData.append("description", form.description);
    formData.append("priority", form.priority);
    
    form.images.forEach((image) => formData.append("images", image));

    try {
      const complaint = await createComplaint(formData);

      toast.success("Complaint submitted successfully.");

      navigate(`/student/complaints/${complaint.complaint_id}`);
    } catch (error) {
      toast.error("Unable to submit complaint.");
    }
  }

  return {
    form,

    loading,

    categories,
    categoriesLoading,
    categoriesError,

    refresh,

    handleChange,
    handleImagesChange,
    handleRemoveImage,
    handleSubmit,
  };
}
