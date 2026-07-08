import "./CategorySelect.css";

function CategorySelect({ categories, value, onChange }) {
  return (
    <div className="form-group">
      <label htmlFor="category">
        Complaint Category<span className="required">*</span>
      </label>

      <select
        id="category"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required
      >
        <option value="">Select a complaint category</option>

        {categories.map((category) => (
          <option key={category.id} value={category.id}>
            {category.name}
          </option>
        ))}
      </select>
    </div>
  );
}

export default CategorySelect;
