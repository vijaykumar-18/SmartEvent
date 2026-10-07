from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, EmailStr, Field
from app.models import BookingStatus, NotificationType

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    user_id: Optional[int] = None

class EventBase(BaseModel):
    title: str
    description: str
    category: Literal["Music", "Tech", "Sports", "Business"]
    location: str
    event_date: datetime
    ticket_price: float = Field(ge=0)
    total_tickets: int = Field(gt=0)
    banner_image: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    available_tickets: int
    created_at: datetime
    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    event_id: int
    ticket_quantity: int = Field(gt=0, le=10)

class TicketResponse(BaseModel):
    id: int
    booking_id: int
    ticket_code: str
    qr_code_url: str
    created_at: datetime
    event: Optional[EventResponse] = None
    class Config:
        from_attributes = True

class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    ticket_quantity: int
    total_price: float
    booking_status: BookingStatus
    created_at: datetime
    event: EventResponse
    tickets: List[TicketResponse] = Field(default_factory=list)
    class Config:
        from_attributes = True

class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    type: NotificationType
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True