"use client";

import {
  createContext,
  PropsWithChildren,
  useContext,
  useEffect,
  useLayoutEffect,
  useState,
} from "react";

// Define the authentication state interface
interface AuthState extends AuthenticatedUserResponse {}

// Create an initial state for authentication
const initialAuthState: AuthState = {
  access_token: "",
  token_type: "",
  username: "",
  id: "",
};

// Create a context for authentication state and actions
const AuthContext = createContext<{
  authState: AuthState;
  login: (data: AuthState) => void;
  logout: () => void;
}>({
  authState: initialAuthState,
  login: () => {},
  logout: () => {},
});

// Custom hook to access the AuthContext
export const useAuth = () => useContext(AuthContext);

// AuthProvider component to wrap your app
export const AuthProvider = ({ children }: PropsWithChildren<{}>) => {
  const [authState, setAuthState] = useState<AuthState>(initialAuthState);
  const USER_SESION = "USER_SESION";
  const login = (data: AuthState) => {
    setAuthState(data);
  };

  const logout = () => {
    setAuthState(initialAuthState);
    localStorage.removeItem(USER_SESION);
  };

  const contextValue = {
    authState,
    login,
    logout,
  };

  useLayoutEffect(() => {
    if (authState.access_token) {
      localStorage.setItem(USER_SESION, JSON.stringify(authState));
    }
  }, [authState]);

  useEffect(() => {
    const state = localStorage.getItem(USER_SESION);

    if (state !== null) {
      setAuthState(JSON.parse(state));
    }
  }, []);

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
};
