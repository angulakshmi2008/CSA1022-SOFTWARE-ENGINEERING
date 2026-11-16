import sqlite3
import uuid
import json
from datetime import datetime, timezone
from typing import Optional, Any

def log_audit_event(
    conn: sqlite3.Connection,
    actor_id: str,
    action: str,
    entity_type: str,
    entity_id: str,
    old_version: Optional[int] = None,
    new_version: Optional[int] = None,
    details: Optional[Any] = None
) -> str:
    event_id = str(uuid.uuid4())
    details_str = json.dumps(details) if details is not None else None
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audit_events (
            event_id, actor_id, action, entity_type, entity_id, old_version, new_version, details_json, occurred_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'utc'))
    """, (event_id, actor_id, action, entity_type, entity_id, old_version, new_version, details_str))
    return event_id
