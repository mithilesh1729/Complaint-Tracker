import { useState } from "react";

import "./ComplaintImages.css";

function ComplaintImages({ complaint }) {
  const [selectedImage, setSelectedImage] = useState(null);

  if (!complaint.images?.length) {
    return null;
  }

  return (
    <div className="complaint-images">
      <h3>Attachments ({complaint.images.length})</h3>

      <p className="attachments-hint">
        Click any attachment to view it in full size.
      </p>

      <div className="image-grid">
        {complaint.images.map((image, index) => (
          <div
            className="image-card"
            key={index}
            onClick={() => setSelectedImage(image.image)}
          >
            <img
              src={image.image}
              alt={`Attachment ${index + 1}`}
              loading="lazy"
            />
          </div>
        ))}
      </div>

      {selectedImage && (
        <div
          className="image-preview-overlay"
          onClick={() => setSelectedImage(null)}
        >
          <button
            className="preview-close"
            onClick={() => setSelectedImage(null)}
          >
            ×
          </button>
          <img
            src={selectedImage}
            alt="Complaint attachment"
            className="image-preview"
            onClick={(e) => e.stopPropagation()}
          />
        </div>
      )}
    </div>
  );
}

export default ComplaintImages;
