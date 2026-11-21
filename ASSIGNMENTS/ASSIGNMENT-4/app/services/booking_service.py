"""
Booking management, duration policy enforcement, and overlap detection service.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.models.booking import Booking, BookingStatus
from app.models.facility import Facility
from app.models.outbox_event import OutboxEvent, OutboxStatus
from app.models.user import User
from app.schemas.booking import BookingCreate


def check_interval_overlap(
    start1: datetime, end1: datetime, start2: datetime, end2: datetime
) -> bool:
    """
    Half-open interval overlap check: [start1, end1) and [start2, end2).
    Two bookings overlap if and only if start1 < end2 and start2 < end1.
    If start2 == end1 (adjacent bookings), they DO NOT overlap.
    """
    return start1 < end2 and start2 < end1


class BookingService:
    def __init__(self, db: Session):
        self.db = db

    def get_max_duration_minutes(self, facility: Facility) -> int:
        """Lookup campus-specific policy duration limit, defaulting to 180 min."""
        if facility.policy and facility.policy.is_active:
            return facility.policy.max_duration_minutes
        return 180

    def create_booking(self, booking_in: BookingCreate, current_user: User) -> Booking:
        """
        Create a new booking with validation, overlap checks, and transaction safety.
        """
        # Validate facility exists
        facility = self.db.query(Facility).filter(Facility.id == booking_in.facility_id).first()
        if not facility:
            raise ValueError(f"Facility with ID {booking_in.facility_id} does not exist.")

        # Ensure start_time and end_time are UTC
        start = booking_in.start_time
        end = booking_in.end_time
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)

        if end <= start:
            raise ValueError("Booking end time must be strictly after start time.")

        # Duration validation (Faculty reference: 180m accepted, 181m rejected)
        duration_minutes = (end - start).total_seconds() / 60.0
        max_duration = self.get_max_duration_minutes(facility)
        if duration_minutes > max_duration:
            raise ValueError(
                f"Booking duration ({int(duration_minutes)} minutes) exceeds "
                f"maximum allowed limit of {max_duration} minutes."
            )

        # Overlap check within transaction
        # Query active bookings for the same facility
        active_bookings = (
            self.db.query(Booking)
            .filter(
                Booking.facility_id == facility.id,
                Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.PENDING_APPROVAL]),
            )
            .all()
        )

        for existing in active_bookings:
            e_start = existing.start_time
            e_end = existing.end_time
            if e_start.tzinfo is None:
                e_start = e_start.replace(tzinfo=timezone.utc)
            if e_end.tzinfo is None:
                e_end = e_end.replace(tzinfo=timezone.utc)

            if check_interval_overlap(start, end, e_start, e_end):
                raise ValueError(
                    f"Booking overlaps with existing reservation {existing.booking_reference} "
                    f"({e_start.isoformat()} to {e_end.isoformat()}). Adjacent bookings are permitted, but intervals cannot overlap."
                )

        # Determine initial status based on restriction
        initial_status = (
            BookingStatus.PENDING_APPROVAL if facility.is_restricted else BookingStatus.CONFIRMED
        )

        ref_uuid = uuid.uuid4().hex[:8].upper()
        ref = f"BKG-{facility.code}-{ref_uuid}"
        now = datetime.now(timezone.utc)

        booking = Booking(
            booking_reference=ref,
            facility_id=facility.id,
            user_id=current_user.id,
            title=booking_in.title,
            description=booking_in.description,
            start_time=start,
            end_time=end,
            status=initial_status,
            version=1,
            created_at=now,
            updated_at=now,
        )
        self.db.add(booking)
        self.db.flush()

        # Audit log
        audit = AuditLog(
            entity_type="Booking",
            entity_id=booking.id,
            action="CREATE",
            old_state=None,
            new_state=initial_status.value,
            actor_id=current_user.id,
            actor_role=current_user.role.value,
            details=f"Created booking {booking.booking_reference} ({duration_minutes:.0f} mins)",
            version=1,
            timestamp=now,
        )
        self.db.add(audit)

        # Outbox event for external calendar synchronization
        outbox_payload = {
            "booking_reference": booking.booking_reference,
            "facility_code": facility.code,
            "facility_name": facility.name,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "user_email": current_user.email,
            "status": initial_status.value,
        }
        outbox_event = OutboxEvent(
            event_type="CALENDAR_SYNC",
            aggregate_type="Booking",
            aggregate_id=booking.id,
            payload=json.dumps(outbox_payload),
            status=OutboxStatus.PENDING,
            created_at=now,
            updated_at=now,
        )
        self.db.add(outbox_event)

        self.db.commit()
        self.db.refresh(booking)
        return booking

    def get_booking_by_id(self, booking_id: int) -> Optional[Booking]:
        return self.db.query(Booking).filter(Booking.id == booking_id).first()

    def list_bookings(
        self, facility_id: Optional[int] = None, user_id: Optional[int] = None
    ) -> List[Booking]:
        query = self.db.query(Booking)
        if facility_id:
            query = query.filter(Booking.facility_id == facility_id)
        if user_id:
            query = query.filter(Booking.user_id == user_id)
        return query.order_by(Booking.start_time.desc()).all()
