"""
Pydantic schemas for Sensor Events and Telemetry Ingestion.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SensorEventCreate(BaseModel):
    event_id: str = Field(min_length=3, max_length=100)
    sensor_id: str = Field(min_length=2, max_length=50)
    sensor_type: str = Field(default="temperature", max_length=30)
    facility_id: int
    value: float
    unit: str = Field(default="celsius", max_length=20)


class SensorEventResponse(BaseModel):
    id: int
    event_id: str
    sensor_id: str
    sensor_type: str
    facility_id: int
    value: float
    unit: str
    threshold: float
    is_breached: bool
    processed_at: datetime
    maintenance_ticket_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)
