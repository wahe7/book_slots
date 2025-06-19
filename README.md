# BookMySlot – Fullstack Hiring Challenge for New Grads

Welcome to the WizCommerce Fullstack Hiring Challenge! This challenge is designed to assess your frontend and backend skills in building a simple, real-world application. Good luck, and have fun!

> 🧠 **Note:** This challenge is ideal for SD1 candidates applying for either frontend or backend roles — but the best candidates will attempt both parts. We'll evaluate you on your strengths, but fullstack attempts are highly appreciated.

---

## 🔄 Project Overview

Build a simple scheduling application where users can create events and let others book available time slots. Think of it as a mini-Calendly.

---

## 🚀 Core Features

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

## 📚 Tech Stack (Suggestions)

* **Frontend**: React (Vite) + TailwindCSS
* **Backend**: FastAPI / Flask / Express.js
* **Database**: SQLite or PostgreSQL
* **Deployment**: Vercel (frontend) + Render / Railway (backend)

---

## 🚗 Deployment Instructions

### 🌐 Example Hosting Platforms

Here are some services you can use to deploy your frontend and backend:

#### Frontend (Static Hosting)

* [Vercel](https://vercel.com/) – Fast CI/CD with GitHub integration
* [Netlify](https://www.netlify.com/) – Great for React/Vite apps
* [Cloudflare Pages](https://pages.cloudflare.com/) – Free and fast
* [GitHub Pages](https://pages.github.com/) – Works for static SPAs

#### Backend (API + Database Hosting)

* [Render](https://render.com/) – Easy FastAPI or Node.js hosting
* [Railway](https://railway.app/) – Great for fullstack apps with PostgreSQL
* [Fly.io](https://fly.io/) – Edge deployment with Docker support
* [Replit](https://replit.com/) – Quick backend demos
* [Supabase](https://supabase.com/) – For database + lightweight backend APIs

### 📤 Submission Form

To officially submit your solution, please fill out this short [Google Form](https://forms.gle/bY9UeufzBpUhiyU5A) with the following details:

* Your Full Name
* Email Address
* GitHub repository link (private repo with access granted)
* Frontend deployment URL (e.g., Vercel)
* Backend deployment URL (e.g., Render)
* Any notes or context you want us to know

This helps us track all submissions in one place and ensures nothing gets missed.

1. Fork this repo
2. Build the frontend and backend
3. Deploy (if possible) and include URLs in your README
4. Submit GitHub link with live demo or local instructions

---

## ✨ Bonus Features (Optional)

* Email confirmation on booking
* Realtime booking updates
* Event branding with image upload
* Google Calendar sync (mocked is fine)

---

## 🔍 Evaluation Rubric

| Area             | What We're Looking For                        |
| ---------------- | --------------------------------------------- |
| ✅ Functionality  | All core features implemented, no major bugs  |
| 📚 Code Quality  | Clear structure, modular design, comments     |
| 🎨 UI/UX         | Responsive design, form feedback, good layout |
| ⚙️ API Design    | RESTful, validation, edge-case handling       |
| 🚁 Deployment    | Working links, good README, .env support      |
| 📣 Communication | Commit hygiene, comments, README clarity      |

---

## 📄 Submission Checklist

* [x] Working backend with all relevant routes and validations
* [x] Functional frontend with event listing, detail view, and booking
* [x] Clear GitHub repository with meaningful commit history
* [x] Frontend deployment URL (e.g., Vercel, Netlify)
* [x] Backend deployment URL (e.g., Render, Railway)
* [x] Local setup instructions (with `.env.example`)
* [x] Well-written README explaining tech choices, folder structure, and approach
* [x] Bonus features (if implemented) clearly listed in README
* [x] Short write-up on assumptions made and areas for improvement

> 🔒 **Plagiarism Notice:** We manually review all submissions. Identical or copy-pasted codebases will be **disqualified**. Please do original work — this helps you grow and us evaluate fairly.

---

## 👊 Good Luck!

We’re excited to see your submission. Think creatively, structure your code well, and showcase your ability to work across the stack. Happy coding!
