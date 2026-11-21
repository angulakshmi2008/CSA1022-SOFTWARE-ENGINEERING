"""
User and Role models for Smart Campus Facility Platform.
"""

import enum
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class UserRole(str, enum.Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    FACILITY_MANAGER = "FACILITY_MANAGER"
    MAINTENANCE_TECHNICIAN = "MAINTENANCE_TECHNICIAN"
    DEPARTMENT_APPROVER = "DEPARTMENT_APPROVER"
    FACULTY_MEMBER = "FACULTY_MEMBER"
    STUDENT = "STUDENT"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False, index=True)
    department = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    bookings = relationship("Booking", back_populates="user", foreign_keys="Booking.user_id")
    assigned_tickets = relationship(
        "MaintenanceTicket",
        back_populates="assigned_technician",
        foreign_keys="MaintenanceTicket.assigned_to_user_id",
    )
    audit_logs = relationship("AuditLog", back_populates="actor", foreign_keys="AuditLog.actor_id")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role.value}')>"
