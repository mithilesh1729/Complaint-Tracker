import { useState } from "react";
import api from "../../api/axios";
import useToast from "../../hooks/useToast";
import StatCard from "../../components/common/StatCard/StatCards";
import PageHeader from "../../components/layout/PageHeader";
import "./AdminProfile.css";

function AdminReports() {
  const { showToast } = useToast();
  const [downloading, setDownloading] = useState(false);

  const handleDownloadCSV = async () => {
    try {
      setDownloading(true);
      const response = await api.get("/admin/reports/csv/", {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "complaints_report.csv");
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);

      showToast("Report downloaded successfully", "success");
    } catch (error) {
      showToast("Failed to download report", "error");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="p-4">
      <PageHeader 
        title="Analytics & Reports" 
        subtitle="Export and analyze system data"
      />

      <div className="admin-profile-grid" style={{ gridTemplateColumns: "1fr" }}>
        <div className="admin-profile-card">
          <h3>Export Data</h3>
          <p className="text-muted mb-4">
            Download a comprehensive CSV export of all complaints across all hostels. 
            This data can be used in Excel, Google Sheets, or other BI tools for advanced analytics.
          </p>
          
          <button 
            className="table-action-button primary"
            style={{ padding: "12px 24px", fontSize: "14px", display: "inline-flex", alignItems: "center", gap: "8px" }}
            onClick={handleDownloadCSV}
            disabled={downloading}
          >
            {downloading ? (
              <>
                <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Generating Report...
              </>
            ) : (
              <>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-download" viewBox="0 0 16 16">
                  <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                  <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
                </svg>
                Download Full CSV Report
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

export default AdminReports;
