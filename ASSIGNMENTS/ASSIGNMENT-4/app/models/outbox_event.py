"""
Outbox Event model for reliable external service synchronization.
"""

import enum
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Integer, String, Text

from app.database import Base


class OutboxStatus(str, enum.Enum):
    PENDING = "PENDING"
    RETRYING = "RETRYING"
    SENT = "SENT"
    FAILED = "FAILED"


class OutboxEvent(Base):
    __tablename__ = "outbox_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), nullable=False, index=True)  # CALENDAR_SYNC, ISSUE_TRACKER_SYNC
    aggregate_type = Column(String(50), nullable=False)  # Booking, MaintenanceTicket
    aggregate_id = Column(Integer, nullable=False, index=True)
    payload = Column(Text, nullable=False)
    status = Column(Enum(OutboxStatus), default=OutboxStatus.PENDING, nullable=False, index=True)
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    last_attempt_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<OutboxEvent(id={self.id}, type='{self.event_type}', status='{self.status.value}', retries={self.retry_count})>"
