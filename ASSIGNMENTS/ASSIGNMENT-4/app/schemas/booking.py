"""
Pydantic schemas for Bookings and Approvals.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.booking import BookingStatus


class BookingCreate(BaseModel):
    facility_id: int
    title: str = Field(min_length=3, max_length=150)
    description: Optional[str] = Field(default=None, max_length=500)
    start_time: datetime
    end_time: datetime


class BookingApprovalRequest(BaseModel):
    approved: bool
    notes: Optional[str] = Field(default=None, max_length=500)


class BookingResponse(BaseModel):
    id: int
    booking_reference: str
    facility_id: int
    user_id: int
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    status: BookingStatus
    approved_by_user_id: Optional[int]
    approval_notes: Optional[str]
    approved_at: Optional[datetime]
    version: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
