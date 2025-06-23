## BookMySlot

### 🛠 Tech Stack

### Backend
- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (database migrations)
- Pydantic (data validation)

### Frontend
- React with TypeScript
- Tailwind CSS
- Axios for API calls
- React Router for navigation

### 🚀 Core Features

### ✏️ 1. Create Event (Private User)

* Input: Event title, description
* List of available time slots (ISO 8601 format: `2025-06-20T10:00`)
* Max bookings per slot

### 📋 2. Public Event Listing

* List of all created events with titles and basic info
* Click to see event details + available time slots

### ⏰ 3. Booking Interface

* Visitors can enter name + email to book a slot
* Slot becomes unavailable after booking
* Prevent double booking for same user + slot

### 🌍 4. Time Zone Support

* Users should be able to view and book slots in **their local time zone**
* Time slots should auto-convert to user's browser or selected time zone
* Store data in UTC and convert client-side using libraries like `date-fns-tz` or `luxon`

### 📅 5. View My Bookings (optional)

* User can see all their past bookings (filter by email)

---

## 🖥 Suggested Frontend Screens

### 1. **Home Page (Event Listing)**

* Displays all upcoming public events
* Basic event metadata: name, creator, number of slots

### 2. **Event Details Page**

* Shows:

  * Event name and description
  * Available slots in user’s local time
  * Booking form with name + email input

### 3. **Create Event Page**

* Form to input event name, description, and slots (date + time)
* Time zone awareness on the input

### 4. **My Bookings Page (Optional)**

* Displays list of bookings by current user (using email as identifier)

### 5. **Success/Feedback Screens**

* Post-booking confirmation
* Error/failure states (e.g. already booked, slot full)

---

## 📊 API Specification (Suggested)

| Method | Endpoint                 | Description              |
| ------ | ------------------------ | ------------------------ |
| POST   | `/events`                | Create an event          |
| GET    | `/events`                | List all events          |
| GET    | `/events/:id`            | Get event + slots        |
| POST   | `/events/:id/bookings`   | Book a slot              |
| GET    | `/users/:email/bookings` | View bookings (optional) |

---

* Email confirmation on booking
* Realtime booking updates
* Event branding with image upload
* Google Calendar sync (mocked is fine)

---

## 🔍 Evaluation Rubric

## 🚀 API Endpoints

### Admin
- `POST /api/admin/login` - Admin login
- `GET /api/admin/events` - List all events (admin)
- `POST /api/admin/events` - Create new event (admin)

### Events
- `GET /api/events` - List all public events
- `GET /api/events/{event_id}` - Get event details
- `GET /api/events/{event_id}/slots` - Get available slots for event

### Bookings
- `POST /api/bookings` - Create new booking
- `GET /api/bookings?email=user@example.com` - Get user's bookings

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL
- pipenv (for Python dependencies)
- npm or yarn (for frontend dependencies)

### Backend Setup
```bash
# Install dependencies
cd backend
pipenv install

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🚀 Deployment

### Backend
Deploy to your preferred cloud provider (Render) with PostgreSQL add-on.

### Frontend
Build and deploy the React app to Vercel


---

## 🚀 Project Status
✅ Core features implemented  
🔧 Under active development  
🚀 Ready for production deployment

---
## Demo Video

## 🎥 Demo Video
<video src="https://github.com/wahe7/book_slots/blob/main/demo.mp4" controls width="100%"></video>

