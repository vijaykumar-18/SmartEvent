import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime, timedelta

from app.database import Base, engine, SessionLocal
from app import models
from app.routers import auth, events, bookings, tickets, notifications
from app.config import ALLOWED_ORIGINS

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartEvent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/qrcodes", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(bookings.router)
app.include_router(tickets.router)
app.include_router(notifications.router)

def create_due_event_reminders():
    now = datetime.utcnow()
    reminder_deadline = now + timedelta(hours=24)
    db = SessionLocal()
    try:
        upcoming_events = (
            db.query(models.Event)
            .filter(models.Event.event_date > now, models.Event.event_date <= reminder_deadline)
            .all()
        )
        for event in upcoming_events:
            bookings = (
                db.query(models.Booking)
                .filter(
                    models.Booking.event_id == event.id,
                    models.Booking.booking_status == models.BookingStatus.CONFIRMED,
                )
                .all()
            )
            reminder_title = f"Reminder: {event.title}"
            reminder_message = f"Your event '{event.title}' (event #{event.id}) starts within 24 hours."
            for booking in bookings:
                reminder_exists = (
                    db.query(models.Notification.id)
                    .filter(
                        models.Notification.user_id == booking.user_id,
                        models.Notification.title == reminder_title,
                        models.Notification.message == reminder_message,
                    )
                    .first()
                )
                if not reminder_exists:
                    db.add(models.Notification(
                        user_id=booking.user_id,
                        title=reminder_title,
                        message=reminder_message,
                        type=models.NotificationType.EVENT,
                    ))
        db.commit()
    finally:
        db.close()

async def event_reminder_loop():
    while True:
        await asyncio.to_thread(create_due_event_reminders)
        await asyncio.sleep(300)

@app.on_event("startup")
async def start_event_reminders():
    app.state.reminder_task = asyncio.create_task(event_reminder_loop())

@app.on_event("shutdown")
async def stop_event_reminders():
    reminder_task = getattr(app.state, "reminder_task", None)
    if reminder_task:
        reminder_task.cancel()
        try:
            await reminder_task
        except asyncio.CancelledError:
            pass

@app.on_event("startup")
def seed_initial_events():
    db = SessionLocal()
    if db.query(models.Event).count() == 0:
        sample_events = [
            models.Event(
                title="Global AI & Cloud Summit 2026",
                description="Experience keynote speeches from leaders in Generative AI, MLOps, and scalable systems.",
                category="Tech",
                location="Silicon Valley Convention Center",
                event_date=datetime.utcnow() + timedelta(days=20),
                ticket_price=149.99,
                total_tickets=250,
                available_tickets=250,
                banner_image="https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200&auto=format&fit=crop&q=80"
            ),
            models.Event(
                title="Neon Horizon Electronic Music Fest",
                description="3 stages, top electro-pop artists, and state-of-the-art spatial audio and laser visual systems.",
                category="Music",
                location="Austin Open Air Arena",
                event_date=datetime.utcnow() + timedelta(days=14),
                ticket_price=79.50,
                total_tickets=500,
                available_tickets=480,
                banner_image="https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=1200&auto=format&fit=crop&q=80"
            ),
              models.Event(
                title="Culinary Arts & Wine Tasting Expo",
                description="Sample gourmet dishes from top chefs and enjoy curated wine pairings.",
                category="Food & Drink",
                location="Downtown Culinary Center",
                event_date=datetime.utcnow() + timedelta(days=28),
                ticket_price=120.00,
                total_tickets=150,
                available_tickets=150,
                banner_image="https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200&auto=format&fit=crop&q=80"
            ),
            models.Event(
                title="SaaS & Startup Founders Forum",
                description="Roundtable discussions, venture capital speed-dating, and networking mixers.",
                category="Business",
                location="Grand Hyatt Conference Hall",
                event_date=datetime.utcnow() + timedelta(days=35),
                ticket_price=220.00,
                total_tickets=80,
                available_tickets=80,
                banner_image="https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=1200&auto=format&fit=crop&q=80"
            )
        ]
        db.add_all(sample_events)
        db.commit()
    db.close()

@app.get("/")
def health_check():
    return {"status": "ok", "app": "SmartEvent API"}