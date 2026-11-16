import sqlite3
from typing import Dict, Any
from backend.app.models.enums import ReservationStatus, OrderState
from backend.app.services.inventory_service import release_order_reservations
from backend.app.services.audit_service import log_audit_event

def expire_unpaid_reservations(conn: sqlite3.Connection) -> Dict[str, Any]:
    cursor = conn.cursor()
    # Find all active reservations whose lease has expired
    cursor.execute("""
        SELECT DISTINCT r.order_id
        FROM reservations r
        JOIN orders o ON r.order_id = o.order_id
        WHERE r.status = ? 
          AND o.state = ?
          AND datetime(r.expires_at) <= datetime('now', 'utc')
    """, (ReservationStatus.ACTIVE.value, OrderState.PLACED.value))
    expired_orders = cursor.fetchall()
    
    reclaimed_orders = 0
    total_reservations_released = 0
    
    for row in expired_orders:
        order_id = row["order_id"]
        count = release_order_reservations(conn, order_id, new_status=ReservationStatus.EXPIRED)
        
        cursor.execute("""
            UPDATE orders
            SET state = ?, version = version + 1, updated_at = datetime('now', 'utc')
            WHERE order_id = ?
        """, (OrderState.CANCELLED.value, order_id))
        
        log_audit_event(
            conn, actor_id="EXPIRY_WORKER", action="ORDER_EXPIRED",
            entity_type="ORDER", entity_id=order_id,
            details={"released_reservations": count}
        )
        reclaimed_orders += 1
        total_reservations_released += count
        
    return {
        "reclaimed_orders": reclaimed_orders,
        "released_reservations": total_reservations_released
    }
