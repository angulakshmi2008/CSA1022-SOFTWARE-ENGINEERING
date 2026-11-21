"""
Integration tests for Maintenance Ticket lifecycle, optimistic locking, and audit persistence.
Matches Assignment 4 faculty specifications: I1, R3, R4.
"""

import pytest

from app.models.audit import AuditLog
from app.models.ticket import TicketState
from app.schemas.ticket import TicketCreate, TicketTransitionRequest
from app.services.ticket_service import TicketService


# ============================================================================
# I1: Valid ticket commands plus persistence and audit -> Correct Closed State
# ============================================================================
def test_i1_valid_ticket_lifecycle_persistence_and_audit(
    db_session, seeded_users, seeded_facilities
):
    """
    I1: Execute complete valid ticket lifecycle:
    New -> Assigned -> In Progress -> Resolved -> Closed
    Asserts:
    1. Reaches final Closed state.
    2. Version increments correctly from 1 to 5.
    3. Exactly 5 immutable audit log records are created.
    """
    service = TicketService(db_session)
    admin = seeded_users["admin"]
    tech = seeded_users["tech_dave"]
    facility = seeded_facilities["general"]

    # Step 1: Create Ticket (State: New, Version: 1)
    ticket_in = TicketCreate(
        facility_id=facility.id,
        title="Lab 101 AC Leaking Water",
        description="Air conditioning unit is leaking water onto floor",
        impact="High",
        urgency="High",
    )
    ticket = service.create_ticket(ticket_in, creator=admin)
    assert ticket.state == TicketState.NEW
    assert ticket.version == 1
    assert ticket.priority == "M1"
    ticket_id = ticket.id

    # Step 2: Transition New -> Assigned (Version: 2)
    req_assign = TicketTransitionRequest(
        target_state=TicketState.ASSIGNED, expected_version=1, assigned_to_user_id=tech.id
    )
    ticket = service.transition_ticket(ticket_id, req_assign, actor=admin)
    assert ticket.state == TicketState.ASSIGNED
    assert ticket.version == 2
    assert ticket.assigned_to_user_id == tech.id

    # Step 3: Transition Assigned -> In Progress (Version: 3)
    req_progress = TicketTransitionRequest(target_state=TicketState.IN_PROGRESS, expected_version=2)
    ticket = service.transition_ticket(ticket_id, req_progress, actor=tech)
    assert ticket.state == TicketState.IN_PROGRESS
    assert ticket.version == 3

    # Step 4: Transition In Progress -> Resolved with mandatory notes (Version: 4)
    req_resolve = TicketTransitionRequest(
        target_state=TicketState.RESOLVED,
        expected_version=3,
        resolution_notes="Cleaned evaporator condensate drain pipe and replaced seal gasket.",
    )
    ticket = service.transition_ticket(ticket_id, req_resolve, actor=tech)
    assert ticket.state == TicketState.RESOLVED
    assert ticket.version == 4
    assert ticket.resolution_notes is not None

    # Step 5: Transition Resolved -> Closed (Version: 5)
    req_close = TicketTransitionRequest(target_state=TicketState.CLOSED, expected_version=4)
    ticket = service.transition_ticket(ticket_id, req_close, actor=admin)
    assert ticket.state == TicketState.CLOSED
    assert ticket.version == 5

    # Verify Audit Trail persistence
    audit_records = (
        db_session.query(AuditLog)
        .filter(AuditLog.entity_type == "MaintenanceTicket", AuditLog.entity_id == ticket_id)
        .order_by(AuditLog.version.asc())
        .all()
    )

    assert len(audit_records) == 5, f"Expected 5 audit records, found {len(audit_records)}"
    states = [a.new_state for a in audit_records]
    assert states == [
        TicketState.NEW.value,
        TicketState.ASSIGNED.value,
        TicketState.IN_PROGRESS.value,
        TicketState.RESOLVED.value,
        TicketState.CLOSED.value,
    ]


# ============================================================================
# R3: Resolve without notes -> Rejection; In Progress retained (Regression)
# ============================================================================
def test_r3_resolve_without_notes_rejected(db_session, seeded_users, seeded_facilities):
    """
    R3: Attempting to resolve a ticket without resolution notes must be rejected,
    and state must remain 'In Progress' with unchanged version.
    """
    service = TicketService(db_session)
    admin = seeded_users["admin"]
    tech = seeded_users["tech_dave"]
    facility = seeded_facilities["general"]

    ticket = service.create_ticket(
        TicketCreate(
            facility_id=facility.id,
            title="Broken Projector HDMI",
            description="HDMI cable port broken",
            impact="Medium",
            urgency="Medium",
        ),
        creator=admin,
    )
    # Move to Assigned then In Progress
    service.transition_ticket(
        ticket.id,
        TicketTransitionRequest(target_state=TicketState.ASSIGNED, expected_version=1),
        actor=admin,
    )
    service.transition_ticket(
        ticket.id,
        TicketTransitionRequest(target_state=TicketState.IN_PROGRESS, expected_version=2),
        actor=tech,
    )

    # Attempt to resolve with empty notes
    req_empty_notes = TicketTransitionRequest(
        target_state=TicketState.RESOLVED,
        expected_version=3,
        resolution_notes="   ",  # Empty / whitespace
    )
    with pytest.raises(ValueError, match="Resolution notes are mandatory"):
        service.transition_ticket(ticket.id, req_empty_notes, actor=tech)

    # Verify state retained as IN_PROGRESS and version remains 3
    db_session.refresh(ticket)
    assert ticket.state == TicketState.IN_PROGRESS
    assert ticket.version == 3


# ============================================================================
# R4: Stale expected ticket version -> Rejection; state retained (Regression)
# ============================================================================
def test_r4_stale_expected_ticket_version_rejected(db_session, seeded_users, seeded_facilities):
    """
    R4: Optimistic concurrency control test.
    Updating with a stale expected_version must be rejected, preserving the ticket state.
    """
    service = TicketService(db_session)
    admin = seeded_users["admin"]
    facility = seeded_facilities["general"]

    ticket = service.create_ticket(
        TicketCreate(
            facility_id=facility.id,
            title="Broken Door Latch",
            description="Door latch sticking",
            impact="Low",
            urgency="Low",
        ),
        creator=admin,
    )
    # Current version is 1. Attempt update specifying expected_version=99 (stale)
    req_stale = TicketTransitionRequest(target_state=TicketState.ASSIGNED, expected_version=99)
    with pytest.raises(ValueError, match="Optimistic lock conflict"):
        service.transition_ticket(ticket.id, req_stale, actor=admin)

    db_session.refresh(ticket)
    assert ticket.state == TicketState.NEW
    assert ticket.version == 1
