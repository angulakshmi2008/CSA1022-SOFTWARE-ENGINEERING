"""
External Issue Tracker integration adapter (e.g. Jira / GitLab Issues / GitHub Issues).
"""

from typing import Any, Dict


class IssueTrackerAdapter:
    def __init__(
        self,
        service_url: str = "https://jira.campus.internal/rest/api/2",
        simulate_down: bool = False,
    ):
        self.service_url = service_url
        self.simulate_down = simulate_down

    def sync_maintenance_ticket(self, ticket_payload: Dict[str, Any]) -> str:
        """
        Create or update external issue tracker issue.
        Returns external issue key (e.g. 'CAMPUS-102') or raises ConnectionError on failure.
        """
        if self.simulate_down:
            raise ConnectionError("Developer Issue Tracker (Jira) API connection timed out.")

        ticket_number = ticket_payload.get("ticket_number", "TKT-UNKNOWN")
        return f"CAMPUS-{ticket_number[-4:]}"
