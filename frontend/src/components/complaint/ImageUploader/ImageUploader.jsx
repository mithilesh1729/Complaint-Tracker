import { FiUploadCloud } from "react-icons/fi";

import "./ImageUploader.css";

function ImageUploader({ onChange }) {
  function handleFiles(e) {
    const files = Array.from(e.target.files);

    onChange(files);
  }

  return (
    <div className="image-uploader">
      <label htmlFor="complaint-images" className="upload-box">
        <FiUploadCloud className="upload-icon" />

        <h4>Upload Images</h4>

        <p>Drag & drop images here or click to browse</p>

        <small>JPG • PNG • WEBP</small>
      </label>

      <input
        id="complaint-images"
        type="file"
        multiple
        accept="image/*"
        hidden
        onChange={handleFiles}
      />
    </div>
  );
}

export default ImageUploader;
