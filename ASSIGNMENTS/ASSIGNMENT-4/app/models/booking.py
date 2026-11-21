"""
Booking model and booking status definitions.
"""

import enum
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class BookingStatus(str, enum.Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_reference = Column(String(50), unique=True, index=True, nullable=False)
    facility_id = Column(Integer, ForeignKey("facilities.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    status = Column(
        Enum(BookingStatus), default=BookingStatus.CONFIRMED, nullable=False, index=True
    )
    approved_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    approval_notes = Column(String(500), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    facility = relationship("Facility", back_populates="bookings")
    user = relationship("User", back_populates="bookings", foreign_keys=[user_id])
    approver = relationship("User", foreign_keys=[approved_by_user_id])

    def __repr__(self):
        return f"<Booking(ref='{self.booking_reference}', facility_id={self.facility_id}, status='{self.status.value}', v={self.version})>"
