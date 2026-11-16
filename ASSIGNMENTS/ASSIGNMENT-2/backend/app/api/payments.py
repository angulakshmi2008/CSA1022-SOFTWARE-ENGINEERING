from fastapi import APIRouter, Header, Request, HTTPException, status
from backend.app.schemas.payment import PaymentCallbackRequest, PaymentResponse
from backend.app.services.payment_service import verify_callback_signature, process_payment_callback
from backend.app.database import get_db

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/callback", response_model=PaymentResponse)
async def payment_gateway_callback(request: Request, x_signature: str = Header(None, alias="X-Signature")):
    body_bytes = await request.body()
    
    # 1. Signature Verification Guard
    if not verify_callback_signature(body_bytes, x_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid HMAC-SHA256 signature in X-Signature header"
        )
        
    data = await request.json()
    callback_in = PaymentCallbackRequest(**data)
    
    with get_db() as conn:
        result = process_payment_callback(
            conn=conn,
            gateway_id=callback_in.gateway_id,
            event_id=callback_in.event_id,
            order_id=callback_in.order_id,
            amount=callback_in.amount,
            currency=callback_in.currency,
            signature=x_signature,
            raw_payload=body_bytes.decode('utf-8')
        )
        return PaymentResponse(**result)
