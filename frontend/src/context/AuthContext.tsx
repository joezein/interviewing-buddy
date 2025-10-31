'use client';

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { api, type User } from "../lib/api";

interface AuthContextValue {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const STORAGE_KEY = "interview-buddy-token";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const loadUser = useCallback(async (authToken: string) => {
    try {
      const currentUser = await api.getCurrentUser(authToken);
      setUser(currentUser);
    } catch (error) {
      console.error(error);
      setUser(null);
      setToken(null);
      window.localStorage.removeItem(STORAGE_KEY);
      throw error;
    }
  }, []);

  const refreshUser = useCallback(async () => {
    if (!token) return;
    await loadUser(token);
  }, [loadUser, token]);

  const loginHandler = useCallback(
    async (email: string, password: string) => {
      setLoading(true);
      try {
        const result = await api.login(email, password);
        window.localStorage.setItem(STORAGE_KEY, result.access_token);
        setToken(result.access_token);
        await loadUser(result.access_token);
      } finally {
        setLoading(false);
      }
    },
    [loadUser]
  );

  const logoutHandler = useCallback(() => {
    setToken(null);
    setUser(null);
    window.localStorage.removeItem(STORAGE_KEY);
  }, []);

  useEffect(() => {
    const storedToken = window.localStorage.getItem(STORAGE_KEY);
    if (!storedToken) {
      setLoading(false);
      return;
    }

    setToken(storedToken);
    loadUser(storedToken)
      .catch(() => {
        window.localStorage.removeItem(STORAGE_KEY);
      })
      .finally(() => setLoading(false));
  }, [loadUser]);

  const value = useMemo(
    () => ({ user, token, loading, login: loginHandler, logout: logoutHandler, refreshUser }),
    [user, token, loading, loginHandler, logoutHandler, refreshUser]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
