import sqlite3
import uuid
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
from backend.app.models.enums import RefundState, UserRole, IntentPurpose, IntentStatus
from backend.app.services.audit_service import log_audit_event
from backend.app.services.pricing_service import get_active_policy

def create_refund_request(
    conn: sqlite3.Connection,
    order_id: str,
    amount: float,
    reason: str,
    requester_id: str,
    idempotency_key: Optional[str] = None
) -> Dict[str, Any]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
    idemp_key = idempotency_key or str(uuid.uuid4())
    cursor.execute("SELECT * FROM refund_requests WHERE idempotency_key = ?", (idemp_key,))
    existing = cursor.fetchone()
    if existing:
        return dict(existing)
        
    refund_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO refund_requests (
            refund_id, order_id, amount, state, reason, requested_by, idempotency_key, version, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 1, datetime('now', 'utc'))
    """, (refund_id, order_id, amount, RefundState.REQUESTED.value, reason, requester_id, idemp_key))
    
    log_audit_event(
        conn, actor_id=requester_id, action="REFUND_REQUESTED",
        entity_type="REFUND", entity_id=refund_id, old_version=None, new_version=1,
        details={"order_id": order_id, "amount": amount, "reason": reason}
    )
    
    cursor.execute("SELECT * FROM refund_requests WHERE refund_id = ?", (refund_id,))
    return dict(cursor.fetchone())

def decide_refund_request(
    conn: sqlite3.Connection,
    refund_id: str,
    reviewer: Dict[str, Any],
    decision: str,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM refund_requests WHERE refund_id = ?", (refund_id,))
    refund = cursor.fetchone()
    if not refund:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Refund request not found")
        
    if refund["state"] != RefundState.REQUESTED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Refund request is in state '{refund['state']}' and cannot be decided upon."
        )
        
    # Four-Eyes Principle Guard: Requester cannot approve their own refund
    if refund["requested_by"] == reviewer["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Four-Eyes Governance Violation: The requester cannot approve their own refund request."
        )
        
    cursor.execute("SELECT region_id FROM orders WHERE order_id = ?", (refund["order_id"],))
    order_row = cursor.fetchone()
    region_id = order_row["region_id"] if order_row else "US-EAST"
    policy = get_active_policy(conn, region_id)
    threshold = float(policy["refund_approval_threshold"])
    
    amount = float(refund["amount"])
    # If amount exceeds threshold, caller MUST be a FINANCE_REVIEWER
    if amount > threshold and reviewer["role"] != UserRole.FINANCE_REVIEWER.value and reviewer["role"] != UserRole.ADMINISTRATOR.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Approval threshold exceeded (${amount:.2f} > ${threshold:.2f}). Only Finance Reviewers can approve this refund."
        )
        
    new_state = RefundState.APPROVED.value if decision.upper() == "APPROVE" else RefundState.REJECTED.value
    cursor.execute("""
        UPDATE refund_requests
        SET state = ?, approved_by = ?, version = version + 1, resolved_at = datetime('now', 'utc')
        WHERE refund_id = ?
    """, (new_state, reviewer["user_id"], refund_id))
    
    log_audit_event(
        conn, actor_id=reviewer["user_id"], action=f"REFUND_{new_state}",
        entity_type="REFUND", entity_id=refund_id, old_version=refund["version"], new_version=refund["version"]+1,
        details={"notes": notes, "reviewer_role": reviewer["role"]}
    )
    
    cursor.execute("SELECT * FROM refund_requests WHERE refund_id = ?", (refund_id,))
    return dict(cursor.fetchone())

def execute_refund_intent(
    conn: sqlite3.Connection,
    refund_id: str,
    caller_id: str,
    simulate_failure: bool = False
) -> Dict[str, Any]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM refund_requests WHERE refund_id = ?", (refund_id,))
    refund = cursor.fetchone()
    if not refund:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Refund request not found")
        
    # Crucial Invariant: Refund CANNOT execute without APPROVED state (or FAILED retry)
    if refund["state"] not in [RefundState.APPROVED.value, RefundState.FAILED.value]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot execute refund in state '{refund['state']}'. Prior finance approval is mandatory."
        )
        
    if simulate_failure:
        # Gateway failure simulation: keep approval, transition to FAILED for controlled retry
        cursor.execute("""
            UPDATE refund_requests
            SET state = ?, failure_reason = ?, version = version + 1, resolved_at = datetime('now', 'utc')
            WHERE refund_id = ?
        """, (RefundState.FAILED.value, "Simulated gateway connection timeout (504)", refund_id))
        
        log_audit_event(
            conn, actor_id=caller_id, action="REFUND_EXECUTION_FAILED",
            entity_type="REFUND", entity_id=refund_id, old_version=refund["version"], new_version=refund["version"]+1,
            details={"error": "Gateway timeout", "approval_retained": refund["approved_by"]}
        )
        cursor.execute("SELECT * FROM refund_requests WHERE refund_id = ?", (refund_id,))
        return dict(cursor.fetchone())
        
    # Execution Success
    cursor.execute("""
        UPDATE refund_requests
        SET state = ?, failure_reason = NULL, version = version + 1, resolved_at = datetime('now', 'utc')
        WHERE refund_id = ?
    """, (RefundState.EXECUTED.value, refund_id))
    
    # Update order state to CLOSED if appropriate
    cursor.execute("""
        UPDATE orders
        SET state = 'CLOSED', version = version + 1, updated_at = datetime('now', 'utc')
        WHERE order_id = ?
    """, (refund["order_id"],))
    
    log_audit_event(
        conn, actor_id=caller_id, action="REFUND_EXECUTED",
        entity_type="REFUND", entity_id=refund_id, old_version=refund["version"], new_version=refund["version"]+1,
        details={"amount": refund["amount"], "idempotency_key": refund["idempotency_key"]}
    )
    cursor.execute("SELECT * FROM refund_requests WHERE refund_id = ?", (refund_id,))
    return dict(cursor.fetchone())
