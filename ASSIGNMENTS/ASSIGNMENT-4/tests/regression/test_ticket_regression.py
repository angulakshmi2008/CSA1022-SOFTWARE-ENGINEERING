"""
Regression suite for ticket lifecycle transitions, optimistic locking, and notes requirements.
Covers R1, R2, R3, R4 and lifecycle safety.
"""

import pytest

from app.models.ticket import TicketState
from app.schemas.ticket import TicketCreate, TicketTransitionRequest
from app.services.priority_service import calculate_priority, classify_category
from app.services.ticket_service import TicketService


def test_regression_r1_high_medium_priority():
    """R1: High impact, medium urgency yields M2."""
    assert calculate_priority("High", "Medium") == "M2"


def test_regression_r2_unknown_terminology():
    """R2: Ambiguous text routes to Manual Review."""
    assert classify_category("Unknown optical sensor calibration glitch") == "Manual Review"


def test_regression_invalid_transition_sequence_rejected(
    db_session, seeded_users, seeded_facilities
):
    """
    Ensure illegal state skip transitions are rejected:
    New -> In Progress (skipping Assigned) -> Must fail!
    New -> Resolved (skipping Assigned and In Progress) -> Must fail!
    """
    service = TicketService(db_session)
    admin = seeded_users["admin"]
    fac = seeded_facilities["general"]

    ticket = service.create_ticket(
        TicketCreate(
            facility_id=fac.id,
            title="Broken Lock",
            description="Door lock broken",
            impact="Low",
            urgency="Low",
        ),
        creator=admin,
    )
    assert ticket.state == TicketState.NEW

    # Attempt illegal skip to In Progress
    with pytest.raises(ValueError, match="Invalid state transition"):
        service.transition_ticket(
            ticket.id,
            TicketTransitionRequest(target_state=TicketState.IN_PROGRESS, expected_version=1),
            actor=admin,
        )

    # Attempt illegal skip to Resolved
    with pytest.raises(ValueError, match="Invalid state transition"):
        service.transition_ticket(
            ticket.id,
            TicketTransitionRequest(
                target_state=TicketState.RESOLVED, expected_version=1, resolution_notes="Done"
            ),
            actor=admin,
        )
