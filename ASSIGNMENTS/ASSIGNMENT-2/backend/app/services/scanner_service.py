import sqlite3
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any
from backend.app.schemas.scanner import ScannerEventItem
from backend.app.services.audit_service import log_audit_event

def sync_scanner_batch(conn: sqlite3.Connection, events: List[ScannerEventItem], caller_id: str) -> Dict[str, Any]:
    cursor = conn.cursor()
    received_count = len(events)
    processed_count = 0
    duplicate_count = 0
    stale_count = 0
    
    current_time = datetime.now(timezone.utc)
    
    for ev in events:
        # Check if observation is older than 24 hours (stale check)
        try:
            obs_dt = datetime.fromisoformat(ev.observation_time.replace("Z", "+00:00"))
            is_stale = 1 if (current_time - obs_dt).total_seconds() > 86400 else 0
        except Exception:
            is_stale = 0
            
        if is_stale:
            stale_count += 1
            
        log_id = str(uuid.uuid4())
        try:
            cursor.execute("""
                INSERT INTO scanner_event_logs (
                    log_id, node_id, event_id, sku, region_id, event_type, quantity, observation_time, schema_version, is_stale, received_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'utc'))
            """, (log_id, ev.node_id, ev.event_id, ev.sku, ev.region_id, ev.event_type, ev.quantity, ev.observation_time, ev.schema_version, is_stale))
        except sqlite3.IntegrityError:
            # Duplicate (node_id, event_id)
            duplicate_count += 1
            continue
            
        # Apply stock movement if valid and not stale count
        if ev.event_type == "RECEIVE" and not is_stale:
            cursor.execute("""
                UPDATE stock_items
                SET on_hand = on_hand + ?, version = version + 1, updated_at = datetime('now', 'utc')
                WHERE sku = ? AND region_id = ?
            """, (ev.quantity, ev.sku, ev.region_id))
            
        processed_count += 1
        
    log_audit_event(
        conn, actor_id=caller_id, action="SCANNER_BATCH_SYNC",
        entity_type="SCANNER", entity_id=events[0].node_id if events else "UNKNOWN",
        details={"received": received_count, "processed": processed_count, "duplicates": duplicate_count}
    )
    
    return {
        "received_count": received_count,
        "processed_count": processed_count,
        "duplicate_count": duplicate_count,
        "stale_count": stale_count,
        "message": f"Successfully ingested batch. Processed: {processed_count}, Duplicates ignored: {duplicate_count}, Stale: {stale_count}"
    }
