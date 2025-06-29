## BookMySlot

## vercel (Frontend)
Link: https://book-slots.vercel.app

## Render (Backend)
Link: https://book-slots.onrender.com

## Admin Login
Admin Login credentials 
email: wahegurusingh2002@gmail.com
password: 12345

## ✨ Key Features

### 🎟 Event Management
- **Admin-only** event creation and management
- Create and manage events with custom time slots (admin)
- Set maximum bookings per time slot (admin)
- View and manage all events in one place

### 📅 Booking System
- Users can book available time slots
- Real-time availability updates
- Prevent double bookings and overbooking
- Email confirmation for all bookings


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
## 🎥 Demo Video
[Watch the demo](https://github.com/wahe7/book_slots/blob/main/demo.mp4)

