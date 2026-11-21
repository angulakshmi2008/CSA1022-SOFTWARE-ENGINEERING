"""
Sensor telemetry intake and threshold breach endpoints.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.sensor import SensorEventCreate, SensorEventResponse
from app.services.sensor_service import SensorService, sensor_breached

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post("/telemetry", response_model=SensorEventResponse, status_code=status.HTTP_201_CREATED)
def ingest_sensor_telemetry(event_in: SensorEventCreate, db: Session = Depends(get_db)):
    """
    Ingest sensor event. Supports idempotency via event_id.
    Breaches trigger automated maintenance ticket creation using strict greater-than threshold.
    """
    service = SensorService(db)
    event, is_new = service.process_sensor_event(event_in)
    return event


@router.get("/threshold-check")
def check_threshold(value: float, threshold: float = 28.0):
    """
    Direct evaluation of strict greater-than sensor threshold:
    value > threshold.
    28.00 -> False
    28.01 -> True
    """
    breached = sensor_breached(value, threshold)
    return {
        "value": value,
        "threshold": threshold,
        "breached": breached,
        "operator": "strict_greater_than",
    }
