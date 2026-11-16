import sqlite3
import uuid
from typing import List, Dict, Any
from fastapi import HTTPException, status
from backend.app.models.enums import OrderState
from backend.app.services.inventory_service import consume_order_reservations
from backend.app.services.audit_service import log_audit_event

def get_picker_orders(conn: sqlite3.Connection, picker_region: str) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    # Pickers see only PAID orders with active reservations in their region
    cursor.execute("""
        SELECT o.order_id, o.owner_id, o.state, o.region_id, o.total_amount, o.dispatch_due_at, o.created_at
        FROM orders o
        WHERE o.state = ? AND o.region_id = ?
        ORDER BY o.dispatch_due_at ASC
    """, (OrderState.PAID.value, picker_region))
    orders = cursor.fetchall()
    
    result = []
    for ord_row in orders:
        ord_dict = dict(ord_row)
        cursor.execute("SELECT sku, quantity FROM order_lines WHERE order_id = ?", (ord_dict["order_id"],))
        ord_dict["items"] = [dict(r) for r in cursor.fetchall()]
        result.append(ord_dict)
    return result

def confirm_pick_and_pack(conn: sqlite3.Connection, order_id: str, picker_id: str) -> Dict[str, Any]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
    if order["state"] != OrderState.PAID.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order cannot be picked in state '{order['state']}'. Must be 'PAID'."
        )
        
    consume_order_reservations(conn, order_id)
    cursor.execute("""
        UPDATE orders
        SET state = ?, version = version + 1, updated_at = datetime('now', 'utc')
        WHERE order_id = ?
    """, (OrderState.PACKED.value, order_id))
    
    log_audit_event(
        conn, actor_id=picker_id, action="ORDER_PACKED",
        entity_type="ORDER", entity_id=order_id, old_version=order["version"], new_version=order["version"]+1
    )
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    return dict(cursor.fetchone())

def dispatch_order(conn: sqlite3.Connection, order_id: str, picker_id: str) -> Dict[str, Any]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
    # Crucial Invariant: Dispatch requires confirmed payment and pick confirmation (state PACKED)
    if order["state"] != OrderState.PACKED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lifecycle Guard Violation: Cannot dispatch order in state '{order['state']}'. Must be in 'PACKED' state with confirmed pick."
        )
        
    cursor.execute("""
        UPDATE orders
        SET state = ?, version = version + 1, updated_at = datetime('now', 'utc')
        WHERE order_id = ?
    """, (OrderState.DISPATCHED.value, order_id))
    
    log_audit_event(
        conn, actor_id=picker_id, action="ORDER_DISPATCHED",
        entity_type="ORDER", entity_id=order_id, old_version=order["version"], new_version=order["version"]+1
    )
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    return dict(cursor.fetchone())
