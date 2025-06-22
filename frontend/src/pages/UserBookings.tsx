// frontend/src/pages/UserBookingsPage.tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";
import { format, parseISO } from 'date-fns';

type Booking = {
  id: number;
  event_id: number;
  slot_id: number;
  name: string;
  email: string;
  created_at: string;
  event_name: string;
  slot_time: string; 
};

export default function UserBookingsPage() {
  const [email, setEmail] = useState("");
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const fetchBookings = async (userEmail: string) => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get(`/api/users/${encodeURIComponent(userEmail)}/bookings`);
      setBookings(response.data);
    } catch (err) {
      console.error("Failed to fetch bookings", err);
      setError("Failed to load bookings. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email.trim()) {
      fetchBookings(email.trim());
    }
  };

  const formatTime = (dateString: string) => {
    try {
      const date = parseISO(dateString);
      return format(date, 'MMM d, yyyy h:mm a');
    } catch (err) {
      return dateString;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6 bg-gray-50">
            <div className="flex justify-between items-start">
              <h1 className="text-2xl font-bold text-gray-900">My Bookings</h1>
              <button
                onClick={() => navigate(-1)}
                className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Back
              </button>
            </div>
          </div>

          <div className="px-4 py-5 sm:p-6">
            <form onSubmit={handleSubmit} className="mb-8">
              <div className="flex gap-4">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="flex-1 min-w-0 block w-full px-3 py-2 rounded-md border border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Enter your email to view bookings"
                  required
                />
                <button
                  type="submit"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  disabled={loading}
                >
                  {loading ? 'Loading...' : 'View Bookings'}
                </button>
              </div>
            </form>

            {error && (
              <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-md">
                {error}
              </div>
            )}

            {bookings.length > 0 ? (
              <div className="space-y-4">
                {bookings.map((booking) => (
                  <div key={booking.id} className="border rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="text-lg font-medium text-gray-900">
                          {booking.event_name}
                        </h3>
                        <p className="text-sm text-gray-500">
                          Booked on: {formatTime(booking.created_at)}
                        </p>
                        <p className="text-sm text-gray-500 mt-1">
                          Time Slot: {formatTime(booking.slot_time)}
                        </p>
                      </div>
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        Confirmed
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : null }
          </div>
        </div>
      </div>
    </div>
  );
}