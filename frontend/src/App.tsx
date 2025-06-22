import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import CreateEventPage from "./pages/CreateEventPage";
import EventDetailsPage from "./pages/EventDetailsPage";
import UserBookingsPage from "./pages/UserBookings";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/create-event" element={<CreateEventPage />} />
        <Route path="/events/:id" element={<EventDetailsPage />} />
        <Route path="/user-bookings" element={<UserBookingsPage />} />
      </Routes>
    </Router>
  );
}