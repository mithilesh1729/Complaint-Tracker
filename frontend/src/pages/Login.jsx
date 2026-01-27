// import { useState } from "react";
// import api from "../api/axios";
// import { useNavigate } from "react-router-dom";
// import { jwtDecode } from "jwt-decode";

// function Login() {
//   const navigate = useNavigate();

//   const [rollNo, setRollNo] = useState("");
//   const [password, setPassword] = useState("");
//   const [error, setError] = useState("");

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     // print the login id
//     console.log("Roll No:", rollNo);
//     console.log("Password:", password);
//     setError("");

//     try {
//       const response = await api.post("/token/", {
//         roll_no: rollNo, // must match backend
//         password,
//       });

//       // Store JWTs
//       localStorage.setItem("access", response.data.access);
//       localStorage.setItem("refresh", response.data.refresh);

//       // temporary success log
//       console.log("JWT stored");

//       // Decode token ONCE
//       const decoded = jwtDecode(response.data.access);
//       console.log(decoded);

//       // Role-based redirect (IMPORTANT UX)
//       if (decoded.is_admin) {
//         navigate("/admin/dashboard");
//       } else {
//         navigate("/dashboard");
//       }
//     } catch (err) {
//       console.error("Login failed", err);
//       setError("Invalid roll number or password");
//     }
//   };

//   return (
//     <div className="container mt-5">
//       <div className="row justify-content-center">
//         <div className="col-md-4">
//           <h3 className="text-center mb-4">Login</h3>

//           {error && <div className="alert alert-danger">{error}</div>}

//           <form onSubmit={handleSubmit}>
//             <div className="mb-3">
//               <label className="form-label">Roll Number</label>
//               <input
//                 type="text"
//                 className="form-control"
//                 value={rollNo}
//                 onChange={(e) => setRollNo(e.target.value)}
//                 required
//               />
//             </div>

//             <div className="mb-3">
//               <label className="form-label">Password</label>
//               <input
//                 type="password"
//                 className="form-control"
//                 value={password}
//                 onChange={(e) => setPassword(e.target.value)}
//                 required
//               />
//             </div>

//             <button type="submit" className="btn btn-primary w-100">
//               Login
//             </button>
//           </form>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default Login;

import { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

// 👉 use the SECOND image (main gate)
import campusImg from "../assets/MainEntrance.webp";

function Login() {
  const navigate = useNavigate();

  const [rollNo, setRollNo] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await api.post("/token/", {
        roll_no: rollNo,
        password,
      });

      localStorage.setItem("access", response.data.access);
      localStorage.setItem("refresh", response.data.refresh);

      const decoded = jwtDecode(response.data.access);

      if (decoded.is_admin) {
        navigate("/admin/dashboard");
      } else {
        navigate("/dashboard");
      }
    } catch {
      setError("Invalid roll number or password");
    }
  };

  return (
    <div className="container-fluid vh-100">
      <div className="row h-100">
        {/* LEFT : Image */}
        <div className="col-md-7 d-none d-md-block p-0">
          <img
            src={campusImg}
            alt="Campus Entrance"
            className="img-fluid h-100 w-100"
            style={{ objectFit: "cover" }}
          />
        </div>

        {/* RIGHT : Login Form */}
        <div className="col-md-5 d-flex align-items-center justify-content-center bg-light">
          <div
            className="card shadow-sm p-4"
            style={{ width: "100%", maxWidth: 380 }}
          >
            <h4 className="text-center fw-bold mb-1">
              Complaint Tracking System
            </h4>
            <p className="text-center text-muted mb-4">
              National Institute of Technology, Patna
            </p>

            {error && <div className="alert alert-danger">{error}</div>}

            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label className="form-label">Roll Number</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="e.g. 2101CS01"
                  value={rollNo}
                  onChange={(e) => setRollNo(e.target.value)}
                  required
                />
              </div>

              <div className="mb-3">
                <label className="form-label">Password</label>
                <input
                  type="password"
                  className="form-control"
                  placeholder=""
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>

              <button type="submit" className="btn btn-primary w-100 mt-2">
                Login
              </button>
            </form>

            <p
              className="text-center text-muted mt-4 mb-0"
              style={{ fontSize: 13 }}
            >
              © NIT Patna – Internal Student Portal
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
