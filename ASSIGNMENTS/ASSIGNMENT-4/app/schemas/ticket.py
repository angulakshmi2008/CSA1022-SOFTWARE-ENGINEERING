"""
Pydantic schemas for Maintenance Tickets and Transitions.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.ticket import TicketState


class TicketCreate(BaseModel):
    facility_id: int
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=5, max_length=1000)
    impact: str = Field(description="High, Medium, or Low")
    urgency: str = Field(description="High, Medium, or Low")
    category: Optional[str] = None  # If omitted, auto-classified


class TicketTransitionRequest(BaseModel):
    target_state: TicketState
    expected_version: int = Field(ge=1)
    resolution_notes: Optional[str] = Field(default=None, max_length=1000)
    assigned_to_user_id: Optional[int] = None


class TicketResponse(BaseModel):
    id: int
    ticket_number: str
    facility_id: int
    title: str
    description: str
    category: str
    impact: str
    urgency: str
    priority: str
    state: TicketState
    assigned_to_user_id: Optional[int]
    created_by_user_id: Optional[int]
    sensor_event_id: Optional[int]
    sla_deadline: datetime
    resolution_notes: Optional[str]
    version: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
