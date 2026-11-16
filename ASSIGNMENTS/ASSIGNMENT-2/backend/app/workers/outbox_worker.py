import sqlite3
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List
from backend.app.models.enums import IntentStatus, IntentPurpose
from backend.app.integrations.courier.mock_courier import MockCourierAPI
from backend.app.services.audit_service import log_audit_event

def process_pending_outbox_intents(
    conn: sqlite3.Connection,
    batch_size: int = 10,
    simulate_courier_timeout: bool = False,
    target_order_id: str = None
) -> Dict[str, Any]:
    cursor = conn.cursor()
    query = """
        SELECT intent_id, aggregate_id, purpose, correlation_key, payload_json, attempts, max_attempts
        FROM outbox_intents
        WHERE status = ? AND datetime(next_retry_at) <= datetime('now', 'utc')
    """
    params = [IntentStatus.PENDING.value]
    if target_order_id:
        query += " AND aggregate_id = ?"
        params.append(target_order_id)
        
    query += " ORDER BY created_at ASC LIMIT ?"
    params.append(batch_size)
    cursor.execute(query, params)
    intents = cursor.fetchall()
    
    processed = 0
    succeeded = 0
    failed = 0
    
    for row in intents:
        intent_id = row["intent_id"]
        purpose = row["purpose"]
        correlation_key = row["correlation_key"]
        attempts = row["attempts"] + 1
        payload = json.loads(row["payload_json"])
        
        if purpose == IntentPurpose.COURIER_DISPATCH.value:
            try:
                # 1. Reconcile with carrier API first to avoid duplicate bookings
                existing_carrier_booking = MockCourierAPI.get_shipment_by_correlation_key(correlation_key)
                if existing_carrier_booking:
                    tracking_no = existing_carrier_booking["tracking_number"]
                else:
                    res = MockCourierAPI.register_shipment(
                        correlation_key, payload, simulate_timeout=simulate_courier_timeout
                    )
                    tracking_no = res["tracking_number"]
                    
                cursor.execute("""
                    UPDATE outbox_intents
                    SET status = ?, external_reference = ?, attempts = ?, updated_at = datetime('now', 'utc')
                    WHERE intent_id = ?
                """, (IntentStatus.COMPLETED.value, tracking_no, attempts, intent_id))
                
                log_audit_event(
                    conn, actor_id="OUTBOX_WORKER", action="COURIER_INTENT_COMPLETED",
                    entity_type="OUTBOX", entity_id=intent_id,
                    details={"order_id": row["aggregate_id"], "tracking_number": tracking_no}
                )
                succeeded += 1
            except Exception as e:
                # Controlled retry with exponential backoff
                backoff_seconds = min(3600, 2 ** attempts)
                next_retry = (datetime.now(timezone.utc) + timedelta(seconds=backoff_seconds)).strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("""
                    UPDATE outbox_intents
                    SET attempts = ?, next_retry_at = ?, updated_at = datetime('now', 'utc')
                    WHERE intent_id = ?
                """, (attempts, next_retry, intent_id))
                failed += 1
                
        processed += 1
        
    return {
        "processed": processed,
        "succeeded": succeeded,
        "failed": failed
    }
