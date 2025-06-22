import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { PlusIcon, TrashIcon, CalendarIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

type TimeSlotError = {
  time: string;
  error: string;
};

const SuccessNotification = () => (
  <div className="fixed top-4 right-4 z-50 animate-fade-in">
    <div className="bg-green-500 text-white px-6 py-4 rounded-lg shadow-lg flex items-center space-x-2">
      <CheckCircleIcon className="h-6 w-6" />
      <span>Event created successfully!</span>
    </div>
  </div>
);

const FormField = ({
  id,
  label,
  children,
}: {
  id: string;
  label: string;
  children: React.ReactNode;
}) => (
  <div>
    <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
      {label}
    </label>
    {children}
  </div>
);

export default function CreateEventPage() {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    creatorName: '',
    maxBookings: 1,
    slots: [''] as string[],
  });
  const [showSuccess, setShowSuccess] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (showSuccess) {
      const timer = setTimeout(() => {
        setShowSuccess(false);
        navigate('/');
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [showSuccess, navigate]);

  const handleInputChange = (field: keyof typeof formData, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: typeof value === 'number' ? Math.max(1, value) : value,
    }));
  };

  const handleSlotChange = (index: number, value: string) => {
    const updatedSlots = [...formData.slots];
    updatedSlots[index] = value;
    handleInputChange('slots', updatedSlots);
  };

  const addSlot = () => handleInputChange('slots', [...formData.slots, '']);
  const removeSlot = (index: number) =>
    handleInputChange(
      'slots',
      formData.slots.filter((_, i) => i !== index)
    );

  const formatError = (error: any): string => {
    if (!error?.response?.data) {
      return error?.message || 'An unexpected error occurred';
    }

    const errorData = error.response.data.detail || error.response.data;
    
    if (errorData.errors?.slots) {
      const slotErrors = Array.isArray(errorData.errors.slots)
        ? errorData.errors.slots
            .map((e: TimeSlotError) => `• ${e.time || 'Unknown time'}: ${e.error || 'Invalid slot'}`)
            .join('\n')
        : 'Invalid time slots';
      
      return [
        errorData.detail || 'One or more time slots are invalid:',
        '',
        slotErrors,
      ].join('\n');
    }

    return errorData.detail || errorData.message || 'An error occurred';
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.creatorName.trim()) {
      alert('Please enter your name');
      return;
    }

    try {
      const slotDatetimes = formData.slots.map(slot => new Date(slot).toISOString());
      
      await api.post('/api/events', {
        name: formData.name,
        description: formData.description,
        created_by: formData.creatorName.trim(),
        max_bookings_per_slot: formData.maxBookings,
        slots: slotDatetimes,
      });

      setShowSuccess(true);
    } catch (error: any) {
      console.error('Error creating event:', error);
      alert(formatError(error));
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8 relative">
      {showSuccess && <SuccessNotification />}
      
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="p-8">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-extrabold text-gray-900">Create New Event</h1>
              <p className="mt-2 text-sm text-gray-600">Fill in the details below to create your event</p>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <FormField id="event-name" label="Event Name">
                <input
                  id="event-name"
                  type="text"
                  className="block w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200"
                  placeholder="Enter event name"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  required
                />
              </FormField>

              <FormField id="description" label="Description">
                <textarea
                  id="description"
                  rows={3}
                  className="block w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200"
                  placeholder="Tell us about your event..."
                  value={formData.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                  required
                />
              </FormField>

              <FormField id="creator-name" label="Your Name (Creator)">
                <input
                  id="creator-name"
                  type="text"
                  className="block w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200"
                  placeholder="Enter your name"
                  value={formData.creatorName}
                  onChange={(e) => handleInputChange('creatorName', e.target.value)}
                  required
                />
              </FormField>

              <FormField id="max-bookings" label="Maximum Bookings per Slot">
                <input
                  id="max-bookings"
                  type="number"
                  min={1}
                  className="block w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200"
                  placeholder="e.g. 10"
                  value={formData.maxBookings}
                  onChange={(e) => handleInputChange('maxBookings', parseInt(e.target.value) || 1)}
                  required
                />
              </FormField>

              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <label className="block text-sm font-medium text-gray-700">
                    Event Slots
                  </label>
                  <button
                    type="button"
                    onClick={addSlot}
                    className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                  >
                    <PlusIcon className="-ml-0.5 mr-1.5 h-4 w-4" />
                    Add Slot
                  </button>
                </div>

                {formData.slots.map((slot: string, idx: number) => (
                  <div key={idx} className="flex items-center space-x-2">
                    <div className="relative flex-1">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <CalendarIcon className="h-5 w-5 text-gray-400" />
                      </div>
                      <input
                        type="datetime-local"
                        value={slot}
                        onChange={(e) => handleSlotChange(idx, e.target.value)}
                        className="block w-full pl-10 pr-3 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200"
                        required
                      />
                    </div>
                    {formData.slots.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeSlot(idx)}
                        className="inline-flex items-center p-2 border border-transparent rounded-full text-red-600 hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
                      >
                        <TrashIcon className="h-5 w-5" />
                      </button>
                    )}
                  </div>
                ))}
              </div>

              <div className="pt-2">
                <button
                  type="submit"
                  className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                >
                  Create Event
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
