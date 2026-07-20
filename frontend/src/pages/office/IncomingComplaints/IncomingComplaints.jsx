import { useState } from "react";

import { FiUserCheck } from "react-icons/fi";

import PageHeader from "../../../components/layout/PageHeader";
import ComplaintTable from "../../../components/complaint/ComplaintTable/ComplaintTable";
import ComplaintFilters from "../../../components/complaint/Filters/ComplaintFilters";

// import ConfirmDialog from "../../../components/common/ConfirmDialog";
import TextareaDialog from "../../../components/common/TextareaDialog";
import ErrorState from "../../../components/common/ErrorState";

import { OFFICE_QUEUE_FILTERS } from "../../../config/complaintFilters";
import { OFFICE_COMPLAINT_COLUMNS } from "../../../config/complaintTableColumns";

import useIncomingComplaints from "../../../hooks/useIncomingComplaints";
import useAssignComplaint from "../../../hooks/useAssignComplaint";

import "./IncomingComplaints.css";

function IncomingComplaints() {
  const {
    complaints,
    loading,
    error,
    pagination,
    page,
    setPage,
    filters,
    updateFilters,
    refresh,
  } = useIncomingComplaints();

  const [selectedComplaint, setSelectedComplaint] = useState(null);

  const { loading: assigning, assign } = useAssignComplaint(refresh);

  // async function handleAssign() {
  //   const result = await assign(selectedComplaint.complaint_id);

  //   if (result.success) {
  //     setSelectedComplaint(null);
  //   }
  // }

  async function handleAssign(remark) {
    const result = await assign(selectedComplaint.complaint_id, {
      remark,
    });

    if (result.success) {
      setSelectedComplaint(null);
    }
  }

  const actions = [
    {
      label: "Assign",
      icon: FiUserCheck,
      variant: "primary",
      onClick: (complaint) => setSelectedComplaint(complaint),
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
    <div className="incoming-complaints-page">
      <PageHeader
        title="Incoming Complaints"
        subtitle="Pending complaints waiting for assignment."
      />

      <ComplaintFilters
        filters={filters}
        config={OFFICE_QUEUE_FILTERS}
        onChange={updateFilters}
        onRefresh={refresh}
      />

      <ComplaintTable
        columns={OFFICE_COMPLAINT_COLUMNS}
        data={complaints}
        actions={actions}
        loading={loading}
        pagination={pagination}
        page={page}
        onPageChange={setPage}
      />

      {/* <ConfirmDialog
        open={Boolean(selectedComplaint)}
        title="Assign Complaint"
        message="Are you sure you want to assign this complaint to yourself?"
        confirmText="Assign"
        loading={assigning}
        onCancel={() => setSelectedComplaint(null)}
        onConfirm={handleAssign}
      /> */}

      <TextareaDialog
        open={Boolean(selectedComplaint)}
        title="Assign Complaint"
        label="Initial Remark"
        placeholder="Complaint accepted. Work has been scheduled..."
        confirmText="Assign"
        required
        loading={assigning}
        onCancel={() => setSelectedComplaint(null)}
        onConfirm={handleAssign}
      />
    </div>
  );
}

export default IncomingComplaints;
