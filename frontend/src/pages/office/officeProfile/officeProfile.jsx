import PageHeader from "../../../components/layout/PageHeader";

import ProfileCard from "../../../components/profile/ProfileCard";
import PersonalInfo from "../../../components/profile/PersonalInfo";
import HostelInfo from "../../../components/profile/HostelInfo";
import ProfileStatistics from "../../../components/profile/ProfileStatistics";

import useProfile from "../../../hooks/useProfile";

import Skeleton from "../../../components/common/Skeleton";
import ErrorState from "../../../components/common/ErrorState";

import "./officeProfile.css";

function OfficeProfile() {
  const { profile, loading, error, refresh } = useProfile();

  if (loading) {
    return <Skeleton height="500px" />;
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
    <div className="office-profile-page">
      <PageHeader
        title="Office Profile"
        subtitle="Manage your account information."
      />

      <ProfileCard profile={profile} />

      <PersonalInfo profile={profile} />

      <HostelInfo profile={profile} />

      <ProfileStatistics profile={profile} />
    </div>
  );
}

export default OfficeProfile;
