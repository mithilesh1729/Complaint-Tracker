import "./Button.css";

function Button({
  children,

  variant = "primary",

  type = "button",

  loading = false,

  disabled = false,

  fullWidth = false,

  icon,

  ...props
}) {
  return (
    <button
      type={type}
      disabled={disabled || loading}
      className={`btn btn-${variant} ${fullWidth ? "btn-full" : ""}`}
      {...props}
    >
      {loading ? (
        "Loading..."
      ) : (
        <>
          {icon}

          {children}
        </>
      )}
    </button>
  );
}

export default Button;
