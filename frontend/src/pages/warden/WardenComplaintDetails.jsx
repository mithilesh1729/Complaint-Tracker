import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../../api/axios";
import useToast from "../../hooks/useToast";

import PageHeader from "../../components/layout/PageHeader";
import ComplaintHeader from "../../components/complaint/ComplaintHeader";
import ComplaintInfo from "../../components/complaint/ComplaintInfo";
import ComplaintImages from "../../components/complaint/ComplaintImages";
import ComplaintTimeline from "../../components/complaint/ComplaintTimeline";
import WardenComplaintActions from "../../components/complaint/ComplaintActions/WardenComplaintActions";

import Skeleton from "../../components/common/Skeleton";
import ErrorState from "../../components/common/ErrorState";

function WardenComplaintDetails() {
  const { complaintId } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();
  
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetchComplaint();
  }, [complaintId]);

  const fetchComplaint = async () => {
    try {
      setLoading(true);
      setError(false);
      const res = await api.get(`/complaints/${complaintId}/`);
      setComplaint(res.data);
    } catch (err) {
      setError(true);
      showToast("Failed to load complaint details", "error");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Skeleton height="600px" />;
  }

  if (error || !complaint) {
    return (
      <ErrorState
        title="Unable to load complaint"
        message="Please try again."
        onRetry={fetchComplaint}
      />
    );
  }

  return (
    <div className="p-4" style={{ maxWidth: '1200px', margin: '0 auto' }}>
      <PageHeader
        title="Complaint Details"
        subtitle="View and manage complaint."
      />

      <ComplaintHeader complaint={complaint} />
      <ComplaintInfo complaint={complaint} />
      <ComplaintImages complaint={complaint} />
      <ComplaintTimeline complaint={complaint} />
      <WardenComplaintActions complaint={complaint} refresh={fetchComplaint} />
    </div>
  );
}

export default WardenComplaintDetails;
