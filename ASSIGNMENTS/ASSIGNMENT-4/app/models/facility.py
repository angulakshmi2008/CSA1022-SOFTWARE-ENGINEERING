"""
Facility and Facility Policy models.
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class FacilityPolicy(Base):
    __tablename__ = "facility_policies"

    id = Column(Integer, primary_key=True, index=True)
    campus = Column(String(50), nullable=False, index=True)  # e.g., "Main Campus", "North Campus"
    facility_type = Column(String(50), nullable=True)  # e.g., "Lab", "Classroom", "Auditorium"
    max_duration_minutes = Column(Integer, default=180, nullable=False)
    temp_threshold = Column(Float, default=28.0, nullable=False)
    requires_approval_for_restricted = Column(Boolean, default=True, nullable=False)
    policy_version = Column(Integer, default=1, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    facilities = relationship("Facility", back_populates="policy")

    def __repr__(self):
        return f"<FacilityPolicy(campus='{self.campus}', max_duration={self.max_duration_minutes}m, threshold={self.temp_threshold}C, v={self.policy_version})>"


class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    campus = Column(String(50), default="Main Campus", nullable=False, index=True)
    building = Column(String(50), nullable=False)
    room_number = Column(String(20), nullable=False)
    facility_type = Column(String(50), default="General", nullable=False)
    capacity = Column(Integer, default=30, nullable=False)
    is_restricted = Column(Boolean, default=False, nullable=False)
    policy_id = Column(Integer, ForeignKey("facility_policies.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    policy = relationship("FacilityPolicy", back_populates="facilities")
    bookings = relationship("Booking", back_populates="facility")
    sensor_events = relationship("SensorEvent", back_populates="facility")
    tickets = relationship("MaintenanceTicket", back_populates="facility")

    def __repr__(self):
        return f"<Facility(code='{self.code}', name='{self.name}', campus='{self.campus}', restricted={self.is_restricted})>"
