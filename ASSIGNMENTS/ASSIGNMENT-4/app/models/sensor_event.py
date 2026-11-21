"""
Sensor event model for environmental and equipment telemetry.
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class SensorEvent(Base):
    __tablename__ = "sensor_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String(100), unique=True, index=True, nullable=False)
    sensor_id = Column(String(50), nullable=False, index=True)
    sensor_type = Column(
        String(30), nullable=False
    )  # temperature, humidity, water_leak, power, co2
    facility_id = Column(Integer, ForeignKey("facilities.id"), nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(20), default="celsius", nullable=False)
    threshold = Column(Float, default=28.0, nullable=False)
    is_breached = Column(Boolean, default=False, nullable=False)
    processed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    maintenance_ticket_id = Column(Integer, ForeignKey("maintenance_tickets.id"), nullable=True)

    facility = relationship("Facility", back_populates="sensor_events")
    ticket = relationship(
        "MaintenanceTicket", back_populates="sensor_events", foreign_keys=[maintenance_ticket_id]
    )

    def __repr__(self):
        return f"<SensorEvent(event_id='{self.event_id}', sensor='{self.sensor_id}', value={self.value}, breached={self.is_breached})>"
