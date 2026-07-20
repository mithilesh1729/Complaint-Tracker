import { useState, useEffect } from "react";
import api from "../../api/axios";
import PageHeader from "../../components/layout/PageHeader";
import "./Warden.css";

function StaffPerformance() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const res = await api.get("/warden/staff-performance/");
      setData(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <PageHeader title="Office Staff Performance" subtitle="Resolution metrics by staff member" />
      
      {loading ? (
        <div className="mt-4">Loading metrics...</div>
      ) : (
        <div className="mt-4 warden-table-container">
          <table className="warden-table">
            <thead>
              <tr>
                <th>Staff Member</th>
                <th>Assigned</th>
                <th>Resolved</th>
                <th>Pending</th>
              </tr>
            </thead>
            <tbody>
              {data.map((staff) => (
                <tr key={staff.roll_no}>
                  <td>{staff.name} ({staff.roll_no})</td>
                  <td>{staff.assigned}</td>
                  <td>{staff.resolved}</td>
                  <td>{staff.pending}</td>
                </tr>
              ))}
              {data.length === 0 && (
                <tr>
                  <td colSpan="4" className="text-center p-4">No staff data available.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default StaffPerformance;
