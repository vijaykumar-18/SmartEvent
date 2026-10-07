import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Calendar, Ticket, User, LogOut } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import NotificationDropdown from './NotificationDropdown';

export default function Navbar() {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-bold text-xl text-blue-600">
          <Calendar className="w-6 h-6" />
          <span>SmartEvent</span>
        </Link>

        <div className="flex items-center gap-4">
          <Link to="/" className="text-sm font-medium text-slate-600 hover:text-blue-600">Discover</Link>
          {user ? (
            <>
              <Link to="/bookings" className="text-sm font-medium text-slate-600 hover:text-blue-600 flex items-center gap-1">
                <Ticket className="w-4 h-4" /> Bookings
              </Link>
              <Link to="/tickets" className="text-sm font-medium text-slate-600 hover:text-blue-600">Tickets</Link>
              <NotificationDropdown />
              <div className="flex items-center gap-3 pl-2 border-l border-slate-200">
                <span className="text-sm font-semibold text-slate-700 flex items-center gap-1">
                  <User className="w-4 h-4" /> {user.username}
                </span>
                <button
                  onClick={() => { logout(); navigate('/login'); }}
                  className="p-2 text-slate-500 hover:text-rose-600"
                  title="Logout"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <Link to="/login" className="px-4 py-2 text-sm font-medium text-slate-700 hover:text-blue-600">Sign In</Link>
              <Link to="/register" className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg">Register</Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}