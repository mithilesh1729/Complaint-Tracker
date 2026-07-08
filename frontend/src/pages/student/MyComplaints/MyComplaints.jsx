import AppLayout from "../../../components/layout/AppLayout";
import PageHeader from "../../../components/layout/PageHeader";

import ComplaintList from "../../../components/complaint/ComplaintList";

import Skeleton from "../../../components/common/Skeleton";
import ErrorState from "../../../components/common/ErrorState";

import useComplaints from "../../../hooks/useComplaints";

function MyComplaints() {
  const { complaints, loading, error, refresh } = useComplaints();

  if (loading) {
    return (
      <>
        <Skeleton height="400px" />
      </>
    );
  }

  if (error) {
    return (
      <>
        <ErrorState
          title="Unable to load complaints"
          message="Please try again."
          onRetry={refresh}
        />
      </>
    );
  }

  return (
    <>
      <PageHeader title="My Complaints" subtitle="Track all your complaints" />

      <ComplaintList complaints={complaints} />
    </>
  );
}

export default MyComplaints;
