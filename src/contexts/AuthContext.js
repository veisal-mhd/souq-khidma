import React, { createContext, useState, useContext } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  const register = async (formData) => {
    try {
      // POST avec le slash final pour Django
      const response = await axios.post('http://127.0.0.1:8000/api/accounts/register/', formData);
      
      // Si ton backend renvoie un token JWT après l'inscription
      if (response.data.access) {
        localStorage.setItem('token', response.data.access);
        setUser(response.data.user);
      }
      return { success: true };
    } catch (error) {
      console.error("Erreur Django détaillée:", error.response?.data);
      return { 
        success: false, 
        error: error.response?.data 
      };
    }
  };

  return (
    <AuthContext.Provider value={{ user, register, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);