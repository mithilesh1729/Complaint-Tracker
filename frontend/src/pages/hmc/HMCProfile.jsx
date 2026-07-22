import PageHeader from "../../components/layout/PageHeader";

import ProfileCard from "../../components/profile/ProfileCard";
import PersonalInfo from "../../components/profile/PersonalInfo";
import ProfileStatistics from "../../components/profile/ProfileStatistics";
import ChangePasswordForm from "../../components/profile/ChangePasswordForm";

import useProfile from "../../hooks/useProfile";

import Skeleton from "../../components/common/Skeleton";
import ErrorState from "../../components/common/ErrorState";

function HMCProfile() {
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
    <div className="hmc-profile-page p-4" style={{ display: 'flex', flexDirection: 'column', gap: '24px', paddingBottom: '40px', maxWidth: '1200px', margin: '0 auto' }}>
      <PageHeader
        title="HMC Profile"
        subtitle="Manage your account information."
      />

      <ProfileCard profile={profile} />
      <PersonalInfo profile={profile} />
      <ProfileStatistics profile={profile} />
      <ChangePasswordForm />
    </div>
  );
}

export default HMCProfile;
