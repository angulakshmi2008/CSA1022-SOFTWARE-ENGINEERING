from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from backend.app.schemas.order import OrderCreate, OrderResponse
from backend.app.core.security import get_current_user, require_role
from backend.app.models.enums import UserRole
from backend.app.services.order_service import create_order, get_order_details, cancel_order
from backend.app.database import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def place_order(order_in: OrderCreate, current_user: dict = Depends(get_current_user)):
    with get_db() as conn:
        items = [{"sku": it.sku, "quantity": it.quantity} for it in order_in.items]
        return create_order(conn, user_id=current_user["user_id"], items=items, region_id=order_in.region_id or current_user.get("region_id", "US-EAST"))

@router.get("/")
def list_orders(current_user: dict = Depends(get_current_user), region_id: Optional[str] = None):
    with get_db() as conn:
        cursor = conn.cursor()
        role = current_user["role"]
        
        # Customers only see their own orders
        if role == UserRole.CUSTOMER.value:
            cursor.execute("SELECT * FROM orders WHERE owner_id = ? ORDER BY created_at DESC", (current_user["user_id"],))
        else:
            # Staff can filter by region
            if region_id:
                cursor.execute("SELECT * FROM orders WHERE region_id = ? ORDER BY created_at DESC", (region_id,))
            else:
                cursor.execute("SELECT * FROM orders ORDER BY created_at DESC LIMIT 50")
                
        orders = [dict(r) for r in cursor.fetchall()]
        return orders

@router.get("/{order_id}")
def get_order(order_id: str, current_user: dict = Depends(get_current_user)):
    is_staff = current_user["role"] in [
        UserRole.SUPPORT_AGENT.value, UserRole.FINANCE_REVIEWER.value,
        UserRole.STORE_MANAGER.value, UserRole.ADMINISTRATOR.value
    ]
    with get_db() as conn:
        return get_order_details(conn, order_id=order_id, caller_id=current_user["user_id"], is_staff=is_staff)

@router.post("/{order_id}/cancel")
def cancel_customer_order(order_id: str, current_user: dict = Depends(get_current_user)):
    with get_db() as conn:
        return cancel_order(conn, order_id=order_id, caller_id=current_user["user_id"])
