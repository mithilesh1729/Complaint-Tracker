function DescriptionInput({ value, onChange }) {
  return (
    <div className="form-group">
      <label>Description</label>

      <textarea
        rows={6}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required
      />
    </div>
  );
}

export default DescriptionInput;
