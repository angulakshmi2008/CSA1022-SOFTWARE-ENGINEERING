"""
Booking management endpoints.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse
from app.security.authorization import require_authenticated
from app.services.booking_service import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated),
):
    """
    Create a new facility booking.
    Enforces maximum duration (180 min default) and half-open interval overlap checks.
    """
    service = BookingService(db)
    try:
        booking = service.create_booking(booking_in, current_user)
        return booking
    except ValueError as e:
        msg = str(e)
        if "overlaps with existing reservation" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg) from e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg) from e


@router.get("", response_model=List[BookingResponse])
def list_bookings(
    facility_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated),
):
    """List bookings. Regular users view their bookings; staff can view all."""
    service = BookingService(db)
    # If user is student, only show own bookings unless facility specified
    user_id_filter = current_user.id if current_user.role.value == "STUDENT" else None
    return service.list_bookings(facility_id=facility_id, user_id=user_id_filter)


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authenticated),
):
    """Retrieve booking details."""
    service = BookingService(db)
    booking = service.get_booking_by_id(booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found.")
    return booking
