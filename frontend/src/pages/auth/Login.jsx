import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import useAuth from "../../hooks/useAuth";

import "./Login.css";

function Login() {
  const navigate = useNavigate();

  const { login } = useAuth();

  const [rollNo, setRollNo] = useState("");

  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  useEffect(() => {
    document.title = "Login • Complaint Management System";
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();

    setError("");

    if (!rollNo.trim() || !password.trim()) {
      setError("Roll number and password are required.");

      return;
    }

    try {
      setLoading(true);

      const route = await login({
        roll_no: rollNo,
        password,
      });

      navigate(route, {
        replace: true,
      });
    } catch (error) {
      if (error.response) {
        setError("Invalid Roll Number or Password.");
      } else {
        setError("Unable to connect to server.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>Complaint Management System</h1>

        <p>National Institute of Technology Patna</p>

        {error && <div className="login-error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Roll Number</label>

            <input
              value={rollNo}
              onChange={(e) => setRollNo(e.target.value)}
              placeholder="Enter Roll Number"
            />
          </div>

          <div className="form-group">
            <label>Password</label>

            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter Password"
            />
          </div>

          <button className="login-button" disabled={loading}>
            {loading ? "Signing In..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
