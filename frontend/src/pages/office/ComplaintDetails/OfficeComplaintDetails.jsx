import { useParams } from "react-router-dom";

import PageHeader from "../../../components/layout/PageHeader";

import ComplaintHeader from "../../../components/complaint/ComplaintHeader";
import ComplaintInfo from "../../../components/complaint/ComplaintInfo";
import ComplaintImages from "../../../components/complaint/ComplaintImages";
import ComplaintTimeline from "../../../components/complaint/ComplaintTimeline";

import OfficeComplaintActions from "../../../components/complaint/ComplaintActions/OfficeComplaintActions";

import ErrorState from "../../../components/common/ErrorState";
import Skeleton from "../../../components/common/Skeleton";

import useComplaintDetails from "../../../hooks/useComplaintDetails";

import "./OfficeComplaintDetails.css";

function OfficeComplaintDetails() {
  const { complaintId } = useParams();

  const {
    complaint,

    loading,

    error,

    refresh,
  } = useComplaintDetails(complaintId);

  if (loading) {
    return <Skeleton height="600px" />;
  }

  if (error) {
    return (
      <ErrorState
        title="Unable to load complaint"
        message="Please try again."
        onRetry={refresh}
      />
    );
  }

  return (
    <div className="office-complaint-details">
      <PageHeader
        title="Complaint Details"
        subtitle="View and manage complaint."
      />

      <ComplaintHeader complaint={complaint} />

      <ComplaintInfo complaint={complaint} />

      <ComplaintImages complaint={complaint} />

      <ComplaintTimeline complaint={complaint} />

      <OfficeComplaintActions complaint={complaint} refresh={refresh} />
    </div>
  );
}

export default OfficeComplaintDetails;
