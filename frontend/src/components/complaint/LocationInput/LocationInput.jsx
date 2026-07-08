function LocationInput({ value, onChange }) {
  return (
    <div className="form-group">
      <label>Location Details</label>

      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Room A203 Bathroom"
      />
    </div>
  );
}

export default LocationInput;
