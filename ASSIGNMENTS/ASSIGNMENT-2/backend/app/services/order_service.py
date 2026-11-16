import sqlite3
import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from backend.app.models.enums import OrderState, UserRole
from backend.app.services.pricing_service import calculate_order_pricing
from backend.app.services.inventory_service import reserve_stock_atomic, release_order_reservations
from backend.app.services.audit_service import log_audit_event
from backend.app.config import settings

def create_order(conn: sqlite3.Connection, user_id: str, items: List[Dict[str, Any]], region_id: str = "US-EAST") -> Dict[str, Any]:
    pricing = calculate_order_pricing(conn, items, region_id)
    order_id = str(uuid.uuid4())
    cursor = conn.cursor()
    
    # 1. Insert Order record
    cursor.execute("""
        INSERT INTO orders (
            order_id, owner_id, state, region_id, policy_version,
            subtotal, tax_amount, shipping_fee, total_amount,
            version, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, datetime('now', 'utc'), datetime('now', 'utc'))
    """, (
        order_id, user_id, OrderState.PLACED.value, region_id, pricing["policy_version"],
        pricing["subtotal"], pricing["tax_amount"], pricing["shipping_fee"], pricing["total_amount"]
    ))
    
    # 2. Insert Order Lines
    for line in pricing["lines"]:
        line_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO order_lines (
                line_id, order_id, sku, quantity, unit_price, tax_rate, tax_amount, line_total
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            line_id, order_id, line["sku"], line["quantity"], line["unit_price"],
            line["tax_rate"], line["tax_amount"], line["line_total"]
        ))
        
    # 3. Reserve Stock Atomically (Throws HTTP 409 if unavailable)
    reserve_stock_atomic(conn, order_id, region_id, items)
    
    # 4. Append Audit Event
    log_audit_event(
        conn, actor_id=user_id, action="ORDER_PLACED",
        entity_type="ORDER", entity_id=order_id, old_version=None, new_version=1,
        details={"total": pricing["total_amount"], "region": region_id}
    )
    
    return get_order_details(conn, order_id, user_id, is_staff=False)

def get_order_details(conn: sqlite3.Connection, order_id: str, caller_id: str, is_staff: bool = False) -> Dict[str, Any]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order '{order_id}' not found")
        
    # Strict customer isolation guard
    if not is_staff and order["owner_id"] != caller_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You are not authorized to view another customer's order."
        )
        
    cursor.execute("SELECT * FROM order_lines WHERE order_id = ?", (order_id,))
    lines = cursor.fetchall()
    
    order_dict = dict(order)
    order_dict["items"] = [dict(line) for line in lines]
    return order_dict

def cancel_order(conn: sqlite3.Connection, order_id: str, caller_id: str) -> Dict[str, Any]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if order["owner_id"] != caller_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot cancel another customer's order")
        
    # Pre-payment cancellation rule
    if order["state"] != OrderState.PLACED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order cannot be cancelled in state '{order['state']}'. Cancellation is only allowed before payment."
        )
        
    release_order_reservations(conn, order_id)
    cursor.execute("""
        UPDATE orders
        SET state = ?, version = version + 1, updated_at = datetime('now', 'utc')
        WHERE order_id = ?
    """, (OrderState.CANCELLED.value, order_id))
    
    log_audit_event(
        conn, actor_id=caller_id, action="ORDER_CANCELLED",
        entity_type="ORDER", entity_id=order_id, old_version=order["version"], new_version=order["version"]+1
    )
    return get_order_details(conn, order_id, caller_id)
