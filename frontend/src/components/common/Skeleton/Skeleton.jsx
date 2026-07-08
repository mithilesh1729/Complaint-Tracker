import "./Skeleton.css";

function Skeleton({ width = "100%", height = "20px", borderRadius = "12px" }) {
  return (
    <div
      className="skeleton"
      style={{
        width,
        height,
        borderRadius,
      }}
    />
  );
}

export default Skeleton;
