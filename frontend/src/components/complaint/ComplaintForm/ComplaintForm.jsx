import useComplaintForm from "../../../hooks/useComplaintForm";

import CategorySelect from "../CategorySelect";
import ImageUploader from "../ImageUploader";
import ImagePreview from "../ImagePreview";
import SubmitBar from "../SubmitBar";

import Skeleton from "../../common/Skeleton";
import ErrorState from "../../common/ErrorState";

import "./ComplaintForm.css";

function ComplaintForm() {
  const {
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
  } = useComplaintForm();

  if (categoriesLoading) {
    return <Skeleton height="420px" />;
  }

  if (categoriesError) {
    return (
      <ErrorState
        title="Unable to load complaint categories"
        message="Please try again."
        onRetry={refresh}
      />
    );
  }

  return (
    <form className="complaint-form" onSubmit={handleSubmit}>
      {/* Category */}

      <CategorySelect
        categories={categories}
        value={form.category_id}
        onChange={(value) => handleChange("category_id", value)}
      />

      {/* Location */}

      <div className="form-group">
        <label>Location Details</label>

        <input
          type="text"
          placeholder="Example: Aryabhatta Hostel, Room A203, Corridor"
          value={form.location_details}
          onChange={(e) => handleChange("location_details", e.target.value)}
        />
      </div>

      {/* Priority */}
      <div className="form-group">
        <label>Priority</label>
        <select
          value={form.priority}
          onChange={(e) => handleChange("priority", e.target.value)}
          className="priority-select"
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      {/* Description */}

      <div className="form-group">
        <label>
          Description
          <span className="required">*</span>
        </label>

        <textarea
          rows={6}
          maxLength={500}
          placeholder="Describe the issue clearly..."
          value={form.description}
          onChange={(e) => handleChange("description", e.target.value)}
          required
        />

        <div className="textarea-footer">
          <small>{form.description.length}/500 characters</small>
        </div>
      </div>

      {/* Images */}
      <label>
        Attachments
        <span className="optional">(Optional)</span>
      </label>
      <ImageUploader onChange={handleImagesChange} />

      <ImagePreview images={form.images} onRemove={handleRemoveImage} />

      <SubmitBar loading={loading} text="Raise Complaint" />
    </form>
  );
}

export default ComplaintForm;
