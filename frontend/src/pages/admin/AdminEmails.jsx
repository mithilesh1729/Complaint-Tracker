import { useState, useEffect } from "react";
import api from "../../api/axios";
import PageHeader from "../../components/layout/PageHeader";
import DataTable from "../../components/common/DataTable/DataTable";

function AdminEmails() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchEmails();
  }, []);

  const fetchEmails = async () => {
    try {
      setLoading(true);
      const response = await api.get("/admin/dev/emails/");
      setEmails(response.data);
      setError(null);
    } catch (err) {
      setError("Failed to load email logs");
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { 
      header: "Sent At", 
      field: "sent_at",
      width: "150px",
      render: (row) => new Date(row.sent_at).toLocaleString()
    },
    { header: "Recipient", field: "recipient", width: "200px" },
    { header: "Subject", field: "subject", width: "250px" },
    { 
      header: "Email Body", 
      field: "body",
      render: (row) => (
        <div style={{ whiteSpace: "pre-wrap", fontSize: "13px", color: "var(--text-secondary)", maxHeight: "100px", overflowY: "auto", padding: "8px", background: "#f8f9fa", borderRadius: "8px" }}>
          {row.body}
        </div>
      )
    }
  ];

  return (
    <div className="admin-profile-page" style={{ padding: "32px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
        <PageHeader 
          title="System Email Logs (Dev Mode)" 
          subtitle="View temporary passwords and sent emails"
        />
        <button className="table-action-button secondary" onClick={fetchEmails}>
          Refresh Logs
        </button>
      </div>

      {error && <div style={{ color: "red", marginBottom: "16px" }}>{error}</div>}

      <div className="complaint-table-container mb-4" style={{ padding: "20px" }}>
        <DataTable
          columns={columns}
          data={emails}
          keyField="id"
          loading={loading}
          emptyMessage="No emails have been sent yet."
        />
      </div>
    </div>
  );
}

export default AdminEmails;
