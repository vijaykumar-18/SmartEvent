import React from 'react';
import { useLocation, Link, Navigate } from 'react-router-dom';
import { CheckCircle, ArrowLeft } from 'lucide-react';
import { assetBaseUrl } from '../api/axios';

export default function BookingConfirmation() {
  const { state } = useLocation();
  const booking = state?.booking;

  if (!booking) return <Navigate to="/" replace />;

  return (
    <div className="max-w-2xl mx-auto px-4 py-12 text-center">
      <CheckCircle className="w-16 h-16 text-emerald-500 mx-auto mb-4" />
      <h1 className="text-2xl font-bold text-slate-900">Booking Confirmed!</h1>
      <p className="text-sm text-slate-600 mt-1">
        Booking Reference #{booking.id} — Total: ${booking.total_price.toFixed(2)}
      </p>

      <div className="mt-8 space-y-4">
        {booking.tickets.map((t) => (
          <div key={t.id} className="p-4 bg-white border border-slate-200 rounded-xl flex items-center justify-between shadow-sm">
            <div className="text-left">
              <span className="text-xs font-mono text-slate-400">TICKET PASS</span>
              <p className="font-bold text-slate-800">{t.ticket_code}</p>
            </div>
            <img
              src={`${assetBaseUrl}${t.qr_code_url}`}
              alt={t.ticket_code}
              className="w-20 h-20 border border-slate-200 rounded-lg p-1"
            />
          </div>
        ))}
      </div>

      <div className="mt-8 flex justify-center gap-4">
        <Link
          to="/bookings"
          className="px-6 py-2.5 bg-blue-600 text-white rounded-lg text-sm font-semibold hover:bg-blue-700 flex items-center gap-2"
        >
          Go to Booking History
        </Link>
        <Link
          to="/"
          className="px-6 py-2.5 border border-slate-300 text-slate-700 rounded-lg text-sm font-semibold hover:bg-slate-50 flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" /> Browse More
        </Link>
      </div>
    </div>
  );
}