"""
Regression tests for campus-specific policies and schema evolution (Q6 Adaptation).
"""

from datetime import datetime, timedelta, timezone

import pytest

from app.models.facility import Facility
from app.schemas.booking import BookingCreate
from app.services.booking_service import BookingService
from app.services.sensor_service import SensorService, sensor_breached


def test_campus_specific_duration_policy(db_session, seeded_users, seeded_facilities):
    """
    Q6 Adaptation:
    - Main Campus: 180 min limit
    - North Campus: 120 min limit
    Ensure 150-minute booking succeeds on Main Campus but fails on North Campus.
    """
    service = BookingService(db_session)
    user = seeded_users["prof_smith"]
    main_fac = seeded_facilities["general"]  # Main Campus
    p_north = seeded_facilities["policy_north"]

    north_fac = Facility(
        code="NC-SEM-1",
        name="North Campus Seminar Hall",
        campus="North Campus",
        building="Newton Wing",
        room_number="10",
        facility_type="Seminar Hall",
        capacity=60,
        policy_id=p_north.id,
    )
    db_session.add(north_fac)
    db_session.commit()
    db_session.refresh(north_fac)

    start = datetime.now(timezone.utc) + timedelta(days=30)
    end_150 = start + timedelta(minutes=150)

    # 150 minutes on Main Campus (Limit: 180) -> Succeeds
    b_main = service.create_booking(
        BookingCreate(
            facility_id=main_fac.id, title="Main Campus 150m", start_time=start, end_time=end_150
        ),
        current_user=user,
    )
    assert b_main.id is not None

    # 150 minutes on North Campus (Limit: 120) -> Fails
    with pytest.raises(ValueError, match="exceeds maximum allowed limit of 120 minutes"):
        service.create_booking(
            BookingCreate(
                facility_id=north_fac.id,
                title="North Campus 150m",
                start_time=start,
                end_time=end_150,
            ),
            current_user=user,
        )


def test_campus_specific_sensor_threshold(db_session, seeded_facilities):
    """
    Q6 Adaptation:
    - Main Campus threshold: 28.0C
    - North Campus threshold: 26.0C
    A reading of 27.0C does NOT breach Main Campus, but breaches North Campus!
    """
    service = SensorService(db_session)
    main_fac = seeded_facilities["general"]
    p_north = seeded_facilities["policy_north"]

    north_fac = Facility(
        code="NC-SERVER-1",
        name="North Campus Server Room",
        campus="North Campus",
        building="Newton Wing",
        room_number="SR1",
        facility_type="Server Room",
        capacity=5,
        policy_id=p_north.id,
    )
    db_session.add(north_fac)
    db_session.commit()

    main_thresh = service.get_facility_threshold(main_fac.id)
    north_thresh = service.get_facility_threshold(north_fac.id)

    assert main_thresh == 28.0
    assert north_thresh == 26.0

    reading = 27.0
    assert sensor_breached(reading, main_thresh) is False, "27.0 should not breach 28.0 threshold"
    assert sensor_breached(reading, north_thresh) is True, "27.0 should breach 26.0 threshold"
