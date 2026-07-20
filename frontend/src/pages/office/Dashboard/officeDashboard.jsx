import PageHeader from "../../../components/layout/PageHeader";

import Skeleton from "../../../components/common/Skeleton";
import ErrorState from "../../../components/common/ErrorState";

import DashboardStats from "../../../components/office/DashboardStats";
import QuickActions from "../../../components/office/QuickActions";
import RecentComplaints from "../../../components/office/RecentComplaints";

import useOfficeDashboard from "../../../hooks/useOfficeDashboard";

import "./officeDashboard.css";

function OfficeDashboard() {
  const { dashboard, loading, error, refresh } = useOfficeDashboard();

  if (loading) {
    return <Skeleton height="650px" />;
  }

  if (error) {
    return (
      <ErrorState
        title="Unable to load dashboard"
        message="Please try again."
        onRetry={refresh}
      />
    );
  }

  return (
    <div className="office-dashboard-page">
      <PageHeader
        title="Office Dashboard"
        subtitle="Manage hostel complaints efficiently."
      />

      <DashboardStats stats={dashboard.stats} />

      <QuickActions />

      <RecentComplaints complaints={dashboard.recent_complaints} />
    </div>
  );
}

export default OfficeDashboard;
