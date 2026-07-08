import { useEffect, useState } from "react";

export default function useToast() {
  const [toast, setToast] = useState({
    open: false,
    type: "success",
    message: "",
  });

  function showToast(message, type = "success") {
    setToast({
      open: true,
      type,
      message,
    });
  }

  function hideToast() {
    setToast((prev) => ({
      ...prev,
      open: false,
    }));
  }

  useEffect(() => {
    if (!toast.open) return;

    const timer = setTimeout(hideToast, 3000);

    return () => clearTimeout(timer);
  }, [toast.open]);

  return {
    toast,
    showToast,
    hideToast,
  };
}
