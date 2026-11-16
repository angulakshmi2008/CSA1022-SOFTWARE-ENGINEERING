from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Role(str, Enum):
    CUSTOMER = "CUSTOMER"
    WAREHOUSE_PICKER = "WAREHOUSE_PICKER"
    SUPPORT_AGENT = "SUPPORT_AGENT"
    FINANCE_REVIEWER = "FINANCE_REVIEWER"
    STORE_MANAGER = "STORE_MANAGER"
    ADMINISTRATOR = "ADMINISTRATOR"
    DEVOPS_ENGINEER = "DEVOPS_ENGINEER"

class OrderStatus(str, Enum):
    CREATED = "CREATED"
    RESERVED = "RESERVED"
    PAID = "PAID"
    PICKING = "PICKING"
    PICKED = "PICKED"
    DISPATCHED = "DISPATCHED"
    DELIVERED = "DELIVERED"
    RETURN_REQUESTED = "RETURN_REQUESTED"
    REFUND_PENDING = "REFUND_PENDING"
    REFUNDED = "REFUNDED"
    CANCELLED = "CANCELLED"

# Permitted public customer-facing tracking milestones
PUBLIC_MILESTONES = [
    OrderStatus.PAID,
    OrderStatus.PICKED,
    OrderStatus.DISPATCHED,
    OrderStatus.DELIVERED,
    OrderStatus.REFUNDED
]

# Valid state machine transitions
VALID_TRANSITIONS: Dict[OrderStatus, List[OrderStatus]] = {
    OrderStatus.CREATED: [OrderStatus.RESERVED, OrderStatus.CANCELLED],
    OrderStatus.RESERVED: [OrderStatus.PAID, OrderStatus.CANCELLED],
    OrderStatus.PAID: [OrderStatus.PICKING, OrderStatus.CANCELLED],
    OrderStatus.PICKING: [OrderStatus.PICKED, OrderStatus.CANCELLED],
    OrderStatus.PICKED: [OrderStatus.DISPATCHED],
    OrderStatus.DISPATCHED: [OrderStatus.DELIVERED],
    OrderStatus.DELIVERED: [OrderStatus.RETURN_REQUESTED],
    OrderStatus.RETURN_REQUESTED: [OrderStatus.REFUND_PENDING, OrderStatus.DELIVERED],
    OrderStatus.REFUND_PENDING: [OrderStatus.REFUNDED, OrderStatus.DELIVERED],
    OrderStatus.REFUNDED: [],
    OrderStatus.CANCELLED: []
}

@dataclass
class Product:
    sku: str
    name: str
    category: str
    price: float
    stock_quantity: int
    low_stock_threshold: int
    barcode: str

@dataclass
class OrderItem:
    sku: str
    quantity: int
    unit_price: float

@dataclass
class Order:
    order_id: str
    customer_id: str
    customer_email: str
    region_code: str
    warehouse_id: str
    items: List[OrderItem]
    subtotal: float
    tax_amount: float
    shipping_amount: float
    total_amount: float
    status: OrderStatus
    created_at: str
    updated_at: str
    delivered_at: Optional[str] = None
    tracking_number: Optional[str] = None
    return_reason: Optional[str] = None

@dataclass
class Reservation:
    reservation_id: str
    order_id: str
    sku: str
    quantity: int
    status: str  # ACTIVE, RELEASED, CONFIRMED
    expires_at: str
    created_at: str

@dataclass
class PaymentIntent:
    intent_id: str
    order_id: str
    idempotency_key: str
    amount: float
    status: str  # PENDING, SUCCESS, FAILED, REFUNDED
    gateway_transaction_id: str
    created_at: str

@dataclass
class AuditRecord:
    audit_id: str
    entity_type: str
    entity_id: str
    actor_id: str
    actor_role: str
    action: str
    from_state: Optional[str]
    to_state: Optional[str]
    timestamp: str
    details: str
