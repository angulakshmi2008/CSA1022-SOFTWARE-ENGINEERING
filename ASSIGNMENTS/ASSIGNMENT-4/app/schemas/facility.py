"""
Pydantic schemas for Facility and Facility Policy.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FacilityPolicyBase(BaseModel):
    campus: str
    facility_type: Optional[str] = "General"
    max_duration_minutes: int = Field(default=180, gt=0)
    temp_threshold: float = Field(default=28.0)
    requires_approval_for_restricted: bool = True
    policy_version: int = Field(default=1, ge=1)
    is_active: bool = True


class FacilityPolicyCreate(FacilityPolicyBase):
    pass


class FacilityPolicyResponse(FacilityPolicyBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FacilityBase(BaseModel):
    code: str
    name: str
    campus: str = "Main Campus"
    building: str
    room_number: str
    facility_type: str = "General"
    capacity: int = Field(default=30, gt=0)
    is_restricted: bool = False


class FacilityCreate(FacilityBase):
    policy_id: Optional[int] = None


class FacilityResponse(FacilityBase):
    id: int
    policy_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
