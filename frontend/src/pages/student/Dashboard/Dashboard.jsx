import "./Dashboard.css";

import AppLayout from "../../../components/layout/AppLayout";
import PageHeader from "../../../components/layout/PageHeader";

import WelcomeCard from "../../../components/student/dashboard/WelcomeCard";
import StatsGrid from "../../../components/student/dashboard/StatsGrid";
import RecentComplaints from "../../../components/student/dashboard/RecentComplaints";

import useDashboard from "../../../hooks/useDashboard";

import Skeleton from "../../../components/common/Skeleton";
import ErrorState from "../../../components/common/ErrorState";

function Dashboard() {
  const { dashboard, loading, error, refresh } = useDashboard();

  if (loading) {
    return (
      <>
        <div className="dashboard-page">
          <Skeleton height="80px" />

          <div className="stats-grid">
            <Skeleton height="120px" />

            <Skeleton height="120px" />

            <Skeleton height="120px" />

            <Skeleton height="120px" />
          </div>

          <Skeleton height="250px" />
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <ErrorState
          title="Unable to load Dashboard"
          message="Please check your internet connection or try again."
          onRetry={refresh}
        />
      </>
    );
  }

  return (
    <>
      <div className="dashboard-page">
        <PageHeader title="Dashboard" subtitle="Welcome back" />

        <WelcomeCard />

        <StatsGrid stats={dashboard.stats} />

        <RecentComplaints complaints={dashboard.recent_complaints} />
      </div>
    </>
  );
}

export default Dashboard;
