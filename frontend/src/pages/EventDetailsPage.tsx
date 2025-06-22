import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../services/api";
import { format, parseISO } from 'date-fns';
import { toZonedTime } from 'date-fns-tz';

type Slot = {
  id: number;
  time: string;
  available_slots: number;
};

type Event = {
  id: number;
  name: string;
  description: string;
  created_by: string;
  max_bookings_per_slot: number;
  slots: Slot[];
};

type BookingFormData = {
  name: string;
  email: string;
  slotId: number | null;
};

export default function EventDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [event, setEvent] = useState<Event | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [bookingSuccess, setBookingSuccess] = useState(false);
  const [formData, setFormData] = useState<BookingFormData>({
    name: "",
    email: "",
    slotId: null,
  });

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        setLoading(true);
        const response = await api.get(`/api/events/${id}`);
        setEvent(response.data);
      } catch {
        setError("Failed to load event details. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchEvent();
  }, [id]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSlotSelect = (slotId: number) => {
    setFormData(prev => ({
      ...prev,
      slotId: prev.slotId === slotId ? null : slotId
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.slotId) {
      alert("Please select a time slot");
      return;
    }

    try {
      const selectedSlot = event?.slots.find(slot => slot.id === formData.slotId);
      if (!selectedSlot) {
        throw new Error('Selected slot not found');
      }

      const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      
      const isoString = selectedSlot.time.replace(' ', 'T') + 'Z';
      const utcDate = new Date(isoString);
      const localTimeString = format(utcDate, "EEEE, MMMM d, yyyy 'at' h:mm a");

      await api.post(`/api/events/${id}/bookings`, {
        name: formData.name,
        email: formData.email,
        slot_id: formData.slotId,
        slot_time: localTimeString,
        timezone: userTimeZone
      });
      
      setBookingSuccess(true);
      setFormData({ name: "", email: "", slotId: null });
      
      const response = await api.get(`/api/events/${id}`);
      setEvent(response.data);
      
      setTimeout(() => setBookingSuccess(false), 3000);
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 
                         err.response?.data?.detail || 
                         err.response?.data?.message || 
                         err.message ||
                         "Failed to book slot. Please try again.";
      alert(`Error: ${errorMessage}`);
    }
  };

  const formatTime = (utcDateString: string) => {
    try {
      const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      const userLocalTime = toZonedTime(utcDateString, userTimeZone);
      return format(userLocalTime, 'PPPpp (zzzz)');
    } catch (error) {
      console.error('Error formatting time:', error);
      return format(parseISO(utcDateString), 'PPPpp');
    }
  };

  const formatTimeSimple = (utcDateString: string) => {
    try {
      // Parse the UTC time string (format: "2025-06-27 00:28:00")
      // Convert it to ISO format that date-fns can understand
      const isoString = utcDateString.replace(' ', 'T') + 'Z';
      
      const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      const utcDate = new Date(isoString);
      
      // Format the date in user's local timezone
      return {
        date: format(utcDate, 'EEEE, MMMM d, yyyy'), // e.g., "Friday, June 27, 2025"
        time: format(utcDate, 'h:mm a'), // e.g., "5:58 AM" (for IST timezone)
        timezone: userTimeZone.replace('_', ' ')
      };
    } catch (error) {
      console.error('Error formatting time:', error);
      return {
        date: 'Invalid date',
        time: '--:--',
        timezone: '--'
      };
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
        <div className="text-center max-w-md">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
            <svg className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Event</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!event) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-600">Event not found</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6 bg-gray-50">
            <div className="flex justify-between items-start">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{event.name}</h1>
                <p className="mt-1 text-sm text-gray-500">
                  Created by {event.created_by || 'Unknown'}
                </p>
              </div>
              <button
                onClick={() => navigate(-1)}
                className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Back to Events
              </button>
            </div>
          </div>

          <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="md:col-span-2 space-y-6">
                <div>
                  <h2 className="text-lg font-medium text-gray-900">Description</h2>
                  <p className="mt-2 text-gray-600 whitespace-pre-line">
                    {event.description || 'No description provided.'}
                  </p>
                </div>

                <div>
                  <h2 className="text-lg font-medium text-gray-900 mb-4">Available Time Slots</h2>
                  {event.slots && event.slots.length > 0 ? (
                    <div className="grid grid-cols-1 gap-3">
                      {event.slots.map((slot) => (
                        <button
                          key={slot.id}
                          type="button"
                          onClick={() => handleSlotSelect(slot.id)}
                          className={`flex justify-between items-center p-4 border rounded-lg text-left transition-colors ${
                            formData.slotId === slot.id
                              ? 'border-blue-500 bg-blue-50'
                              : 'border-gray-200 hover:border-blue-300'
                          }`}
                        >
                          <div>
                            <div className="font-medium">
                              <div className="text-gray-900">
                                {formatTimeSimple(slot.time).date}
                              </div>
                              <div className="flex items-center">
                                <span className="text-lg font-semibold">
                                  {formatTimeSimple(slot.time).time}
                                </span>
                                <span className="text-sm text-gray-500 ml-2">
                                  ({formatTimeSimple(slot.time).timezone})
                                </span>
                              </div>
                            </div>
                            <p className="text-sm text-gray-500 mt-1">
                              {slot.available_slots} of {event.max_bookings_per_slot} slots available
                            </p>
                          </div>
                          <div className={`flex-shrink-0 h-5 w-5 rounded-full border-2 ${
                            formData.slotId === slot.id 
                              ? 'border-blue-500 bg-blue-500' 
                              : 'border-gray-300'
                          }`}>
                            {formData.slotId === slot.id && (
                              <div className="h-2 w-2 bg-white rounded-full m-0.5" />
                            )}
                          </div>
                        </button>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500">No time slots available for this event.</p>
                  )}
                </div>
              </div>

              <div className="md:col-span-1">
                <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
                  <h2 className="text-lg font-medium text-gray-900 mb-4">Book Your Slot</h2>
                  
                  {bookingSuccess && (
                    <div className="mb-4 p-3 bg-green-50 text-green-800 text-sm rounded-md">
                      Booking successful! You'll receive a confirmation email shortly.
                    </div>
                  )}

                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                      <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                        Full Name
                      </label>
                      <input
                        type="text"
                        id="name"
                        name="name"
                        required
                        value={formData.name}
                        onChange={handleInputChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        placeholder="Your name"
                      />
                    </div>

                    <div>
                      <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                        Email Address
                      </label>
                      <input
                        type="email"
                        id="email"
                        name="email"
                        required
                        value={formData.email}
                        onChange={handleInputChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        placeholder="your.email@example.com"
                      />
                    </div>

                    <div className="pt-2">
                      <button
                        type="submit"
                        disabled={!formData.slotId}
                        className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
                          formData.slotId
                            ? 'bg-blue-600 hover:bg-blue-700'
                            : 'bg-gray-400 cursor-not-allowed'
                        } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
                      >
                        {formData.slotId ? 'Book Now' : 'Select a time slot'}
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
