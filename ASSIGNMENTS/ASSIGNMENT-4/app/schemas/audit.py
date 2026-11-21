"""
Pydantic schemas for Audit Logs and Outbox events.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.outbox_event import OutboxStatus


class AuditLogResponse(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    action: str
    old_state: Optional[str]
    new_state: Optional[str]
    actor_id: Optional[int]
    actor_role: Optional[str]
    details: Optional[str]
    version: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class OutboxEventResponse(BaseModel):
    id: int
    event_type: str
    aggregate_type: str
    aggregate_id: int
    status: OutboxStatus
    retry_count: int
    max_retries: int
    last_attempt_at: Optional[datetime]
    error_message: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
