import PageHeader from "../../../components/layout/PageHeader";

import Skeleton from "../../../components/common/Skeleton";
import ErrorState from "../../../components/common/ErrorState";

import ProfileCard from "../../../components/profile/ProfileCard";
import PersonalInfo from "../../../components/profile/PersonalInfo";
import HostelInfo from "../../../components/profile/HostelInfo";

import useProfile from "../../../hooks/useProfile";

import "./MyProfile.css";

function MyProfile() {
  const { profile, loading, error, refresh } = useProfile();

  if (loading) {
    return <Skeleton height="650px" />;
  }

  if (error) {
    return (
      <ErrorState
        title="Unable to load profile"
        message="Please try again."
        onRetry={refresh}
      />
    );
  }

  return (
    <div className="profile-page">
      <PageHeader
        title="My Profile"
        subtitle="View your personal and hostel information."
      />

      <ProfileCard profile={profile} />

      <PersonalInfo profile={profile} />

      <HostelInfo profile={profile} />
    </div>
  );
}

export default MyProfile;
