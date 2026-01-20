import { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";

function CreateComplaint() {
  const navigate = useNavigate();

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [name, setName] = useState("");
  const [hostel, setHostel] = useState("");
  const [roomNo, setRoomNo] = useState("");
  const [phone, setPhone] = useState("");
  const [complaintType, setComplaintType] = useState("");
  const [priority, setPriority] = useState("medium");
  const [description, setDescription] = useState("");
  const [images, setImages] = useState([]);
  const MAX_WORDS = 150;

  const handleDescriptionChange = (e) => {
    const words = e.target.value.trim().split(/\s+/);
    if (words.length <= MAX_WORDS) {
      setDescription(e.target.value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    if (!name || !hostel || !roomNo || !complaintType || !description) {
      setError("Please fill all required fields.");
      return;
    }

    const formData = new FormData();
    formData.append("name", name);
    formData.append("hostel", hostel);
    formData.append("room_no", roomNo);
    formData.append("phone_number", phone);
    formData.append("complaint_type", complaintType);
    formData.append("priority", priority);
    formData.append("description", description);

    for (let i = 0; i < images.length; i++) {
      formData.append("images", images[i]);
    }

    setLoading(true);
    try {
      await api.post("/complaints/create/", formData);
      navigate("/dashboard");
    } catch {
      setError("Failed to submit complaint. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container py-5" style={{ maxWidth: "760px" }}>
      {/* <div className="card shadow-sm border-0"> */}
      {/* <div
        className="card shadow-lg border-0"
        style={{ background: "#ffffff" }}
      > */}

      <div
        className="card-header border-0 pt-4 px-4"
        style={{ background: "#f8f9fa" }}
      >
        <div className="card-body p-4 p-md-5">
          {/* Back */}
          <button
            className="btn btn-link px-0 mb-3"
            onClick={() => navigate("/dashboard")}
          >
            ← Back to Dashboard
          </button>

          {/* Title */}
          <h3
            className="fw-bold text-center mb-2"
            style={{ color: "#0d3b66" }}
          ></h3>
          <h3 className="fw-bold text-center mb-2 text-primary">
            Submit Your Complaint
          </h3>
          <p className="text-muted text-center mb-4">
            Please Fill out the form below to submit your complaint.
          </p>

          {error && <div className="alert alert-danger">{error}</div>}

          <form onSubmit={handleSubmit}>
            {/* Name */}
            <div className="mb-3">
              <label className="form-label">Full Name *</label>
              <input
                type="text"
                className="form-control"
                placeholder="Enter your full name"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            {/* Hostel + Room */}
            <div className="row">
              <div className="col-md-6 mb-3">
                <label className="form-label">Hostel *</label>
                <select
                  className="form-select"
                  value={hostel}
                  onChange={(e) => setHostel(e.target.value)}
                >
                  <option value="">Select Hostel</option>
                  <option>Aryabhatta</option>
                  <option>Kautilya</option>
                  <option>Kadambini</option>
                  <option>Kosi</option>
                  <option>Sone</option>
                  <option>Brahmputra</option>
                  <option>Ganga</option>
                </select>
              </div>

              <div className="col-md-6 mb-3">
                <label className="form-label">Room No. *</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="e.g. 305"
                  value={roomNo}
                  onChange={(e) => setRoomNo(e.target.value)}
                />
              </div>
            </div>

            {/* Phone */}
            <div className="mb-3">
              <label className="form-label">Phone Number</label>
              <div className="input-group">
                <span className="input-group-text">+91</span>
                <input
                  type="text"
                  className="form-control"
                  placeholder="XXXXXXXXXX"
                  maxLength="10"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                />
              </div>
            </div>

            {/* Type + Priority */}
            <div className="row">
              <div className="col-md-6 mb-3">
                <label className="form-label">Complaint Type *</label>
                <select
                  className="form-select"
                  value={complaintType}
                  onChange={(e) => setComplaintType(e.target.value)}
                >
                  <option value="">Select Type</option>
                  <option value="electricity">Electricity</option>
                  <option value="water">Water</option>
                  <option value="mess">Mess</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div className="col-md-6 mb-3">
                <label className="form-label">Priority</label>
                <select
                  className="form-select"
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
            </div>

            {/* Description */}
            <div className="mb-3">
              <label className="form-label">
                Description *{" "}
                <span className="text-muted">(max {MAX_WORDS} words)</span>
              </label>
              <textarea
                className="form-control"
                rows="4"
                placeholder="Describe the issue clearly..."
                value={description}
                onChange={handleDescriptionChange}
              />
              <small className="text-muted">
                {description.trim()
                  ? description.trim().split(/\s+/).length
                  : 0}{" "}
                / {MAX_WORDS} words
              </small>
            </div>

            {/* Images */}
            <div className="mb-4">
              <label className="form-label">Upload Images (optional)</label>
              <input
                type="file"
                className="form-control"
                multiple
                onChange={(e) => setImages(e.target.files)}
              />
            </div>

            {/* Submit (CENTERED) */}
            <div className="text-center pt-3 border-top">
              <button
                className="btn btn-primary px-5"
                type="submit"
                disabled={loading}
              >
                {loading ? "Submitting..." : "Submit Complaint"}
              </button>

              <p className="text-muted mt-3 mb-0" style={{ fontSize: 13 }}>
                You can track status & updates from your dashboard.
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default CreateComplaint;
