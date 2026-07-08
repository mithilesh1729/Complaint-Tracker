import { useState, useEffect, useRef } from "react";

import { useNavigate } from "react-router-dom";

import toast from "react-hot-toast";

import useAuth from "../../hooks/useAuth";
import getDashboardRoute from "../../utils/getDashboardRoute";

function LoginForm() {
  const navigate = useNavigate();

  const { login } = useAuth();

  const [form, setForm] = useState({
    roll_no: "",

    password: "",
  });

  const rollNoRef = useRef(null);

  const [loading, setLoading] = useState(false);

  const { login, isAuthenticated, user } = useAuth();

  useEffect(() => {
    rollNoRef.current?.focus();
  }, []);

  useEffect(() => {
    if (isAuthenticated && user) {
      navigate(
        getDashboardRoute(user.role),

        {
          replace: true,
        },
      );
    }
  }, [isAuthenticated, user, navigate]);

  async function handleSubmit(e) {
    e.preventDefault();

    if (!form.roll_no.trim()) {
      toast.error("Roll Number is required.");

      return;
    }

    if (!form.password.trim()) {
      toast.error("Password is required.");

      return;
    }

    try {
      setLoading(true);

      const route = await login(form);

      toast.success("Welcome back!");

      navigate(route, {
        replace: true,
      });
    } catch (error) {
      if (error.response) {
        toast.error("Invalid Roll Number or Password.");
      } else {
        toast.error("Unable to connect to server.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* Inputs */}

      {/* Button */}
      <button type="submit" className="login-button" disabled={loading}>
        {loading ? "Signing In..." : "Sign In"}
      </button>
    </form>
  );
}

export default LoginForm;
