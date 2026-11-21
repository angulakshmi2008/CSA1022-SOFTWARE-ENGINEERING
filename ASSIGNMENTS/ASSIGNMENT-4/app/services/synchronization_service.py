"""
Outbox pattern synchronization worker service for resilient external integration.
"""

import json
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.integrations.calendar_adapter import CalendarAdapter
from app.integrations.issue_tracker_adapter import IssueTrackerAdapter
from app.models.outbox_event import OutboxEvent, OutboxStatus


class SynchronizationService:
    def __init__(
        self,
        db: Session,
        calendar_adapter: Optional[CalendarAdapter] = None,
        issue_tracker_adapter: Optional[IssueTrackerAdapter] = None,
    ):
        self.db = db
        self.calendar_adapter = calendar_adapter or CalendarAdapter()
        self.issue_tracker_adapter = issue_tracker_adapter or IssueTrackerAdapter()

    def process_pending_outbox_events(self, limit: int = 50) -> List[OutboxEvent]:
        """
        Process pending or retrying events in the transactional outbox.
        Guarantee: Local bookings/tickets remain durable even when remote services fail.
        """
        events = (
            self.db.query(OutboxEvent)
            .filter(OutboxEvent.status.in_([OutboxStatus.PENDING, OutboxStatus.RETRYING]))
            .order_by(OutboxEvent.created_at.asc())
            .limit(limit)
            .all()
        )

        now = datetime.now(timezone.utc)

        for event in events:
            event.last_attempt_at = now
            try:
                payload = json.loads(event.payload)

                if event.event_type == "CALENDAR_SYNC":
                    self.calendar_adapter.sync_booking_event(payload)
                    event.status = OutboxStatus.SENT
                    event.error_message = None

                elif event.event_type == "ISSUE_TRACKER_SYNC":
                    self.issue_tracker_adapter.sync_maintenance_ticket(payload)
                    event.status = OutboxStatus.SENT
                    event.error_message = None

                else:
                    event.status = OutboxStatus.FAILED
                    event.error_message = f"Unsupported event type: {event.event_type}"

            except Exception as e:
                event.retry_count += 1
                event.error_message = str(e)
                if event.retry_count >= event.max_retries:
                    event.status = OutboxStatus.FAILED
                else:
                    event.status = OutboxStatus.RETRYING

        self.db.commit()
        return events
