import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Calendar, MapPin } from 'lucide-react';
import api from '../api/axios';
import { AuthContext } from '../context/AuthContext';
import { formatINR } from '../utils/currency';

export default function EventDetail() {
  const { id } = useParams();
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  const [event, setEvent] = useState(null);
  const [qty, setQty] = useState(1);
  const [bookingLoading, setBookingLoading] = useState(false);
  const [eventLoading, setEventLoading] = useState(true);
  const [eventError, setEventError] = useState('');
  const [error, setError] = useState('');
  const canBook = !user || user.role === 'USER';

  useEffect(() => {
    api.get(`/events/${id}`)
      .then(res => setEvent(res.data))
      .catch(() => setEventError('Unable to load this event. It may have been removed.'))
      .finally(() => setEventLoading(false));
  }, [id]);

  const handleBooking = async () => {
    if (!user) {
      navigate('/login');
      return;
    }
    if (qty < 1 || qty > event.available_tickets || qty > 10) {
      setError('Choose a quantity within the available ticket limit (maximum 10).');
      return;
    }
    setBookingLoading(true);
    setError('');
    try {
      const res = await api.post('/bookings', {
        event_id: Number(id),
        ticket_quantity: Number(qty)
      });
      navigate('/confirmation', { state: { booking: res.data } });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to complete booking.');
    } finally {
      setBookingLoading(false);
    }
  };

  if (eventLoading) return <div className="py-20 text-center">Loading event details...</div>;
  if (eventError || !event) return <div role="alert" className="mx-auto max-w-2xl px-4 py-20 text-center text-rose-700">{eventError || 'Event not found.'}</div>;

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <img
          src={event.banner_image || 'https://images.unsplash.com/photo-1506157786151-b8491531f063?w=1200&auto=format&fit=crop&q=80'}
          alt={event.title}
          className="w-full h-80 object-cover"
        />

        <div className="p-6 sm:p-8 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-2 space-y-4">
            <span className="text-xs uppercase font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
              {event.category}
            </span>
            <h1 className="text-3xl font-bold text-slate-900">{event.title}</h1>
            <span className={`inline-flex rounded-full px-3 py-1 text-xs font-bold ${
              event.event_status === 'CANCELLED'
                ? 'bg-rose-100 text-rose-700'
                : event.event_status === 'COMPLETED'
                  ? 'bg-slate-100 text-slate-700'
                  : event.event_status === 'ONGOING'
                    ? 'bg-emerald-100 text-emerald-700'
                    : 'bg-blue-100 text-blue-700'
            }`}>{event.event_status}</span>
            {event.event_status === 'CANCELLED' && (
              <p role="alert" className="rounded-lg border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700">
                This event has been cancelled. Ticket booking is unavailable.
              </p>
            )}
            
            <div className="flex flex-wrap gap-4 text-sm text-slate-600">
              <div className="flex items-center gap-1.5">
                <Calendar className="w-4 h-4 text-blue-600" />
                <span>{new Date(event.event_date).toLocaleString()}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <MapPin className="w-4 h-4 text-blue-600" />
                <span>{event.location}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <MapPin className="w-4 h-4 text-blue-600" />
                <span>{event.venue}</span>
              </div>
            </div>

            <hr className="border-slate-100" />
            <div>
              <h2 className="text-lg font-semibold text-slate-800 mb-2">About this event</h2>
              <p className="text-slate-600 text-sm leading-relaxed whitespace-pre-line">{event.description}</p>
            </div>
          </div>

          {/* Booking Card */}
          <div className="bg-slate-50 border border-slate-200 p-6 rounded-xl flex flex-col justify-between h-fit">
            <div>
              <div className="flex justify-between items-baseline mb-4">
                <span className="text-sm text-slate-500">Price per ticket</span>
                <span className="text-2xl font-black text-slate-900">{formatINR(event.ticket_price)}</span>
              </div>

              {canBook && event.event_status === 'UPCOMING' && <div className="mb-4">
                <label className="block text-xs font-semibold text-slate-700 mb-1">Select Quantity</label>
                <input
                  type="number"
                  min="1"
                  max={Math.min(event.available_tickets, 10)}
                  value={qty}
                  onChange={(e) => setQty(Math.max(1, parseInt(e.target.value) || 1))}
                  className="w-full border border-slate-300 rounded-lg p-2 text-sm bg-white"
                />
                <span className="text-[11px] text-slate-400 mt-1 block">
                  Available tickets: {event.available_tickets}
                </span>
              </div>}

              {canBook && event.event_status === 'UPCOMING' && <div className="border-t border-slate-200 pt-3 mb-6">
                <div className="flex justify-between font-bold text-slate-800 text-sm">
                  <span>Total Amount</span>
                  <span>{formatINR(event.ticket_price * qty)}</span>
                </div>
              </div>}

              {error && <p className="text-xs text-rose-600 mb-4">{error}</p>}
            </div>

            {canBook && event.event_status === 'UPCOMING' ? <button
              onClick={handleBooking}
              disabled={bookingLoading || event.available_tickets <= 0}
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg text-sm transition disabled:opacity-50"
            >
              {event.available_tickets <= 0 ? 'Sold Out' : bookingLoading ? 'Reserving...' : 'Book Tickets Now'}
            </button> : <p className="text-center text-sm font-semibold text-slate-600">
              {user && user.role !== 'USER'
                ? 'Ticket booking is available to user accounts.'
                : event.event_status === 'CANCELLED'
                  ? 'This event has been cancelled.'
                  : 'Ticket booking is closed for this event.'}
            </p>}
          </div>
        </div>
      </div>
    </div>
  );
}