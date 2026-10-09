import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import EventDetail from './pages/EventDetail';
import BookingConfirmation from './pages/BookingConfirmation';
import BookingHistory from './pages/BookingHistory';
import Tickets from './pages/Tickets';
import Notifications from './pages/Notifications';
import {
  OrganizerDashboard,
  OrganizerEvents,
  OrganizerEventForm,
  OrganizerEventBookings,
} from './pages/OrganizerPages';
import AdminDashboard from './pages/AdminDashboard';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/events/:id" element={<EventDetail />} />

              {/* Protected User Endpoints */}
              <Route element={<ProtectedRoute />}>
                <Route path="/confirmation" element={<BookingConfirmation />} />
                <Route path="/notifications" element={<Notifications />} />
              </Route>
              <Route element={<ProtectedRoute roles={['USER']} />}>
                <Route path="/bookings" element={<BookingHistory />} />
                <Route path="/tickets" element={<Tickets />} />
              </Route>
              <Route element={<ProtectedRoute roles={['ORGANIZER']} />}>
                <Route path="/organizer" element={<OrganizerDashboard />} />
                <Route path="/organizer/events" element={<OrganizerEvents />} />
                <Route path="/organizer/events/new" element={<OrganizerEventForm />} />
                <Route path="/organizer/events/:eventId/edit" element={<OrganizerEventForm />} />
                <Route path="/organizer/events/:eventId/bookings" element={<OrganizerEventBookings />} />
              </Route>
              <Route element={<ProtectedRoute roles={['ADMIN']} />}>
                <Route path="/admin/*" element={<AdminDashboard />} />
              </Route>
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}