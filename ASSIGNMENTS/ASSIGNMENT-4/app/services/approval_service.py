"""
Approval workflow service for restricted facilities and elevated actions.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.models.booking import Booking, BookingStatus
from app.models.user import User
from app.security.authorization import can_approve_booking


class ApprovalService:
    def __init__(self, db: Session):
        self.db = db

    def process_booking_approval(
        self, booking_id: int, approved: bool, notes: str, actor: User
    ) -> Booking:
        """
        Process approval or rejection for a restricted facility booking.
        Enforces strict role authorization:
        - Students cannot approve bookings.
        - Unauthorized requests leave persistent state unchanged.
        """
        if not can_approve_booking(actor):
            raise PermissionError(
                f"User '{actor.username}' with role '{actor.role.value}' is not authorized to approve bookings."
            )

        booking = self.db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise ValueError(f"Booking with ID {booking_id} not found.")

        if booking.status != BookingStatus.PENDING_APPROVAL:
            raise ValueError(
                f"Booking {booking.booking_reference} is in state '{booking.status.value}', not 'PENDING_APPROVAL'."
            )

        old_state = booking.status.value
        new_status = BookingStatus.CONFIRMED if approved else BookingStatus.REJECTED
        now = datetime.now(timezone.utc)

        booking.status = new_status
        booking.approved_by_user_id = actor.id
        booking.approval_notes = notes
        booking.approved_at = now
        booking.version += 1
        booking.updated_at = now

        audit = AuditLog(
            entity_type="Booking",
            entity_id=booking.id,
            action="APPROVE" if approved else "REJECT",
            old_state=old_state,
            new_state=new_status.value,
            actor_id=actor.id,
            actor_role=actor.role.value,
            details=f"Booking {'approved' if approved else 'rejected'} by {actor.username}: {notes}",
            version=booking.version,
            timestamp=now,
        )
        self.db.add(audit)
        self.db.commit()
        self.db.refresh(booking)
        return booking
