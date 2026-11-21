"""
Integration and security tests for role-based authorization boundaries.
Matches Assignment 4 faculty specification: I3.
"""

from datetime import datetime, timedelta, timezone

from fastapi import status

from app.models.audit import AuditLog
from app.models.booking import BookingStatus
from app.schemas.booking import BookingCreate
from app.services.booking_service import BookingService
from tests.conftest import make_auth_header


# ============================================================================
# I3: Student attempts restricted booking approval -> Rejected, Pending state retained
# ============================================================================
def test_i3_student_restricted_approval_rejected(
    db_session, seeded_users, seeded_facilities, client
):
    """
    I3: Direct API authorization test.
    A student attempts to approve a restricted facility booking.
    Oracle:
    1. Direct API request returns HTTP 403 Forbidden.
    2. Booking remains strictly in 'PENDING_APPROVAL' state.
    3. Database state is NOT mutated by the unauthorized request.
    """
    booking_service = BookingService(db_session)
    student = seeded_users["student_charlie"]
    restricted_fac = seeded_facilities["restricted"]

    # Student books a restricted facility -> Status is PENDING_APPROVAL
    start = datetime.now(timezone.utc) + timedelta(days=1)
    end = start + timedelta(hours=2)

    booking = booking_service.create_booking(
        BookingCreate(
            facility_id=restricted_fac.id,
            title="Robotics Team Practice",
            start_time=start,
            end_time=end,
        ),
        current_user=student,
    )
    assert booking.status == BookingStatus.PENDING_APPROVAL
    initial_version = booking.version
    booking_id = booking.id

    # Count audit logs before attack
    audit_count_before = db_session.query(AuditLog).count()

    # Student attempts to approve their own booking via direct API call
    student_header = make_auth_header(student)
    response = client.post(
        f"/api/v1/approvals/bookings/{booking_id}",
        json={"approved": True, "notes": "Self-approved by student"},
        headers=student_header,
    )

    # 1. API boundary rejects request
    assert response.status_code == status.HTTP_403_FORBIDDEN, (
        f"Expected 403 Forbidden, but got {response.status_code}: {response.text}"
    )

    # 2. Verify persistent database state is UNCHANGED
    db_session.refresh(booking)
    assert booking.status == BookingStatus.PENDING_APPROVAL, (
        f"Security violation! Booking status changed to {booking.status.value}"
    )
    assert booking.approved_by_user_id is None
    assert booking.version == initial_version

    # 3. Verify no illegitimate approval audit log was written
    audit_count_after = db_session.query(AuditLog).count()
    assert audit_count_after == audit_count_before


def test_approver_can_approve_restricted_booking(
    db_session, seeded_users, seeded_facilities, client
):
    """Verify that an authorized Department Approver CAN approve the booking."""
    booking_service = BookingService(db_session)
    student = seeded_users["student_charlie"]
    approver = seeded_users["approver_alice"]
    restricted_fac = seeded_facilities["restricted"]

    start = datetime.now(timezone.utc) + timedelta(days=2)
    end = start + timedelta(hours=2)

    booking = booking_service.create_booking(
        BookingCreate(
            facility_id=restricted_fac.id,
            title="AI Lab Research Session",
            start_time=start,
            end_time=end,
        ),
        current_user=student,
    )
    assert booking.status == BookingStatus.PENDING_APPROVAL

    approver_header = make_auth_header(approver)
    response = client.post(
        f"/api/v1/approvals/bookings/{booking.id}",
        json={"approved": True, "notes": "Legitimate academic project"},
        headers=approver_header,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "CONFIRMED"
    assert data["approved_by_user_id"] == approver.id


def test_student_cannot_mutate_ticket_state(db_session, seeded_users, seeded_facilities, client):
    """Verify that a Student role cannot mutate ticket states via API (403 Forbidden)."""
    admin = seeded_users["admin"]
    student = seeded_users["student_charlie"]
    fac = seeded_facilities["general"]

    from app.schemas.ticket import TicketCreate
    from app.services.ticket_service import TicketService

    ticket = TicketService(db_session).create_ticket(
        TicketCreate(
            facility_id=fac.id,
            title="Broken Chair",
            description="Chair wheel broken",
            impact="Low",
            urgency="Low",
        ),
        creator=admin,
    )

    student_header = make_auth_header(student)
    response = client.post(
        f"/api/v1/tickets/{ticket.id}/transition",
        json={"target_state": "Assigned", "expected_version": 1},
        headers=student_header,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
