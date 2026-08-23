import {
  useEffect,
  useState,
  type ReactNode,
} from "react";

import {
  getCurrentUser,
  login as loginApi,
  logout as logoutApi,
  register as registerApi,
  refresh as refreshApi,
  type LoginRequest,
  type RegisterRequest,
  type User,
} from "../api/auth";

import { AuthContext } from "./auth-context";


interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        let token = localStorage.getItem("access_token");
  
        if (!token) {
          const response = await refreshApi();
          token = response.access_token;
  
          localStorage.setItem("access_token", token);
        }
  
        const currentUser = await getCurrentUser();
        setUser(currentUser);
      } catch {
        localStorage.removeItem("access_token");
      } finally {
        setLoading(false);
      }
    };
  
    initializeAuth();
  }, []);

  const login = async (data: LoginRequest) => {
    const response = await loginApi(data);

    localStorage.setItem(
      "access_token",
      response.access_token
    );

    const currentUser = await getCurrentUser();
    setUser(currentUser);
  };

  const register = async (data: RegisterRequest) => {
    await registerApi(data);

    await login({
      email: data.email,
      password: data.password,
    });
  };

  const logout = async () => {
    try {
      await logoutApi();
    } finally {
      localStorage.removeItem("access_token");
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}