import { useState, useEffect } from "react";
import api from "../../api/axios";
import PageHeader from "../../components/layout/PageHeader";
import "../warden/Warden.css"; // Reuse the table styling

function HostelPerformance() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const res = await api.get("/hmc/hostel-performance/");
      setData(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <PageHeader title="Hostel Performance" subtitle="System-wide resolution metrics by hostel" />
      
      {loading ? (
        <div className="mt-4">Loading metrics...</div>
      ) : (
        <div className="mt-4 warden-table-container">
          <table className="warden-table">
            <thead>
              <tr>
                <th>Hostel</th>
                <th>Pending</th>
                <th>Resolved</th>
                <th>Escalated</th>
              </tr>
            </thead>
            <tbody>
              {data.map((h) => (
                <tr key={h.hostel}>
                  <td>{h.hostel}</td>
                  <td>{h.pending}</td>
                  <td>{h.resolved}</td>
                  <td>{h.escalated}</td>
                </tr>
              ))}
              {data.length === 0 && (
                <tr>
                  <td colSpan="4" className="text-center p-4">No hostel data available.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default HostelPerformance;
