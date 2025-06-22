import { useEffect, useState } from "react";
import { api } from "../services/api";
import { Link } from "react-router-dom";

type Event = {
  id: number;
  name: string;
  description: string;
  created_by: string;
  created_at: string;
  max_bookings_per_slot: number;
};

export default function HomePage() {
  const [events, setEvents] = useState<Event[]>([]);

  useEffect(() => {
    api.get('/api/events')
      .then(res => {setEvents(res.data)})
      .catch(err => console.error("Failed to load events", err));
  }, []);

  const renderCreateButton = (
    <div className="mt-8 flex gap-4 justify-center">
      <Link
        to="/create-event"
        className="inline-flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-white bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700 transition-colors whitespace-nowrap">
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path
            fillRule="evenodd"
            d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 01-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
            clipRule="evenodd"/>
        </svg>
        Create New Event
      </Link>
      <Link
        to="/user-bookings"
        className="px-4 py-2.5 border border-gray-300 text-sm font-medium rounded-lg shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
        My Bookings
      </Link>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto space-y-10">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <h1 className="text-3xl font-bold text-gray-800">Available Events</h1>
        </div>

        {/* Event List */}
        <div className="mb-10">  {/* Added margin bottom */}
          <div className="flex justify-end w-full">
            {renderCreateButton}
          </div>
        </div>

        {events.length === 0 ? (
          <div className="bg-white rounded-xl shadow p-10 text-center space-y-4">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <h3 className="text-lg font-semibold text-gray-700">No events yet</h3>
            <p className="text-sm text-gray-500">Get started by creating your first event.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {events.map((event) => (
              <div
                key={event.id}
                className="bg-white rounded-xl shadow hover:shadow-md transition duration-200 border"
              >
                <div className="p-6 space-y-3">
                  <div>
                    <h2 className="text-xl font-semibold text-gray-800">{event.name}</h2>
                    <p className="text-sm text-gray-500 mt-1">
                      Created by {event.created_by || 'Unknown'}
                    </p>
                  </div>
                  <p className="text-gray-600 line-clamp-2">
                    {event.description}
                  </p>
                  <Link
                    to={`/events/${event.id}`}
                    className="text-sm font-medium text-blue-600 hover:text-blue-800"
                  >
                    View details →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
