import { useEffect, useState } from "react";
import { api } from "../services/api";

type Event = {
  id: number;
  name: string;
  description: string;
  max_bookings_per_slot: number;
};

export default function HomePage() {
  const [events, setEvents] = useState<Event[]>([]);

  useEffect(() => {
    api.get('/events')
      .then(res => setEvents(res.data))
      .catch(err => console.error("Failed to load events", err));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Available Events</h1>
      <ul className="space-y-4">
        {events.map(event => (
          <li key={event.id} className="p-4 border rounded bg-white shadow">
            <h2 className="text-lg font-semibold">{event.name}</h2>
            <p>{event.description}</p>
            <p className="text-sm text-gray-600">Max bookings per slot: {event.max_bookings_per_slot}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
