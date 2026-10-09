from datetime import datetime, timezone
from typing import Optional, List, Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator
from app.models import BookingStatus, EventStatus, NotificationType, UserRole

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)
    role: Literal["USER", "ORGANIZER"] = "USER"

class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[UserRole] = None

class EventBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1)
    category: Literal["Music", "Tech", "Sports", "Business", "Food & Drink"]
    location: Literal[
        "Mumbai", "Chennai", "Hyderabad", "Pune", "Goa", "Kolkata",
        "Delhi", "Ahmedabad", "Bengaluru", "Gurugram", "Jaipur", "Kochi",
    ]
    venue: str = Field(min_length=1, max_length=150)
    event_date: datetime
    event_end_date: Optional[datetime] = None
    ticket_price: float = Field(ge=0)
    total_tickets: int = Field(gt=0)
    banner_image: Optional[str] = Field(default=None, max_length=2048)

    @field_validator("event_date", "event_end_date")
    @classmethod
    def normalize_datetime(cls, value):
        if value is not None and value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    @field_validator("location", "venue")
    @classmethod
    def require_event_place(cls, value):
        if not value:
            raise ValueError("City and venue are required")
        return value

    @model_validator(mode="after")
    def validate_dates(self):
        start = self.event_date
        end = self.event_end_date
        if end is not None and start is not None and end <= start:
            raise ValueError("Event end date must be after the start date")
        return self

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: Optional[str] = Field(default=None, min_length=1, max_length=150)
    description: Optional[str] = Field(default=None, min_length=1)
    category: Optional[Literal["Music", "Tech", "Sports", "Business", "Food & Drink"]] = None
    location: Optional[Literal[
        "Mumbai", "Chennai", "Hyderabad", "Pune", "Goa", "Kolkata",
        "Delhi", "Ahmedabad", "Bengaluru", "Gurugram", "Jaipur", "Kochi",
    ]] = None
    venue: Optional[str] = Field(default=None, min_length=1, max_length=150)
    event_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    ticket_price: Optional[float] = Field(default=None, ge=0)
    total_tickets: Optional[int] = Field(default=None, gt=0)
    banner_image: Optional[str] = Field(default=None, max_length=2048)

    @field_validator("event_date", "event_end_date")
    @classmethod
    def normalize_datetime(cls, value):
        if value is not None and value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    @field_validator("location", "venue", mode="before")
    @classmethod
    def require_event_place(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError("City and venue cannot be empty")
        return value

class EventResponse(EventBase):
    id: int
    available_tickets: int
    organizer_id: Optional[int] = None
    event_status: EventStatus
    created_at: datetime
    class Config:
        from_attributes = True

class UserRoleUpdate(BaseModel):
    role: UserRole

class EventAnalytics(BaseModel):
    event_id: int
    event_title: str
    total_tickets: int
    tickets_sold: int
    remaining_tickets: int
    revenue: float
    booking_count: int
    tickets_booked: int
    confirmed_bookings: int
    cancelled_bookings: int
    pending_bookings: int
    confirmed_tickets: int
    cancelled_tickets: int
    pending_tickets: int

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

class OrganizerBookingResponse(BookingResponse):
    user: UserResponse

class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    type: NotificationType
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True

class AdminBookingResponse(BookingResponse):
    user: UserResponse

    class Config:
        from_attributes = True