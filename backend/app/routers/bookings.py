import uuid
import os
import qrcode
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import update
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth
from app.config import BASE_URL

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

QR_FOLDER = os.path.join("static", "qrcodes")
os.makedirs(QR_FOLDER, exist_ok=True)

@router.post("", response_model=schemas.BookingResponse, status_code=status.HTTP_201_CREATED)
def book_tickets(
    payload: schemas.BookingCreate,
    current_user: models.User = Depends(auth.require_roles(models.UserRole.USER)),
    db: Session = Depends(get_db)
):
    if payload.ticket_quantity <= 0:
        raise HTTPException(status_code=400, detail="Ticket quantity must be at least 1")

    event_exists = db.query(models.Event.id).filter(models.Event.id == payload.event_id).first()
    if not event_exists:
        raise HTTPException(status_code=404, detail="Event not found")

    inventory_update = db.execute(
        update(models.Event)
        .where(
            models.Event.id == payload.event_id,
            models.Event.available_tickets >= payload.ticket_quantity,
        )
        .values(available_tickets=models.Event.available_tickets - payload.ticket_quantity)
    )
    if inventory_update.rowcount != 1:
        event = db.query(models.Event).filter(models.Event.id == payload.event_id).first()
        if event.event_status != models.EventStatus.UPCOMING:
            raise HTTPException(status_code=400, detail="Tickets are only available for upcoming events")
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        raise HTTPException(
            status_code=400,
            detail=f"Sold out or insufficient tickets available. Remaining: {event.available_tickets}"
        )

    event = db.query(models.Event).filter(models.Event.id == payload.event_id).first()
    total_price = event.ticket_price * payload.ticket_quantity

    new_booking = models.Booking(
        user_id=current_user.id,
        event_id=event.id,
        ticket_quantity=payload.ticket_quantity,
        total_price=total_price,
        booking_status=models.BookingStatus.CONFIRMED
    )
    db.add(new_booking)
    db.flush()

    # Generate Tickets and QR Codes
    created_tickets = []
    for _ in range(payload.ticket_quantity):
        ticket_code = f"TICK-{uuid.uuid4().hex[:10].upper()}"
        qr_filename = f"{ticket_code}.png"
        qr_file_path = os.path.join(QR_FOLDER, qr_filename)

        # Generate QR code containing verification payload
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        verification_data = f"{BASE_URL.rstrip('/')}/api/tickets/verify/{ticket_code}"
        qr.add_data(verification_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_file_path)

        ticket = models.Ticket(
            booking_id=new_booking.id,
            ticket_code=ticket_code,
            qr_code_url=f"/static/qrcodes/{qr_filename}"
        )
        db.add(ticket)
        created_tickets.append(ticket)

    # Trigger booking confirmation notification
    notification = models.Notification(
        user_id=current_user.id,
        title="Booking Confirmed!",
        message=f"You booked {payload.ticket_quantity} tickets for '{event.title}'. Total: ₹{total_price:,.2f}",
        type=models.NotificationType.BOOKING
    )
    db.add(notification)
    if event.organizer_id is not None:
        db.add(models.Notification(
            user_id=event.organizer_id,
            title="New ticket booking",
            message=(
                f"{current_user.username} booked {payload.ticket_quantity} ticket(s) "
                f"for '{event.title}' (booking #{new_booking.id}). "
                f"Confirmed revenue: ₹{total_price:,.2f}."
            ),
            type=models.NotificationType.BOOKING,
        ))

    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/my-bookings", response_model=List[schemas.BookingResponse])
def get_user_bookings(
    current_user: models.User = Depends(auth.require_roles(models.UserRole.USER)),
    db: Session = Depends(get_db)
):
    return (
        db.query(models.Booking)
        .filter(models.Booking.user_id == current_user.id)
        .order_by(models.Booking.created_at.desc())
        .all()
    )

@router.post("/{booking_id}/cancel", response_model=schemas.BookingResponse)
def cancel_booking(
    booking_id: int,
    current_user: models.User = Depends(auth.require_roles(models.UserRole.USER)),
    db: Session = Depends(get_db)
):
    booking = (
        db.query(models.Booking)
        .filter(
            models.Booking.id == booking_id,
            models.Booking.user_id == current_user.id,
        )
        .first()
    )
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.booking_status != models.BookingStatus.CONFIRMED:
        raise HTTPException(status_code=400, detail="Only confirmed bookings can be cancelled")
    if booking.event.event_date <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Past events cannot be cancelled")

    cancellation = db.execute(
        update(models.Booking)
        .where(
            models.Booking.id == booking.id,
            models.Booking.user_id == current_user.id,
            models.Booking.booking_status == models.BookingStatus.CONFIRMED,
        )
        .values(booking_status=models.BookingStatus.CANCELLED)
    )
    if cancellation.rowcount != 1:
        raise HTTPException(status_code=409, detail="Booking has already been updated")

    db.execute(
        update(models.Event)
        .where(models.Event.id == booking.event_id)
        .values(available_tickets=models.Event.available_tickets + booking.ticket_quantity)
    )
    db.add(models.Notification(
        user_id=current_user.id,
        title="Booking Cancelled",
        message=f"Your booking for '{booking.event.title}' was cancelled.",
        type=models.NotificationType.BOOKING,
    ))
    if booking.event.organizer_id is not None:
        db.add(models.Notification(
            user_id=booking.event.organizer_id,
            title="Booking cancelled",
            message=(
                f"{current_user.username} cancelled booking #{booking.id} for "
                f"'{booking.event.title}' ({booking.ticket_quantity} ticket(s))."
            ),
            type=models.NotificationType.BOOKING,
        ))
    db.commit()
    db.refresh(booking)
    return booking