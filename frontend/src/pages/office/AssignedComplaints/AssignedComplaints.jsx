import { FiArrowRight } from "react-icons/fi";
import { useNavigate } from "react-router-dom";

import PageHeader from "../../../components/layout/PageHeader";

import ComplaintTable from "../../../components/complaint/ComplaintTable/ComplaintTable";
import ComplaintFilters from "../../../components/complaint/Filters/ComplaintFilters";

import ErrorState from "../../../components/common/ErrorState";

import { OFFICE_ASSIGNED_FILTERS } from "../../../config/complaintFilters";

import { OFFICE_COMPLAINT_COLUMNS } from "../../../config/complaintTableColumns";

import useAssignedComplaints from "../../../hooks/useAssignedComplaints";

import "./AssignedComplaints.css";

function AssignedComplaints() {
  const navigate = useNavigate();

  const {
    complaints,
    loading,
    error,
    pagination,
    setPage,
    filters,
    updateFilters,
    refresh,
  } = useAssignedComplaints();

  const actions = [
    {
      label: "View",

      icon: FiArrowRight,

      variant: "secondary",

      onClick: (complaint) =>
        navigate(`/office/complaints/${complaint.complaint_id}`),
    },
  ];

  if (error) {
    return (
      <ErrorState
        title="Unable to load complaints"
        message="Please try again."
        onRetry={refresh}
      />
    );
  }

  return (
    <div className="assigned-complaints-page">
      <PageHeader
        title="My Assigned Work"
        subtitle="Complaints currently assigned to you."
      />

      <ComplaintFilters
        filters={filters}
        config={OFFICE_ASSIGNED_FILTERS}
        onChange={updateFilters}
        onRefresh={refresh}
      />

      <ComplaintTable
        columns={OFFICE_COMPLAINT_COLUMNS}
        data={complaints}
        actions={actions}
        loading={loading}
        pagination={pagination}
        onPageChange={setPage}
      />
    </div>
  );
}

export default AssignedComplaints;
