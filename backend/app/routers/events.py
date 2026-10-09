from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.event_lifecycle import sync_event_statuses

router = APIRouter(prefix="/api/events", tags=["Events"])

@router.get("", response_model=List[schemas.EventResponse])
def get_events(
    category: Optional[str] = Query(None, description="Category filter (Music, Tech, Sports, Business, Food & Drink)"),
    search: Optional[str] = Query(None, description="Search term for event title"),
    db: Session = Depends(get_db)
):
    sync_event_statuses(db)
    query = db.query(models.Event)
    if category and category.lower() != "all":
        query = query.filter(models.Event.category.ilike(category.strip()))
    if search:
        query = query.filter(models.Event.title.ilike(f"%{search}%"))
    return query.order_by(models.Event.event_date.asc()).all()

@router.get("/{event_id}", response_model=schemas.EventResponse)
def get_event_detail(event_id: int, db: Session = Depends(get_db)):
    sync_event_statuses(db)
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
