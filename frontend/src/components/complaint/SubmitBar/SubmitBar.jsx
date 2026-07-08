import "./SubmitBar.css";

function SubmitBar({ loading, text = "Submit" }) {
  return (
    <div className="submit-bar">
      <button type="submit" className="submit-button" disabled={loading}>
        {loading ? "Submitting..." : text}
      </button>
    </div>
  );
}

export default SubmitBar;
