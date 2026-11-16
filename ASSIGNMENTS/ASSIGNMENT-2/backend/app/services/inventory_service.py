import sqlite3
import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
from fastapi import HTTPException, status
from backend.app.config import settings
from backend.app.models.enums import ReservationStatus

def reserve_stock_atomic(conn: sqlite3.Connection, order_id: str, region_id: str, items: List[Dict[str, Any]]) -> List[str]:
    cursor = conn.cursor()
    expires_at = (datetime.now(timezone.utc) + timedelta(minutes=settings.RESERVATION_LEASE_MINUTES)).strftime('%Y-%m-%d %H:%M:%S')
    reservation_ids = []
    
    for item in items:
        sku = item["sku"]
        qty = item["quantity"]
        
        # Atomic conditional update enforcing non-negative available stock
        cursor.execute("""
            UPDATE stock_items
            SET reserved = reserved + ?,
                version = version + 1,
                updated_at = datetime('now', 'utc')
            WHERE sku = ? AND region_id = ? AND (on_hand - reserved) >= ?
        """, (qty, sku, region_id, qty))
        
        if cursor.rowcount == 0:
            cursor.execute("SELECT on_hand, reserved FROM stock_items WHERE sku = ? AND region_id = ?", (sku, region_id))
            row = cursor.fetchone()
            available = (row["on_hand"] - row["reserved"]) if row else 0
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Insufficient available stock for SKU '{sku}' in region '{region_id}'. Available: {available}, Requested: {qty}"
            )
            
        res_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO reservations (
                reservation_id, order_id, sku, region_id, quantity, expires_at, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now', 'utc'))
        """, (res_id, order_id, sku, region_id, qty, expires_at, ReservationStatus.ACTIVE.value))
        reservation_ids.append(res_id)
        
    return reservation_ids

def release_order_reservations(conn: sqlite3.Connection, order_id: str, new_status: ReservationStatus = ReservationStatus.RELEASED) -> int:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT reservation_id, sku, region_id, quantity, status
        FROM reservations
        WHERE order_id = ? AND status = ?
    """, (order_id, ReservationStatus.ACTIVE.value))
    active_reservations = cursor.fetchall()
    
    released_count = 0
    for res in active_reservations:
        qty = res["quantity"]
        sku = res["sku"]
        region_id = res["region_id"]
        
        cursor.execute("""
            UPDATE stock_items
            SET reserved = MAX(0, reserved - ?),
                version = version + 1,
                updated_at = datetime('now', 'utc')
            WHERE sku = ? AND region_id = ?
        """, (qty, sku, region_id))
        
        cursor.execute("""
            UPDATE reservations
            SET status = ?
            WHERE reservation_id = ?
        """, (new_status.value, res["reservation_id"]))
        released_count += 1
        
    return released_count

def consume_order_reservations(conn: sqlite3.Connection, order_id: str) -> int:
    """When order is packed/dispatched, convert reserved to permanently deducted on_hand."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT reservation_id, sku, region_id, quantity
        FROM reservations
        WHERE order_id = ? AND status = ?
    """, (order_id, ReservationStatus.ACTIVE.value))
    active_reservations = cursor.fetchall()
    
    for res in active_reservations:
        qty = res["quantity"]
        sku = res["sku"]
        region_id = res["region_id"]
        
        cursor.execute("""
            UPDATE stock_items
            SET on_hand = MAX(0, on_hand - ?),
                reserved = MAX(0, reserved - ?),
                version = version + 1,
                updated_at = datetime('now', 'utc')
            WHERE sku = ? AND region_id = ?
        """, (qty, qty, sku, region_id))
        
        cursor.execute("""
            UPDATE reservations
            SET status = ?
            WHERE reservation_id = ?
        """, (ReservationStatus.CONSUMED.value, res["reservation_id"]))
        
    return len(active_reservations)
