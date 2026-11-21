"""
Facility catalog and campus policy management routes.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.facility import Facility, FacilityPolicy
from app.models.user import User
from app.schemas.facility import (
    FacilityCreate,
    FacilityPolicyCreate,
    FacilityPolicyResponse,
    FacilityResponse,
)
from app.security.authorization import require_facility_manager_or_admin

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("", response_model=List[FacilityResponse])
def list_facilities(
    campus: Optional[str] = None,
    is_restricted: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """List campus facilities with optional filtering."""
    query = db.query(Facility)
    if campus:
        query = query.filter(Facility.campus == campus)
    if is_restricted is not None:
        query = query.filter(Facility.is_restricted == is_restricted)
    return query.all()


@router.get("/{facility_id}", response_model=FacilityResponse)
def get_facility(facility_id: int, db: Session = Depends(get_db)):
    """Retrieve detailed facility information."""
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Facility with ID {facility_id} not found.",
        )
    return facility


@router.post("", response_model=FacilityResponse, status_code=status.HTTP_201_CREATED)
def create_facility(
    facility_in: FacilityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_facility_manager_or_admin),
):
    """Create a new facility record (Facility Managers and Administrators only)."""
    existing = db.query(Facility).filter(Facility.code == facility_in.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Facility code '{facility_in.code}' already exists.",
        )

    facility = Facility(
        code=facility_in.code,
        name=facility_in.name,
        campus=facility_in.campus,
        building=facility_in.building,
        room_number=facility_in.room_number,
        facility_type=facility_in.facility_type,
        capacity=facility_in.capacity,
        is_restricted=facility_in.is_restricted,
        policy_id=facility_in.policy_id,
    )
    db.add(facility)
    db.commit()
    db.refresh(facility)
    return facility


@router.post(
    "/policies", response_model=FacilityPolicyResponse, status_code=status.HTTP_201_CREATED
)
def create_campus_policy(
    policy_in: FacilityPolicyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_facility_manager_or_admin),
):
    """Define a campus-specific policy (duration limit, temperature threshold)."""
    policy = FacilityPolicy(
        campus=policy_in.campus,
        facility_type=policy_in.facility_type,
        max_duration_minutes=policy_in.max_duration_minutes,
        temp_threshold=policy_in.temp_threshold,
        requires_approval_for_restricted=policy_in.requires_approval_for_restricted,
        policy_version=policy_in.policy_version,
        is_active=policy_in.is_active,
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy
