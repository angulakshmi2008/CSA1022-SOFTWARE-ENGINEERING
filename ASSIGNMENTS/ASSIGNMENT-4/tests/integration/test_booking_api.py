"""
Integration tests for booking API, duration policies, and overlap rejection.
Matches Assignment 4 faculty specification: I4.
"""

from datetime import datetime, timedelta, timezone

from fastapi import status

from tests.conftest import make_auth_header


# ============================================================================
# I4: Overlapping and adjacent bookings -> Overlap rejected, adjacent accepted
# ============================================================================
def test_i4_overlapping_and_adjacent_bookings(db_session, seeded_users, seeded_facilities, client):
    """
    I4: Integration test via HTTP API.
    1. Create Base Booking [10:00 - 12:00] -> Accepted (201 Created).
    2. Attempt Overlapping Booking [11:00 - 13:00] -> Rejected (409 Conflict).
    3. Attempt Adjacent Booking [12:00 - 14:00] -> Accepted (201 Created).
    """
    faculty_user = seeded_users["prof_smith"]
    facility = seeded_facilities["general"]
    headers = make_auth_header(faculty_user)

    base_day = datetime.now(timezone.utc) + timedelta(days=5)
    t1000 = base_day.replace(hour=10, minute=0, second=0, microsecond=0)
    t1100 = base_day.replace(hour=11, minute=0, second=0, microsecond=0)
    t1200 = base_day.replace(hour=12, minute=0, second=0, microsecond=0)
    t1300 = base_day.replace(hour=13, minute=0, second=0, microsecond=0)
    t1400 = base_day.replace(hour=14, minute=0, second=0, microsecond=0)

    # 1. Base Booking: 10:00 - 12:00
    res1 = client.post(
        "/api/v1/bookings",
        json={
            "facility_id": facility.id,
            "title": "Software Architecture Lecture",
            "start_time": t1000.isoformat(),
            "end_time": t1200.isoformat(),
        },
        headers=headers,
    )
    assert res1.status_code == status.HTTP_201_CREATED, f"Base booking failed: {res1.text}"
    b1_data = res1.json()
    assert b1_data["status"] == "CONFIRMED"

    # 2. Overlapping Booking: 11:00 - 13:00 (Overlaps by 60 mins)
    res_overlap = client.post(
        "/api/v1/bookings",
        json={
            "facility_id": facility.id,
            "title": "Conflicting Seminar",
            "start_time": t1100.isoformat(),
            "end_time": t1300.isoformat(),
        },
        headers=headers,
    )
    assert res_overlap.status_code == status.HTTP_409_CONFLICT, (
        f"Overlapping booking must return 409 Conflict, got {res_overlap.status_code}: {res_overlap.text}"
    )

    # 3. Adjacent Booking: 12:00 - 14:00 (Starts exactly when Base booking ends)
    res_adjacent = client.post(
        "/api/v1/bookings",
        json={
            "facility_id": facility.id,
            "title": "Data Mining Lab Session",
            "start_time": t1200.isoformat(),
            "end_time": t1400.isoformat(),
        },
        headers=headers,
    )
    assert res_adjacent.status_code == status.HTTP_201_CREATED, (
        f"Adjacent booking sharing boundary must return 201 Created, got {res_adjacent.status_code}: {res_adjacent.text}"
    )
    b_adj_data = res_adjacent.json()
    assert b_adj_data["status"] == "CONFIRMED"


def test_booking_duration_api_180_accepted_181_rejected(
    db_session, seeded_users, seeded_facilities, client
):
    """
    API duration validation:
    - 180 minutes: Accepted (201 Created)
    - 181 minutes: Rejected (400 Bad Request)
    """
    faculty_user = seeded_users["prof_smith"]
    facility = seeded_facilities["general"]
    headers = make_auth_header(faculty_user)

    base = datetime.now(timezone.utc) + timedelta(days=10)
    start = base.replace(hour=8, minute=0, second=0, microsecond=0)

    # 180 minutes (8:00 to 11:00) -> Allowed
    end_180 = start + timedelta(minutes=180)
    res_180 = client.post(
        "/api/v1/bookings",
        json={
            "facility_id": facility.id,
            "title": "3-Hour Hackathon Session",
            "start_time": start.isoformat(),
            "end_time": end_180.isoformat(),
        },
        headers=headers,
    )
    assert res_180.status_code == status.HTTP_201_CREATED

    # 181 minutes on another day -> Rejected
    start_next = start + timedelta(days=1)
    end_181 = start_next + timedelta(minutes=181)
    res_181 = client.post(
        "/api/v1/bookings",
        json={
            "facility_id": facility.id,
            "title": "3-Hour 1-Min Overlong Session",
            "start_time": start_next.isoformat(),
            "end_time": end_181.isoformat(),
        },
        headers=headers,
    )
    assert res_181.status_code == status.HTTP_400_BAD_REQUEST
    assert "exceeds maximum allowed limit of 180 minutes" in res_181.text
