"""
SLA calculation and deadline verification service.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from app.config import get_settings

settings = get_settings()

SLA_HOURS_MAP = {
    "M1": 2,
    "M2": 8,
    "M3": 24,
    "M4": 72,
    "Manual Review": 24,
}


def calculate_sla_deadline(priority: str, start_time: Optional[datetime] = None) -> datetime:
    """
    Calculate SLA deadline in UTC based on priority.
    Uses start_time or current UTC time if not provided (injectable clock).
    """
    base_time = start_time or datetime.now(timezone.utc)
    if base_time.tzinfo is None:
        base_time = base_time.replace(tzinfo=timezone.utc)

    hours = SLA_HOURS_MAP.get(priority, settings.SLA_HOURS_M3)
    return base_time + timedelta(hours=hours)


def is_sla_overdue(deadline: datetime, current_time: Optional[datetime] = None) -> bool:
    """
    Check if SLA is overdue.
    CRITICAL POLICY: now > deadline.
    Equality (now == deadline) is NOT yet overdue.
    """
    now = current_time or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)

    return now > deadline
