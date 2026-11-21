"""
Unit tests for SLA deadline calculation, timezone awareness, and overdue equality boundaries.
"""

from datetime import datetime, timedelta, timezone

from app.services.sla_service import calculate_sla_deadline, is_sla_overdue


def test_sla_deadline_calculation_with_injected_clock():
    """Verify SLA deadline offsets for all priorities using a fixed mock clock."""
    fixed_start = datetime(2026, 11, 21, 10, 0, 0, tzinfo=timezone.utc)

    d_m1 = calculate_sla_deadline("M1", fixed_start)
    assert d_m1 == fixed_start + timedelta(hours=2)

    d_m2 = calculate_sla_deadline("M2", fixed_start)
    assert d_m2 == fixed_start + timedelta(hours=8)

    d_m3 = calculate_sla_deadline("M3", fixed_start)
    assert d_m3 == fixed_start + timedelta(hours=24)

    d_m4 = calculate_sla_deadline("M4", fixed_start)
    assert d_m4 == fixed_start + timedelta(hours=72)


def test_sla_overdue_boundary_equality_rule():
    """
    CRITICAL POLICY: now > deadline is overdue.
    Equality (now == deadline) is NOT yet overdue.
    Test at:
    - 1 second before deadline -> False
    - Exactly at deadline -> False
    - 1 second after deadline -> True
    """
    deadline = datetime(2026, 11, 21, 14, 0, 0, tzinfo=timezone.utc)

    one_sec_before = deadline - timedelta(seconds=1)
    exactly_at = deadline
    one_sec_after = deadline + timedelta(seconds=1)

    assert is_sla_overdue(deadline, current_time=one_sec_before) is False, (
        "1 second before deadline must not be overdue"
    )
    assert is_sla_overdue(deadline, current_time=exactly_at) is False, (
        "Exactly at deadline (equality) must not be overdue"
    )
    assert is_sla_overdue(deadline, current_time=one_sec_after) is True, (
        "1 second after deadline must be overdue"
    )
