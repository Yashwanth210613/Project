import { createContext, useContext, useMemo, useState } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [role, setRole] = useState(localStorage.getItem('role'));

  const value = useMemo(
    () => ({
      token,
      role,
      login: (newToken, newRole) => {
        localStorage.setItem('token', newToken);
        localStorage.setItem('role', newRole);
        setToken(newToken);
        setRole(newRole);
      },
      logout: () => {
        localStorage.clear();
        setToken(null);
        setRole(null);
      },
    }),
    [token, role]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);
