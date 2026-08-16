import { createContext } from "react";

import type {
  LoginRequest,
  RegisterRequest,
  User,
} from "../api/auth";

export interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (data: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);
