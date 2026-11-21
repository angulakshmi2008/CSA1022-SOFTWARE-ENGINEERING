"""
Integration tests for sensor event intake, breach detection, and idempotency.
Matches Assignment 4 faculty specification: I2.
"""

from app.models.sensor_event import SensorEvent
from app.models.ticket import MaintenanceTicket
from app.schemas.sensor import SensorEventCreate
from app.services.sensor_service import SensorService


# ============================================================================
# I2: Same sensor event submitted 5 times -> 1 logical event, 1 ticket
# ============================================================================
def test_i2_sensor_event_idempotency_five_submissions(db_session, seeded_facilities):
    """
    I2: Replay attack / network retry test.
    The same sensor event (identical event_id) is submitted 5 times.
    Oracle:
    1. Exactly 1 sensor_events database record exists.
    2. Exactly 1 maintenance ticket is created.
    3. Subsequent 4 submissions are identified as duplicates without errors.
    """
    service = SensorService(db_session)
    facility = seeded_facilities["general"]

    # Breaching value: 29.5C > 28.0C threshold
    event_data = SensorEventCreate(
        event_id="EVT-TEMP-TURING-101-20261121-001",
        sensor_id="TEMP-SN-9988",
        sensor_type="temperature",
        facility_id=facility.id,
        value=29.5,
        unit="celsius",
    )

    results = []
    # Submit the identical event 5 consecutive times
    for _ in range(5):
        event, is_new = service.process_sensor_event(event_data)
        results.append((event, is_new))

    # Verification: First submission is newly created, following 4 are recognized duplicates
    assert results[0][1] is True, "First submission should be marked as new"
    for idx in range(1, 5):
        assert results[idx][1] is False, f"Submission {idx + 1} should be identified as duplicate"
        assert results[idx][0].id == results[0][0].id, (
            f"Submission {idx + 1} should return same record ID"
        )

    # Database level check: Exactly 1 sensor event record
    total_events = (
        db_session.query(SensorEvent).filter(SensorEvent.event_id == event_data.event_id).count()
    )
    assert total_events == 1, f"Expected 1 SensorEvent in DB, found {total_events}"

    # Database level check: Exactly 1 linked maintenance ticket created
    total_tickets = (
        db_session.query(MaintenanceTicket)
        .filter(MaintenanceTicket.sensor_event_id == results[0][0].id)
        .count()
    )
    assert total_tickets == 1, f"Expected exactly 1 MaintenanceTicket, found {total_tickets}"
