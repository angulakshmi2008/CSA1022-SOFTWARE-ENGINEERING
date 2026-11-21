"""
Integration outbox and audit log inspection endpoints.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.audit import AuditLog
from app.models.outbox_event import OutboxEvent
from app.models.user import User
from app.schemas.audit import AuditLogResponse, OutboxEventResponse
from app.security.authorization import require_facility_manager_or_admin
from app.services.synchronization_service import SynchronizationService

router = APIRouter(prefix="/integrations", tags=["Integrations & Outbox"])


@router.post("/outbox/process", response_model=List[OutboxEventResponse])
def process_outbox(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_facility_manager_or_admin),
):
    """Trigger background synchronization worker for outbox events."""
    service = SynchronizationService(db)
    events = service.process_pending_outbox_events(limit=limit)
    return events


@router.get("/outbox", response_model=List[OutboxEventResponse])
def list_outbox_events(
    db: Session = Depends(get_db), current_user: User = Depends(require_facility_manager_or_admin)
):
    """List recent transactional outbox synchronization records."""
    return db.query(OutboxEvent).order_by(OutboxEvent.created_at.desc()).limit(100).all()


@router.get("/audit", response_model=List[AuditLogResponse])
def list_audit_logs(
    entity_type: Optional[str] = None,
    entity_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_facility_manager_or_admin),
):
    """Retrieve immutable audit trail entries."""
    query = db.query(AuditLog)
    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)
    if entity_id:
        query = query.filter(AuditLog.entity_id == entity_id)
    return query.order_by(AuditLog.timestamp.desc()).limit(100).all()
