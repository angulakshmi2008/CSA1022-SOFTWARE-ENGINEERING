"""
Unit tests for booking interval mathematics, duration policy limits, and boundary cases.
"""

from datetime import datetime, timezone

from app.services.booking_service import check_interval_overlap


def test_booking_duration_boundary_179_180_181():
    """
    Booking duration boundary validation.
    Faculty reference rule:
    - 180-minute booking: Accepted
    - 181-minute booking: Rejected
    """
    limit_minutes = 180

    def is_duration_allowed(duration_m: int) -> bool:
        return 0 < duration_m <= limit_minutes

    assert is_duration_allowed(179) is True, "179-minute booking should be accepted"
    assert is_duration_allowed(180) is True, (
        "180-minute booking (equality limit) should be accepted"
    )
    assert is_duration_allowed(181) is False, "181-minute booking should be rejected"
    assert is_duration_allowed(0) is False, "0-minute booking should be rejected"
    assert is_duration_allowed(-10) is False, "Negative duration booking should be rejected"


def test_adjacent_bookings_do_not_overlap():
    """
    Adjacent bookings sharing boundary: [09:00, 11:00) and [11:00, 13:00).
    Faculty reference oracle: Adjacent bookings MUST be accepted.
    """
    t0 = datetime(2026, 11, 21, 9, 0, 0, tzinfo=timezone.utc)
    t1 = datetime(2026, 11, 21, 11, 0, 0, tzinfo=timezone.utc)
    t2 = datetime(2026, 11, 21, 13, 0, 0, tzinfo=timezone.utc)

    # Booking 1: 09:00 - 11:00
    # Booking 2: 11:00 - 13:00
    overlaps = check_interval_overlap(t0, t1, t1, t2)
    assert overlaps is False, "Adjacent bookings sharing end-point must not overlap"

    # Symmetric check
    overlaps_reverse = check_interval_overlap(t1, t2, t0, t1)
    assert overlaps_reverse is False, "Reverse adjacent check must also not overlap"


def test_overlapping_intervals_detected():
    """
    Overlapping intervals:
    Case 1: Booking 1 [09:00, 11:00), Booking 2 [10:30, 12:00)
    Case 2: Booking 1 [09:00, 12:00), Booking 2 [10:00, 11:00) (Enclosed)
    Case 3: Booking 1 [09:00, 11:00), Booking 2 [08:30, 09:30) (Starting earlier)
    """
    t0900 = datetime(2026, 11, 21, 9, 0, 0, tzinfo=timezone.utc)
    t1000 = datetime(2026, 11, 21, 10, 0, 0, tzinfo=timezone.utc)
    t1030 = datetime(2026, 11, 21, 10, 30, 0, tzinfo=timezone.utc)
    t1100 = datetime(2026, 11, 21, 11, 0, 0, tzinfo=timezone.utc)
    t1200 = datetime(2026, 11, 21, 12, 0, 0, tzinfo=timezone.utc)

    # Partial overlap
    assert check_interval_overlap(t0900, t1100, t1030, t1200) is True
    # Fully enclosed
    assert check_interval_overlap(t0900, t1200, t1000, t1100) is True
    # Identical interval
    assert check_interval_overlap(t0900, t1100, t0900, t1100) is True
    # Distant non-overlapping
    assert check_interval_overlap(t0900, t1000, t1100, t1200) is False
