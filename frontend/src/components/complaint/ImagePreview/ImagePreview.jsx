import { FiX } from "react-icons/fi";

import "./ImagePreview.css";

function ImagePreview({ images, onRemove }) {
  if (!images.length) return null;

  return (
    <div className="image-preview">
      {images.map((image, index) => (
        <div key={index} className="preview-card">
          <img src={URL.createObjectURL(image)} alt="Complaint" />

          <button type="button" onClick={() => onRemove(index)}>
            <FiX />
          </button>
        </div>
      ))}
    </div>
  );
}

export default ImagePreview;
