"""
Audit Log model for immutable traceability.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(
        String(50), nullable=False, index=True
    )  # Booking, MaintenanceTicket, SensorEvent
    entity_id = Column(Integer, nullable=False, index=True)
    action = Column(
        String(50), nullable=False
    )  # CREATE, TRANSITION, APPROVE, REJECT, CANCEL, RETRY
    old_state = Column(String(50), nullable=True)
    new_state = Column(String(50), nullable=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    actor_role = Column(String(50), nullable=True)
    details = Column(String(1000), nullable=True)
    version = Column(Integer, nullable=False)
    timestamp = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True
    )

    actor = relationship("User", back_populates="audit_logs", foreign_keys=[actor_id])

    def __repr__(self):
        return f"<AuditLog(entity='{self.entity_type}#{self.entity_id}', action='{self.action}', {self.old_state}->{self.new_state})>"
