import { useState } from "react";
import { api } from "../services/api";

export default function CreateEventPage() {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [maxBookings, setMaxBookings] = useState(1);
  const [slots, setSlots] = useState<string[]>([""]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const slotDatetimes = slots.map((s) => new Date(s).toISOString());
      await api.post("/events", {
        name,
        description,
        max_bookings_per_slot: maxBookings,
        slots: slotDatetimes,
      });
      alert("Event created!");
    } catch (err) {
      console.error("Failed to create event", err);
      alert("Error creating event");
    }
  };

  const handleSlotChange = (index: number, value: string) => {
    const updated = [...slots];
    updated[index] = value;
    setSlots(updated);
  };

  const addSlot = () => setSlots([...slots, ""]);
  const removeSlot = (index: number) =>
    setSlots(slots.filter((_, i) => i !== index));

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Create Event</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          className="border p-2 w-full"
          placeholder="Event Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <textarea
          className="border p-2 w-full"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />
        <input
          type="number"
          min={1}
          className="border p-2 w-full"
          placeholder="Max bookings per slot"
          value={maxBookings}
          onChange={(e) => setMaxBookings(parseInt(e.target.value))}
          required
        />
        <div>
          <label className="font-semibold">Slot Times (ISO format):</label>
          {slots.map((slot, idx) => (
            <div key={idx} className="flex items-center gap-2 mt-2">
              <input
                type="datetime-local"
                value={slot}
                onChange={(e) => handleSlotChange(idx, e.target.value)}
                className="border p-2 flex-1"
                required
              />
              <button
                type="button"
                onClick={() => removeSlot(idx)}
                className="text-red-500"
              >
                ✕
              </button>
            </div>
          ))}
          <button
            type="button"
            onClick={addSlot}
            className="mt-2 text-blue-500 underline"
          >
            + Add Slot
          </button>
        </div>
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Create Event
        </button>
      </form>
    </div>
  );
}
