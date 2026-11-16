import sqlite3
import hmac
import hashlib
import uuid
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from fastapi import HTTPException, status
from backend.app.config import settings
from backend.app.models.enums import OrderState, IntentPurpose, IntentStatus, ReservationStatus
from backend.app.services.audit_service import log_audit_event
from backend.app.services.inventory_service import reserve_stock_atomic

def verify_callback_signature(payload_bytes: bytes, signature_header: str) -> bool:
    if not signature_header:
        return False
    expected = hmac.new(settings.GATEWAY_HMAC_SECRET.encode('utf-8'), payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header)

def process_payment_callback(
    conn: sqlite3.Connection,
    gateway_id: str,
    event_id: str,
    order_id: str,
    amount: float,
    currency: str,
    signature: str,
    raw_payload: str
) -> Dict[str, Any]:
    cursor = conn.cursor()
    
    # 1. Check for duplicate callback event using DB uniqueness
    cursor.execute("""
        SELECT event_pk, order_id, amount, status FROM payment_events
        WHERE gateway_id = ? AND event_id = ?
    """, (gateway_id, event_id))
    existing_event = cursor.fetchone()
    if existing_event:
        return {
            "status": "DUPLICATE_ACKNOWLEDGED",
            "message": f"Payment event '{event_id}' from gateway '{gateway_id}' already processed.",
            "order_id": order_id,
            "gateway_id": gateway_id,
            "event_id": event_id,
            "is_duplicate": True
        }
        
    # 2. Retrieve order
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order '{order_id}' not found")
        
    # 3. Match payment amount exactly
    expected_amount = round(float(order["total_amount"]), 2)
    if round(amount, 2) != expected_amount:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Amount mismatch: received {amount}, expected {expected_amount}"
        )
        
    # 4. Record Payment Event (Enforces UNIQUE constraint atomically)
    event_pk = str(uuid.uuid4())
    try:
        cursor.execute("""
            INSERT INTO payment_events (
                event_pk, gateway_id, event_id, order_id, amount, currency, status, signature, verified_at
            ) VALUES (?, ?, ?, ?, ?, ?, 'CAPTURED', ?, datetime('now', 'utc'))
        """, (event_pk, gateway_id, event_id, order_id, amount, currency, signature))
    except sqlite3.IntegrityError:
        # Concurrent collision
        return {
            "status": "DUPLICATE_ACKNOWLEDGED",
            "message": f"Payment event '{event_id}' already processed by concurrent transaction.",
            "order_id": order_id,
            "gateway_id": gateway_id,
            "event_id": event_id,
            "is_duplicate": True
        }
        
    # 5. Check reservation status and handle late payments after expiry (Weakness 1 / Revision)
    cursor.execute("""
        SELECT reservation_id, status FROM reservations
        WHERE order_id = ? AND status = ?
    """, (order_id, ReservationStatus.ACTIVE.value))
    active_res = cursor.fetchall()
    
    dispatch_due = (datetime.now(timezone.utc) + timedelta(hours=settings.DISPATCH_SLA_HOURS)).strftime('%Y-%m-%d %H:%M:%S')
    
    if not active_res:
        # Check if the reservation expired
        cursor.execute("SELECT sku, quantity FROM order_lines WHERE order_id = ?", (order_id,))
        lines = cursor.fetchall()
        items_to_re_reserve = [{"sku": line["sku"], "quantity": line["quantity"]} for line in lines]
        
        try:
            # Attempt to re-reserve stock atomically
            reserve_stock_atomic(conn, order_id, order["region_id"], items_to_re_reserve)
            new_order_state = OrderState.PAID.value
        except HTTPException:
            # Stock is unavailable! Must NOT oversell! Flag as NEEDS_REFUND
            new_order_state = OrderState.NEEDS_REFUND.value
            
            # Automatically create an approval-gated refund request
            refund_id = str(uuid.uuid4())
            idemp_key = f"auto-refund-{order_id}-{event_id}"
            cursor.execute("""
                INSERT INTO refund_requests (
                    refund_id, order_id, amount, state, reason, requested_by, idempotency_key, created_at
                ) VALUES (?, ?, ?, 'REQUESTED', 'Late payment arrived after stock reservation expired and unit resold', ?, ?, datetime('now', 'utc'))
            """, (refund_id, order_id, amount, order["owner_id"], idemp_key))
            
            log_audit_event(
                conn, actor_id="SYSTEM", action="ORDER_NEEDS_REFUND",
                entity_type="ORDER", entity_id=order_id, old_version=order["version"], new_version=order["version"]+1,
                details={"reason": "Late payment after expiry, stock unavailable"}
            )
    else:
        new_order_state = OrderState.PAID.value

    # 6. Update order state and dispatch SLA
    cursor.execute("""
        UPDATE orders
        SET state = ?,
            dispatch_due_at = ?,
            version = version + 1,
            updated_at = datetime('now', 'utc')
        WHERE order_id = ?
    """, (new_order_state, dispatch_due, order_id))
    
    # 7. Insert Transactional Outbox intent if order successfully marked PAID
    if new_order_state == OrderState.PAID.value:
        intent_id = str(uuid.uuid4())
        correlation_key = f"courier-sync-{order_id}"
        outbox_payload = {
            "order_id": order_id,
            "region_id": order["region_id"],
            "owner_id": order["owner_id"],
            "total_amount": amount
        }
        cursor.execute("""
            INSERT INTO outbox_intents (
                intent_id, aggregate_id, purpose, correlation_key, payload_json, status, created_at, next_retry_at
            ) VALUES (?, ?, ?, ?, ?, ?, datetime('now', 'utc'), datetime('now', 'utc'))
        """, (intent_id, order_id, IntentPurpose.COURIER_DISPATCH.value, correlation_key, json.dumps(outbox_payload), IntentStatus.PENDING.value))
        
        log_audit_event(
            conn, actor_id="SYSTEM_WEBHOOK", action="ORDER_PAID",
            entity_type="ORDER", entity_id=order_id, old_version=order["version"], new_version=order["version"]+1,
            details={"gateway_id": gateway_id, "event_id": event_id, "amount": amount}
        )
        
    return {
        "status": "PAYMENT_CONFIRMED",
        "message": f"Payment of {amount} {currency} successfully recorded for order {order_id}. State: {new_order_state}.",
        "order_id": order_id,
        "gateway_id": gateway_id,
        "event_id": event_id,
        "is_duplicate": False
    }
