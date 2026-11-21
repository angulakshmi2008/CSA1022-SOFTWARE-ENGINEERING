"""
External Calendar integration adapter (e.g. Google Calendar / Exchange / CalDAV).
"""

from typing import Any, Dict


class CalendarAdapter:
    def __init__(
        self,
        service_url: str = "https://calendar.campus.internal/api/v1",
        simulate_down: bool = False,
    ):
        self.service_url = service_url
        self.simulate_down = simulate_down

    def sync_booking_event(self, event_payload: Dict[str, Any]) -> bool:
        """
        Synchronize confirmed booking to the campus calendar service.
        Returns True if successful, raises ConnectionError/TimeoutError if unavailable.
        """
        if self.simulate_down:
            raise ConnectionError(
                "External Campus Calendar service is unreachable (503 Service Unavailable)."
            )

        # In a real environment, this makes an HTTP POST request with retry headers
        # For reliable testing, return success
        return True
