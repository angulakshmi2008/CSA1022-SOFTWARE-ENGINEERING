"""
Sensor event processing, threshold checking, and telemetry ingestion service.
"""

from datetime import datetime, timezone
from typing import Tuple

from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.models.facility import Facility
from app.models.sensor_event import SensorEvent
from app.models.ticket import MaintenanceTicket, TicketState
from app.schemas.sensor import SensorEventCreate
from app.services.priority_service import calculate_priority
from app.services.sla_service import calculate_sla_deadline


def sensor_breached(value: float, threshold: float = 28.0) -> bool:
    """
    Check if a sensor value exceeds the threshold.
    CRITICAL POLICY: Uses strict greater-than comparison.
    28.00 -> False (does not breach)
    28.01 -> True (breaches)
    """
    return value > threshold


class SensorService:
    def __init__(self, db: Session):
        self.db = db

    def get_facility_threshold(self, facility_id: int) -> float:
        """Retrieve threshold for facility based on campus policy or default 28.0."""
        facility = self.db.query(Facility).filter(Facility.id == facility_id).first()
        if facility and facility.policy and facility.policy.is_active:
            return facility.policy.temp_threshold
        return 28.0

    def process_sensor_event(self, event_data: SensorEventCreate) -> Tuple[SensorEvent, bool]:
        """
        Process sensor submission with idempotency.
        Returns (SensorEvent, is_newly_created: bool).
        If event_id already exists, returns existing record without duplicating.
        """
        # Idempotency check: see if event already recorded
        existing_event = (
            self.db.query(SensorEvent).filter(SensorEvent.event_id == event_data.event_id).first()
        )

        if existing_event:
            return existing_event, False

        # Look up threshold
        threshold = self.get_facility_threshold(event_data.facility_id)
        is_breached = sensor_breached(event_data.value, threshold)

        sensor_event = SensorEvent(
            event_id=event_data.event_id,
            sensor_id=event_data.sensor_id,
            sensor_type=event_data.sensor_type,
            facility_id=event_data.facility_id,
            value=event_data.value,
            unit=event_data.unit,
            threshold=threshold,
            is_breached=is_breached,
            processed_at=datetime.now(timezone.utc),
        )
        self.db.add(sensor_event)
        self.db.flush()

        # If breached, automatically create a linked maintenance ticket
        if is_breached:
            impact = "High"
            urgency = "Medium"
            priority = calculate_priority(impact, urgency)  # M2
            category = "HVAC" if event_data.sensor_type == "temperature" else "Facilities"
            now = datetime.now(timezone.utc)
            deadline = calculate_sla_deadline(priority, now)

            ticket_number = f"TKT-AUTO-{event_data.event_id[:16]}-{sensor_event.id}"
            ticket = MaintenanceTicket(
                ticket_number=ticket_number,
                facility_id=event_data.facility_id,
                title=f"Automated Alert: {event_data.sensor_type} breach ({event_data.value} {event_data.unit})",
                description=(
                    f"Automated telemetry alert from sensor {event_data.sensor_id}. "
                    f"Recorded value {event_data.value} exceeded threshold of {threshold} {event_data.unit}."
                ),
                category=category,
                impact=impact,
                urgency=urgency,
                priority=priority,
                state=TicketState.NEW,
                sensor_event_id=sensor_event.id,
                sla_deadline=deadline,
                version=1,
                created_at=now,
                updated_at=now,
            )
            self.db.add(ticket)
            self.db.flush()

            sensor_event.maintenance_ticket_id = ticket.id

            # Create audit record
            audit = AuditLog(
                entity_type="MaintenanceTicket",
                entity_id=ticket.id,
                action="CREATE_AUTOMATED",
                old_state=None,
                new_state=TicketState.NEW.value,
                actor_id=None,
                actor_role="SYSTEM_TELEMETRY",
                details=f"Automated ticket created from breached sensor event {event_data.event_id}",
                version=1,
                timestamp=now,
            )
            self.db.add(audit)

        self.db.commit()
        self.db.refresh(sensor_event)
        return sensor_event, True
