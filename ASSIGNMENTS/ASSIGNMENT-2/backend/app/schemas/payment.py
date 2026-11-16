from pydantic import BaseModel
from typing import Optional

class PaymentCallbackRequest(BaseModel):
    gateway_id: str
    event_id: str
    order_id: str
    amount: float
    currency: str = "USD"
    status: str = "CAPTURED"

class PaymentResponse(BaseModel):
    status: str
    message: str
    order_id: str
    gateway_id: str
    event_id: str
    is_duplicate: bool = False
