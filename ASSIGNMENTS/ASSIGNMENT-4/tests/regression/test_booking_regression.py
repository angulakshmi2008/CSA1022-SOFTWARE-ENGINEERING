"""
Regression suite for facility booking rules, overlap protection, and boundary integrity.
Ensures previously verified behavior remains strictly enforced.
"""

from datetime import datetime, timedelta, timezone

import pytest

from app.models.booking import BookingStatus
from app.schemas.booking import BookingCreate
from app.services.booking_service import BookingService


def test_regression_booking_duration_boundary(db_session, seeded_users, seeded_facilities):
    """Regression: 180m accepted, 181m rejected."""
    service = BookingService(db_session)
    user = seeded_users["prof_smith"]
    fac = seeded_facilities["general"]

    start = datetime.now(timezone.utc) + timedelta(days=20)
    end_180 = start + timedelta(minutes=180)
    end_181 = start + timedelta(minutes=181)

    # 180 min must pass
    b_180 = service.create_booking(
        BookingCreate(facility_id=fac.id, title="180m Session", start_time=start, end_time=end_180),
        current_user=user,
    )
    assert b_180.status == BookingStatus.CONFIRMED

    # 181 min must fail
    with pytest.raises(ValueError, match="exceeds maximum allowed limit"):
        service.create_booking(
            BookingCreate(
                facility_id=fac.id,
                title="181m Session",
                start_time=start + timedelta(days=1),
                end_time=end_181 + timedelta(days=1),
            ),
            current_user=user,
        )


def test_regression_booking_overlap_prevention(db_session, seeded_users, seeded_facilities):
    """Regression: Simultaneous bookings must be prevented."""
    service = BookingService(db_session)
    user = seeded_users["prof_smith"]
    fac = seeded_facilities["general"]

    start = datetime.now(timezone.utc) + timedelta(days=22)
    end = start + timedelta(hours=2)

    # First booking
    b1 = service.create_booking(
        BookingCreate(facility_id=fac.id, title="First Booking", start_time=start, end_time=end),
        current_user=user,
    )
    assert b1.id is not None

    # Exact overlap attempt
    with pytest.raises(ValueError, match="overlaps with existing reservation"):
        service.create_booking(
            BookingCreate(
                facility_id=fac.id, title="Exact Duplicate", start_time=start, end_time=end
            ),
            current_user=user,
        )
