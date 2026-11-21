"""
Maintenance ticket management and state lifecycle endpoints.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ticket import MaintenanceTicket, TicketState
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketResponse, TicketTransitionRequest
from app.security.authentication import get_current_user
from app.security.authorization import require_authenticated
from app.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["Maintenance Tickets"])


@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket_in: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated),
):
    """Create a new maintenance ticket with priority and category classification."""
    service = TicketService(db)
    try:
        ticket = service.create_ticket(ticket_in, creator=current_user)
        return ticket
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve)) from ve


@router.get("", response_model=List[TicketResponse])
def list_tickets(
    state: Optional[TicketState] = None,
    facility_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated),
):
    """List maintenance tickets with optional status filtering."""
    query = db.query(MaintenanceTicket)
    if state:
        query = query.filter(MaintenanceTicket.state == state)
    if facility_id:
        query = query.filter(MaintenanceTicket.facility_id == facility_id)
    return query.order_by(MaintenanceTicket.created_at.desc()).all()


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated),
):
    """Retrieve maintenance ticket details."""
    ticket = db.query(MaintenanceTicket).filter(MaintenanceTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found.")
    return ticket


@router.post("/{ticket_id}/transition", response_model=TicketResponse)
def transition_ticket(
    ticket_id: int,
    transition_in: TicketTransitionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Transition ticket state under strict lifecycle and concurrency controls:
    - New -> Assigned -> In Progress -> Resolved -> Closed
    - Checks expected_version (optimistic lock, 409 Conflict if stale)
    - Requires resolution notes for Resolved state
    - Rejects unauthorized roles (Students cannot mutate tickets, 403 Forbidden)
    """
    service = TicketService(db)
    try:
        ticket = service.transition_ticket(ticket_id, transition_in, actor=current_user)
        return ticket
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe)) from pe
    except ValueError as ve:
        msg = str(ve)
        if "Optimistic lock conflict" in msg or "Stale expected" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg) from ve
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg) from ve
