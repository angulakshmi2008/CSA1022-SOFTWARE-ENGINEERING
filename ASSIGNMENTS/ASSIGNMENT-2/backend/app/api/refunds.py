from fastapi import APIRouter, Depends, Header, status
from typing import List, Optional
from backend.app.schemas.refund import RefundCreateRequest, RefundApproveRequest, RefundExecuteRequest, RefundResponse
from backend.app.core.security import get_current_user, require_role
from backend.app.models.enums import UserRole
from backend.app.services.refund_service import create_refund_request, decide_refund_request, execute_refund_intent
from backend.app.database import get_db

router = APIRouter(prefix="/refunds", tags=["Refunds & Returns"])

@router.post("/", response_model=RefundResponse, status_code=status.HTTP_201_CREATED)
def request_refund(
    refund_in: RefundCreateRequest,
    current_user: dict = Depends(get_current_user),
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key")
):
    with get_db() as conn:
        key = idempotency_key or refund_in.idempotency_key
        return create_refund_request(
            conn,
            order_id=refund_in.order_id,
            amount=refund_in.amount,
            reason=refund_in.reason,
            requester_id=current_user["user_id"],
            idempotency_key=key
        )

@router.get("/")
def list_refunds(current_user: dict = Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM refund_requests ORDER BY created_at DESC LIMIT 50")
        return [dict(r) for r in cursor.fetchall()]

@router.post("/{refund_id}/decide", response_model=RefundResponse)
def review_refund(
    refund_id: str,
    decision_in: RefundApproveRequest,
    current_user: dict = Depends(require_role([UserRole.FINANCE_REVIEWER, UserRole.ADMINISTRATOR]))
):
    with get_db() as conn:
        return decide_refund_request(
            conn,
            refund_id=refund_id,
            reviewer=current_user,
            decision=decision_in.decision,
            notes=decision_in.notes
        )

@router.post("/{refund_id}/execute", response_model=RefundResponse)
def execute_refund(
    refund_id: str,
    exec_in: RefundExecuteRequest,
    current_user: dict = Depends(require_role([UserRole.FINANCE_REVIEWER, UserRole.ADMINISTRATOR]))
):
    with get_db() as conn:
        return execute_refund_intent(
            conn,
            refund_id=refund_id,
            caller_id=current_user["user_id"],
            simulate_failure=exec_in.simulate_gateway_failure
        )
