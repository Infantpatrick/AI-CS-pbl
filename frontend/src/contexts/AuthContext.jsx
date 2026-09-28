import React, { createContext, useState, useEffect, useContext } from 'react';
import { getMe, login as apiLogin, logout as apiLogout, register as apiRegister } from '../api/auth';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [authStatus, setAuthStatus] = useState('checking'); // checking, authenticated, unauthenticated

  const refreshUser = async () => {
    setAuthStatus('checking');
    const res = await getMe();
    if (res.success) {
      setUser(res.data);
      setAuthStatus('authenticated');
    } else {
      setUser(null);
      setAuthStatus('unauthenticated');
    }
  };

  useEffect(() => {
    refreshUser();
  }, []);

  const login = async (email, password) => {
    const res = await apiLogin(email, password);
    if (res.success) {
      setUser(res.data);
      setAuthStatus('authenticated');
      return { success: true };
    }
    return res;
  };

  const logout = async () => {
    await apiLogout();
    setUser(null);
    setAuthStatus('unauthenticated');
  };

  const register = async (name, email, password) => {
    return await apiRegister(name, email, password);
  };

  return (
    <AuthContext.Provider value={{ user, authStatus, login, logout, register, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};
