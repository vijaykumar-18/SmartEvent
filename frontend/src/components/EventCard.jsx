import React from 'react';
import { Link } from 'react-router-dom';
import { Calendar, MapPin, Tag } from 'lucide-react';
import { formatINR } from '../utils/currency';

export default function EventCard({ event }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden flex flex-col hover:shadow-md transition">
     <img
  src={event.banner_image || 'https://images.unsplash.com/photo-1506157786151-b8491531f063?w=800&auto=format&fit=crop&q=60'}
  alt={event.title}
  onError={(e) => {
    e.target.onerror = null;
    e.target.src = 'https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=800&auto=format&fit=crop&q=60';
  }}
  className="w-full h-44 object-cover"
/>
      <div className="p-4 flex-1 flex flex-col">
        <span className="text-xs uppercase font-bold text-blue-600 mb-1">{event.category}</span>
        <h3 className="font-semibold text-slate-900 text-lg line-clamp-1 mb-2">{event.title}</h3>
        
        <div className="space-y-1 text-xs text-slate-500 mb-4 flex-1">
          <div className="flex items-center gap-1.5">
            <Calendar className="w-3.5 h-3.5" />
            <span>{new Date(event.event_date).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <MapPin className="w-3.5 h-3.5" />
            <span className="line-clamp-1">{event.venue}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <MapPin className="w-3.5 h-3.5" />
            <span className="line-clamp-1">{event.location}</span>
          </div>
        </div>

        <div className="flex items-center justify-between pt-3 border-t border-slate-100">
          <div>
            <span className="text-xs text-slate-400 block">Price</span>
            <span className="font-bold text-slate-900">{formatINR(event.ticket_price)}</span>
          </div>
          <Link
            to={`/events/${event.id}`}
            className="px-3 py-1.5 text-xs font-semibold text-blue-600 border border-blue-600 hover:bg-blue-50 rounded-lg transition"
          >
            View Details
          </Link>
        </div>
      </div>
    </div>
  );
}