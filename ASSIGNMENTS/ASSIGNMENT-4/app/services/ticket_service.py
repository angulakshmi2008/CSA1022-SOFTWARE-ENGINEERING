"""
Maintenance ticket lifecycle, optimistic locking, and transition enforcement.
"""

import json
from datetime import datetime, timezone
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.models.facility import Facility
from app.models.outbox_event import OutboxEvent, OutboxStatus
from app.models.ticket import MaintenanceTicket, TicketState
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketTransitionRequest
from app.security.authorization import can_mutate_ticket
from app.services.priority_service import calculate_priority, classify_category
from app.services.sla_service import calculate_sla_deadline

# Explicit allowed state transition map
ALLOWED_TRANSITIONS: Dict[TicketState, List[TicketState]] = {
    TicketState.NEW: [TicketState.ASSIGNED],
    TicketState.ASSIGNED: [TicketState.IN_PROGRESS],
    TicketState.IN_PROGRESS: [TicketState.RESOLVED],
    TicketState.RESOLVED: [TicketState.CLOSED],
    TicketState.CLOSED: [],  # Terminal state
}


class TicketService:
    def __init__(self, db: Session):
        self.db = db

    def create_ticket(
        self, ticket_in: TicketCreate, creator: Optional[User] = None
    ) -> MaintenanceTicket:
        """Create new maintenance ticket with SLA calculation and category triage."""
        facility = self.db.query(Facility).filter(Facility.id == ticket_in.facility_id).first()
        if not facility:
            raise ValueError(f"Facility with ID {ticket_in.facility_id} does not exist.")

        # Priority calculation
        priority = calculate_priority(ticket_in.impact, ticket_in.urgency)

        # Category determination (auto-classify if not supplied)
        category = ticket_in.category or classify_category(
            f"{ticket_in.title} {ticket_in.description}"
        )

        now = datetime.now(timezone.utc)
        deadline = calculate_sla_deadline(priority, now)

        count = self.db.query(MaintenanceTicket).count() + 1
        ticket_number = f"TKT-{now.strftime('%Y%m%d')}-{count:04d}"

        ticket = MaintenanceTicket(
            ticket_number=ticket_number,
            facility_id=facility.id,
            title=ticket_in.title,
            description=ticket_in.description,
            category=category,
            impact=ticket_in.impact,
            urgency=ticket_in.urgency,
            priority=priority,
            state=TicketState.NEW,
            created_by_user_id=creator.id if creator else None,
            sla_deadline=deadline,
            version=1,
            created_at=now,
            updated_at=now,
        )
        self.db.add(ticket)
        self.db.flush()

        audit = AuditLog(
            entity_type="MaintenanceTicket",
            entity_id=ticket.id,
            action="CREATE",
            old_state=None,
            new_state=TicketState.NEW.value,
            actor_id=creator.id if creator else None,
            actor_role=creator.role.value if creator else "SYSTEM",
            details=f"Ticket created: {ticket.title} (Priority: {priority}, Category: {category})",
            version=1,
            timestamp=now,
        )
        self.db.add(audit)

        # Issue tracker sync outbox event
        outbox_payload = {
            "ticket_number": ticket.ticket_number,
            "facility_code": facility.code,
            "summary": ticket.title,
            "priority": priority,
            "category": category,
            "sla_deadline": deadline.isoformat(),
            "state": TicketState.NEW.value,
        }
        outbox_event = OutboxEvent(
            event_type="ISSUE_TRACKER_SYNC",
            aggregate_type="MaintenanceTicket",
            aggregate_id=ticket.id,
            payload=json.dumps(outbox_payload),
            status=OutboxStatus.PENDING,
            created_at=now,
            updated_at=now,
        )
        self.db.add(outbox_event)

        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def transition_ticket(
        self, ticket_id: int, req: TicketTransitionRequest, actor: User
    ) -> MaintenanceTicket:
        """
        Transition ticket to target state under optimistic concurrency control.
        Enforces:
        1. Role authorization (Student cannot mutate ticket states).
        2. Optimistic locking: expected_version == ticket.version.
        3. Valid lifecycle transition: New -> Assigned -> In Progress -> Resolved -> Closed.
        4. Resolution notes required when moving to Resolved.
        """
        if not can_mutate_ticket(actor):
            raise PermissionError(
                f"User '{actor.username}' with role '{actor.role.value}' cannot mutate tickets."
            )

        ticket = self.db.query(MaintenanceTicket).filter(MaintenanceTicket.id == ticket_id).first()
        if not ticket:
            raise ValueError(f"Maintenance ticket with ID {ticket_id} not found.")

        # 1. Optimistic Locking check
        if req.expected_version != ticket.version:
            raise ValueError(
                f"Optimistic lock conflict: Stale expected ticket version {req.expected_version}. "
                f"Current ticket version is {ticket.version}. Refresh and retry."
            )

        # 2. Lifecycle validation
        current_state = ticket.state
        allowed_next = ALLOWED_TRANSITIONS.get(current_state, [])
        if req.target_state not in allowed_next:
            allowed_names = [s.value for s in allowed_next]
            raise ValueError(
                f"Invalid state transition: Cannot move ticket from '{current_state.value}' to '{req.target_state.value}'. "
                f"Allowed target states: {allowed_names}."
            )

        # 3. Resolution notes requirement
        if req.target_state == TicketState.RESOLVED:
            if not req.resolution_notes or not req.resolution_notes.strip():
                raise ValueError(
                    "Resolution notes are mandatory when moving a ticket into Resolved."
                )

        now = datetime.now(timezone.utc)
        old_state_str = current_state.value

        ticket.state = req.target_state
        ticket.version += 1
        ticket.updated_at = now

        if req.resolution_notes:
            ticket.resolution_notes = req.resolution_notes.strip()

        if req.assigned_to_user_id:
            ticket.assigned_to_user_id = req.assigned_to_user_id

        audit = AuditLog(
            entity_type="MaintenanceTicket",
            entity_id=ticket.id,
            action="TRANSITION",
            old_state=old_state_str,
            new_state=req.target_state.value,
            actor_id=actor.id,
            actor_role=actor.role.value,
            details=f"State transitioned to {req.target_state.value} by {actor.username}. Notes: {req.resolution_notes or 'None'}",
            version=ticket.version,
            timestamp=now,
        )
        self.db.add(audit)

        # If resolved or closed, notify issue tracker
        if req.target_state in [TicketState.RESOLVED, TicketState.CLOSED]:
            outbox_payload = {
                "ticket_number": ticket.ticket_number,
                "state": req.target_state.value,
                "resolution_notes": ticket.resolution_notes,
                "actor": actor.username,
                "version": ticket.version,
            }
            outbox_event = OutboxEvent(
                event_type="ISSUE_TRACKER_SYNC",
                aggregate_type="MaintenanceTicket",
                aggregate_id=ticket.id,
                payload=json.dumps(outbox_payload),
                status=OutboxStatus.PENDING,
                created_at=now,
                updated_at=now,
            )
            self.db.add(outbox_event)

        self.db.commit()
        self.db.refresh(ticket)
        return ticket
