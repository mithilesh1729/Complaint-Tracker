import { useParams } from "react-router-dom";

import AppLayout from "../../../components/layout/AppLayout";
import PageHeader from "../../../components/layout/PageHeader";

import Skeleton from "../../../components/common/Skeleton";
import ErrorState from "../../../components/common/ErrorState";

import ComplaintHeader from "../../../components/complaint/ComplaintHeader";
import ComplaintInfo from "../../../components/complaint/ComplaintInfo";
import ComplaintImages from "../../../components/complaint/ComplaintImages";
import ComplaintTimeline from "../../../components/complaint/ComplaintTimeline";
import ComplaintActions from "../../../components/complaint/ComplaintActions";

import useComplaint from "../../../hooks/useComplaint";

import "./ComplaintDetails.css";

function ComplaintDetails() {
  const { complaintId } = useParams();

  const { complaint, loading, error, refresh } = useComplaint(complaintId);

  if (loading) {
    return (
      <>
        <Skeleton height="600px" />
      </>
    );
  }

  if (error) {
    return (
      <>
        <ErrorState
          title="Unable to load complaint"
          message="Please try again."
          onRetry={refresh}
        />
      </>
    );
  }

  return (
    <>
      <div className="complaint-details-page">
        <PageHeader
          title="Complaint Details"
          subtitle={complaint.complaint_number}
        />

        <ComplaintHeader complaint={complaint} />

        <ComplaintInfo complaint={complaint} />

        <ComplaintImages complaint={complaint} />

        <ComplaintTimeline complaint={complaint} />

        <ComplaintActions complaint={complaint} refresh={refresh} />
      </div>
    </>
  );
}

export default ComplaintDetails;
