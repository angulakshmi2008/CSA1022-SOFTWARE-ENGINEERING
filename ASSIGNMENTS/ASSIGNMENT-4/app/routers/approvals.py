"""
Approval endpoints for restricted facilities.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.booking import BookingApprovalRequest, BookingResponse
from app.security.authentication import get_current_user
from app.services.approval_service import ApprovalService

router = APIRouter(prefix="/approvals", tags=["Approvals"])


@router.post("/bookings/{booking_id}", response_model=BookingResponse)
def approve_or_reject_booking(
    booking_id: int,
    approval_in: BookingApprovalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Approve or reject a restricted facility booking.
    Enforces role-based permissions: Students cannot approve.
    Direct API authorization check leaves state completely unchanged on failure.
    """
    service = ApprovalService(db)
    try:
        updated_booking = service.process_booking_approval(
            booking_id=booking_id,
            approved=approval_in.approved,
            notes=approval_in.notes or "",
            actor=current_user,
        )
        return updated_booking
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe)) from pe
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve)) from ve
