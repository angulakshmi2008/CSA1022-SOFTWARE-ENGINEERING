from pydantic import BaseModel, Field
from typing import List, Optional

class OrderLineCreate(BaseModel):
    sku: str
    quantity: int = Field(gt=0, description="Quantity must be strictly positive")

class OrderCreate(BaseModel):
    items: List[OrderLineCreate] = Field(min_length=1, description="Order must contain at least one line item")
    region_id: Optional[str] = "US-EAST"

class OrderLineResponse(BaseModel):
    line_id: str
    sku: str
    quantity: int
    unit_price: float
    tax_rate: float
    tax_amount: float
    line_total: float

class OrderResponse(BaseModel):
    order_id: str
    owner_id: str
    state: str
    region_id: str
    policy_version: int
    subtotal: float
    tax_amount: float
    shipping_fee: float
    total_amount: float
    dispatch_due_at: Optional[str] = None
    created_at: str
    updated_at: str
    items: Optional[List[OrderLineResponse]] = None
