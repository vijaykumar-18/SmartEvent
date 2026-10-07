import React, { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

export default function ProtectedRoute() {
  const { user, loading } = useContext(AuthContext);
  if (loading) return <div className="py-20 text-center text-slate-500">Loading your account...</div>;
  return user ? <Outlet /> : <Navigate to="/login" replace />;
}