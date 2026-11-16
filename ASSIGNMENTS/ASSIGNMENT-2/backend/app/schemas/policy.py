from pydantic import BaseModel, Field

class PolicyUpdate(BaseModel):
    tax_rate: float = Field(ge=0.0, le=1.0)
    shipping_fee: float = Field(ge=0.0)
    refund_approval_threshold: float = Field(ge=0.0)

class RegionalPolicyResponse(BaseModel):
    region_id: str
    region_name: str
    policy_version: int
    tax_rate: float
    shipping_fee: float
    refund_approval_threshold: float
    is_active: bool
