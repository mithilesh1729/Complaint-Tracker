import { useEffect, useState } from "react";

import profileService from "../services/profileService";

export default function useProfile() {
  const [profile, setProfile] = useState(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState(null);

  async function fetchProfile() {
    try {
      setLoading(true);

      const data = await profileService.getProfile();

      setProfile(data);

      setError(null);
    } catch (err) {
      console.error(err);

      setError(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchProfile();
  }, []);

  return {
    profile,
    loading,
    error,
    refresh: fetchProfile,
  };
}
