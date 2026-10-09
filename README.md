# 🎟️ SmartEvent – Event Discovery & Ticket Booking System

A full-stack web application for discovering live events, purchasing tickets, and managing digital QR entry passes in real time. 

Built with **FastAPI** for high-performance backend workflows and **React (Vite)** for a responsive, modern frontend interface.

---

## ✨ Features

- **User Authentication**: Secure signup and login using **JWT (JSON Web Tokens)** and **bcrypt** password hashing.
- **Event Discovery**: Search events by title and filter across categories (Tech, Music, Sports, Business).
- **Inventory & Reservation Engine**: Concurrency-safe ticket quantity decrementing, price calculation, and sold-out prevention.
- **Digital QR Passes**: Automatically generates scannable QR verification passes for each booked ticket.
- **Booking Management**: View past orders, ticket details, and download digital passes directly from the dashboard.
- **Notification Center**: Automated booking confirmations and alert badges with read/unread status updates.
- **Multi-role access**: USER, ORGANIZER, and ADMIN permissions enforced by role-bearing JWTs.
- **Organizer tools**: Create and manage owned events, view attendee contact details and booking updates, and track confirmed/cancelled ticket counts and confirmed INR revenue.
- **Admin analytics**: User/event/booking oversight, date-filtered sales trends, and role administration.
- **Event lifecycle**: Upcoming, ongoing, completed, and cancelled states with attendee notifications on updates/cancellations.
- **India-ready listings**: INR pricing, required venue and Indian city fields, and Indian event sample listings.

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** – High-performance asynchronous REST API framework
- **SQLAlchemy** – ORM for database relationships and operations
- **SQLite / PostgreSQL** – Relational database storage
- **Pydantic v2** – Data validation and serialization
- **python-jose & passlib** – JWT generation, token verification, and password encryption
- **qrcode & Pillow** – Dynamic digital QR pass generation

### Frontend
- **React 18 (Vite)** – Fast single-page application bundling and rendering
- **Tailwind CSS** – Utility-first responsive styling
- **Axios** – HTTP client with token request interceptors
- **Lucide React** – Clean iconography

---

## 🗄️ Database Schema

- `users`: User identity credentials and access role (`id`, `username`, `email`, `hashed_password`, `role`, `created_at`)
- `events`: Event catalog, ownership, and lifecycle (`id`, `organizer_id`, `title`, `category`, `venue`, Indian-city `location`, `event_date`, `event_end_date`, `event_status`, INR `ticket_price`, `available_tickets`, `banner_image`)
- `bookings`: Transaction records (`id`, `user_id`, `event_id`, `ticket_quantity`, `total_price`, `booking_status`)
- `tickets`: Unique QR passes tied to bookings (`id`, `booking_id`, `ticket_code`, `qr_code_url`)
- `notifications`: User activity notifications (`id`, `user_id`, `title`, `message`, `type`, `is_read`)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm

---

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Copy `.env.example` to `.env` and set `SECRET_KEY` to a random value with at least 32 characters. Registration supports attendee (USER) and event organizer (ORGANIZER) accounts; ADMIN access is assigned separately. To bootstrap an administrator, register an account with the desired email and set `INITIAL_ADMIN_EMAIL` to that email before starting the backend.
3. Install dependencies and start the API:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
   Existing databases are upgraded on startup with default USER roles and event lifecycle fields.
   Older USD event prices, booking totals, and notification amounts are converted to INR at a fixed migration rate of ₹83 per USD during one-time data migrations.

### Frontend Setup

1. In a separate terminal, navigate to the frontend directory and install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```

Set `INITIAL_ADMIN_EMAIL` in `backend/.env` after registering the administrator account, then restart the backend to grant the initial ADMIN role.
