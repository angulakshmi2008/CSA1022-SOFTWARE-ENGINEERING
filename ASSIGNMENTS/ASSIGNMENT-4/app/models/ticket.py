"""
Maintenance Ticket model and lifecycle definitions.
"""

import enum
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class TicketState(str, enum.Enum):
    NEW = "New"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


class ImpactLevel(str, enum.Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class UrgencyLevel(str, enum.Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class PriorityLevel(str, enum.Enum):
    M1 = "M1"
    M2 = "M2"
    M3 = "M3"
    M4 = "M4"
    MANUAL_REVIEW = "Manual Review"


class MaintenanceTicket(Base):
    __tablename__ = "maintenance_tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(50), unique=True, index=True, nullable=False)
    facility_id = Column(Integer, ForeignKey("facilities.id"), nullable=False, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(1000), nullable=False)
    category = Column(
        String(50), default="Facilities", nullable=False
    )  # Facilities, HVAC, AV-Network, Manual Review
    impact = Column(String(20), nullable=False)  # High, Medium, Low
    urgency = Column(String(20), nullable=False)  # High, Medium, Low
    priority = Column(String(20), nullable=False)  # M1, M2, M3, M4, Manual Review
    state = Column(Enum(TicketState), default=TicketState.NEW, nullable=False, index=True)
    assigned_to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    sensor_event_id = Column(
        Integer, nullable=True
    )  # Back-ref to sensor event if triggered by telemetry
    sla_deadline = Column(DateTime, nullable=False)
    resolution_notes = Column(String(1000), nullable=True)
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    facility = relationship("Facility", back_populates="tickets")
    assigned_technician = relationship(
        "User", foreign_keys=[assigned_to_user_id], back_populates="assigned_tickets"
    )
    creator = relationship("User", foreign_keys=[created_by_user_id])
    sensor_events = relationship(
        "SensorEvent", back_populates="ticket", foreign_keys="SensorEvent.maintenance_ticket_id"
    )

    def __repr__(self):
        return f"<MaintenanceTicket(number='{self.ticket_number}', state='{self.state.value}', priority='{self.priority}', v={self.version})>"
