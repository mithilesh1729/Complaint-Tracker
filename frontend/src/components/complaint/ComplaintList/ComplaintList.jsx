import ComplaintCard from "../ComplaintCard";

import EmptyState from "../../common/EmptyState";

function ComplaintList({ complaints }) {
  if (!complaints.length) {
    return (
      <EmptyState
        title="No Complaints"
        message="You haven't raised any complaints yet."
        actionText="Raise Complaint"
        actionLink="/student/complaints/new"
      />
    );
  }

  return (
    <>
      {complaints.map((complaint) => (
        <ComplaintCard key={complaint.complaint_id} complaint={complaint} />
      ))}
    </>
  );
}

export default ComplaintList;
