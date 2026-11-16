from pydantic import BaseModel, Field
from typing import Optional

class RefundCreateRequest(BaseModel):
    order_id: str
    amount: float = Field(gt=0, description="Refund amount must be positive")
    reason: str
    idempotency_key: Optional[str] = None

class RefundApproveRequest(BaseModel):
    decision: str = Field(description="'APPROVE' or 'REJECT'")
    notes: Optional[str] = None

class RefundExecuteRequest(BaseModel):
    simulate_gateway_failure: bool = False

class RefundResponse(BaseModel):
    refund_id: str
    order_id: str
    amount: float
    state: str
    reason: str
    requested_by: str
    approved_by: Optional[str] = None
    idempotency_key: str
    failure_reason: Optional[str] = None
    created_at: str
    resolved_at: Optional[str] = None
