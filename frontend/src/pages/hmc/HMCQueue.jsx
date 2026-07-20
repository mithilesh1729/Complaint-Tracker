import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/axios";
import DataTable from "../../components/common/DataTable/DataTable";
import PageHeader from "../../components/layout/PageHeader";

function HMCQueue() {
  const navigate = useNavigate();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchQueue();
  }, []);

  const fetchQueue = async () => {
    try {
      setLoading(true);
      const res = await api.get("/hmc/queue/");
      // The API returns paginated response, so data is in res.data.results
      setData(res.data.results || res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { header: "ID", field: "complaint_number" },
    { header: "Hostel", render: (row) => row.hostel || "N/A" },
    { header: "Category", render: (row) => row.category?.name || "N/A" },
    { header: "Priority", field: "priority" },
    { header: "Date", render: (row) => new Date(row.created_at).toLocaleDateString() },
    {
      header: "Actions",
      render: (row) => (
        <button
          className="table-action-button outline"
          onClick={() => navigate(`/hmc/complaints/${row.complaint_id}`)}
        >
          View
        </button>
      )
    }
  ];

  return (
    <div className="p-4">
      <PageHeader title="HMC Queue" subtitle="Complaints escalated by Wardens" />
      <div className="mt-4">
        <DataTable
          columns={columns}
          data={data}
          loading={loading}
          keyField="complaint_id"
          emptyMessage="No escalations found."
        />
      </div>
    </div>
  );
}

export default HMCQueue;
