import { createContext, useState, useEffect, useCallback } from "react";

import authService from "../services/authService";
import { storage } from "../utils/storage";

import getDashboardRoute from "../utils/getDashboardRoute"; ///

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const [loading, setLoading] = useState(true);

  /**
   * Fetch currently logged in user
   */
  const refreshProfile = useCallback(async () => {
    try {
      const response = await authService.profile();

      setUser(response.data);

      return response.data;
    } catch (error) {
      storage.clear();
      setUser(null);
      return null;
    }
  }, []);

  /**
   * Login
   */
  const login = async (credentials) => {
    const response = await authService.login(credentials);

    storage.setAccessToken(response.data.access);

    storage.setRefreshToken(response.data.refresh);

    const user = await refreshProfile();

    return getDashboardRoute(user.role);
  };

  /**
   * Logout
   */
  const logout = async () => {
    try {
      const refreshToken = storage.getRefreshToken();
      if (refreshToken) {
        await authService.logout(refreshToken);
      }
    } catch (error) {
      console.error("Logout API failed, but clearing local session anyway.", error);
    } finally {
      storage.clear();
      setUser(null);
    }
  };

  /**
   * Restore session on page refresh
   */
  useEffect(() => {
    async function initializeAuth() {
      try {
        if (storage.getAccessToken()) {
          await refreshProfile();
        }
      } finally {
        setLoading(false);
      }
    }

    initializeAuth();
  }, [refreshProfile]);

  const value = {
    user,

    loading,

    isAuthenticated: !!user,

    login,

    logout,

    refreshProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
