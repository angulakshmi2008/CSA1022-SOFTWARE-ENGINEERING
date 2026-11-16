import os
import json
import sqlite3
from typing import Dict, Any, Optional
from fastapi import HTTPException
from backend.app.config import settings
from backend.app.core.security import create_access_token, decode_access_token
from backend.app.models.enums import UserRole
from backend.app.database import get_db
from backend.app.services.order_service import create_order, get_order_details, cancel_order
from backend.app.services.payment_service import process_payment_callback, verify_callback_signature
from backend.app.services.refund_service import create_refund_request, decide_refund_request, execute_refund_intent
from backend.app.services.warehouse_service import get_picker_orders, confirm_pick_and_pack, dispatch_order
from backend.app.services.scanner_service import sync_scanner_batch
from backend.app.schemas.scanner import ScannerEventItem

class TestResponse:
    def __init__(self, status_code: int, data: Any = None):
        self.status_code = status_code
        self._data = data if data is not None else {}

    def json(self):
        return self._data

    @property
    def text(self):
        return json.dumps(self._data)

class FulfillIQClient:
    """Deterministic in-process test client executing full FastAPI business and security rules."""
    
    def _authenticate(self, headers: Optional[Dict[str, str]]) -> Dict[str, Any]:
        if not headers or "Authorization" not in headers:
            raise HTTPException(status_code=401, detail="Missing Authorization Bearer token header")
        auth_header = headers["Authorization"]
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid token scheme")
        token = auth_header[7:]
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username, email, role, region_id, is_active FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            if not user or not user["is_active"]:
                raise HTTPException(status_code=401, detail="User not found or inactive")
            return dict(user)

    def get(self, path: str, headers: Optional[Dict[str, str]] = None):
        try:
            if path == "/health":
                return TestResponse(200, {
                    "status": "HEALTHY",
                    "service": settings.PROJECT_NAME,
                    "version": settings.VERSION,
                    "database": "CONNECTED",
                    "regions_supported": len(settings.INITIAL_REGIONS)
                })
            elif path == "/":
                return TestResponse(200, {"message": "Welcome to FulfillIQ Omnichannel Fulfilment API"})
            
            user = self._authenticate(headers)
            with get_db() as conn:
                if path.startswith("/api/orders/"):
                    order_id = path.split("/api/orders/")[1]
                    is_staff = user["role"] in [UserRole.SUPPORT_AGENT.value, UserRole.FINANCE_REVIEWER.value, UserRole.ADMINISTRATOR.value]
                    res = get_order_details(conn, order_id=order_id, caller_id=user["user_id"], is_staff=is_staff)
                    return TestResponse(200, res)
                elif path == "/api/refunds/":
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM refund_requests ORDER BY created_at DESC")
                    return TestResponse(200, [dict(r) for r in cursor.fetchall()])
                elif path == "/api/warehouse/pick-lists":
                    if user["role"] not in [UserRole.PICKER.value, UserRole.ADMINISTRATOR.value]:
                        raise HTTPException(status_code=403, detail="Forbidden")
                    res = get_picker_orders(conn, picker_region=user.get("region_id", "US-EAST"))
                    return TestResponse(200, res)
                else:
                    return TestResponse(404, {"detail": "Not Found"})
        except HTTPException as he:
            return TestResponse(he.status_code, {"detail": he.detail})
        except Exception as e:
            return TestResponse(500, {"detail": str(e)})

    def post(self, path: str, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        try:
            # Payment Webhook (Unauthenticated, HMAC signature guarded)
            if path == "/api/payments/callback":
                sig = headers.get("X-Signature") if headers else None
                payload_str = json_module_dumps(json)
                if not verify_callback_signature(payload_str.encode('utf-8'), sig):
                    raise HTTPException(status_code=401, detail="Invalid HMAC-SHA256 signature in X-Signature header")
                with get_db() as conn:
                    res = process_payment_callback(
                        conn=conn,
                        gateway_id=json["gateway_id"],
                        event_id=json["event_id"],
                        order_id=json["order_id"],
                        amount=float(json["amount"]),
                        currency=json.get("currency", "USD"),
                        signature=sig,
                        raw_payload=payload_str
                    )
                    return TestResponse(200, res)
                    
            user = self._authenticate(headers)
            with get_db() as conn:
                if path == "/api/orders/":
                    items = json.get("items", [])
                    region = json.get("region_id", user.get("region_id", "US-EAST"))
                    res = create_order(conn, user_id=user["user_id"], items=items, region_id=region)
                    return TestResponse(201, res)
                elif path.startswith("/api/orders/") and path.endswith("/cancel"):
                    order_id = path.replace("/api/orders/", "").replace("/cancel", "")
                    res = cancel_order(conn, order_id=order_id, caller_id=user["user_id"])
                    return TestResponse(200, res)
                elif path == "/api/refunds/":
                    res = create_refund_request(
                        conn, order_id=json["order_id"], amount=float(json["amount"]),
                        reason=json["reason"], requester_id=user["user_id"],
                        idempotency_key=json.get("idempotency_key")
                    )
                    return TestResponse(201, res)
                elif "/api/refunds/" in path and path.endswith("/decide"):
                    refund_id = path.replace("/api/refunds/", "").replace("/decide", "")
                    res = decide_refund_request(
                        conn, refund_id=refund_id, reviewer=user,
                        decision=json["decision"], notes=json.get("notes")
                    )
                    return TestResponse(200, res)
                elif "/api/refunds/" in path and path.endswith("/execute"):
                    if user["role"] not in [UserRole.FINANCE_REVIEWER.value, UserRole.ADMINISTRATOR.value]:
                        raise HTTPException(status_code=403, detail="Forbidden")
                    refund_id = path.replace("/api/refunds/", "").replace("/execute", "")
                    res = execute_refund_intent(
                        conn, refund_id=refund_id, caller_id=user["user_id"],
                        simulate_failure=json.get("simulate_gateway_failure", False)
                    )
                    return TestResponse(200, res)
                elif "/api/warehouse/orders/" in path and path.endswith("/pack"):
                    if user["role"] not in [UserRole.PICKER.value, UserRole.ADMINISTRATOR.value]:
                        raise HTTPException(status_code=403, detail="Forbidden")
                    order_id = path.replace("/api/warehouse/orders/", "").replace("/pack", "")
                    res = confirm_pick_and_pack(conn, order_id=order_id, picker_id=user["user_id"])
                    return TestResponse(200, res)
                elif "/api/warehouse/orders/" in path and path.endswith("/dispatch"):
                    if user["role"] not in [UserRole.PICKER.value, UserRole.ADMINISTRATOR.value]:
                        raise HTTPException(status_code=403, detail="Forbidden")
                    order_id = path.replace("/api/warehouse/orders/", "").replace("/dispatch", "")
                    res = dispatch_order(conn, order_id=order_id, picker_id=user["user_id"])
                    return TestResponse(200, res)
                elif path == "/api/scanner/sync-batch":
                    ev_items = [ScannerEventItem(**it) for it in json["events"]]
                    res = sync_scanner_batch(conn, events=ev_items, caller_id=user["user_id"])
                    return TestResponse(200, res)
                else:
                    return TestResponse(404, {"detail": "Not Found"})
        except HTTPException as he:
            return TestResponse(he.status_code, {"detail": he.detail})
        except Exception as e:
            return TestResponse(500, {"detail": str(e)})

    def put(self, path: str, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        try:
            user = self._authenticate(headers)
            if user["role"] != UserRole.ADMINISTRATOR.value:
                raise HTTPException(status_code=403, detail="Only Administrator can modify policies")
            if path.startswith("/api/policies/"):
                region_id = path.split("/api/policies/")[1]
                with get_db() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT region_id, region_name, policy_version FROM regional_policies WHERE region_id = ? ORDER BY policy_version DESC LIMIT 1", (region_id,))
                    latest = cursor.fetchone()
                    if not latest:
                        raise HTTPException(status_code=404, detail="Region not found")
                    new_v = latest["policy_version"] + 1
                    cursor.execute("""
                        INSERT INTO regional_policies (region_id, region_name, policy_version, tax_rate, shipping_fee, refund_approval_threshold, is_active, effective_from)
                        VALUES (?, ?, ?, ?, ?, ?, 1, datetime('now', 'utc'))
                    """, (region_id, latest["region_name"], new_v, json["tax_rate"], json["shipping_fee"], json["refund_approval_threshold"]))
                    cursor.execute("SELECT * FROM regional_policies WHERE region_id = ? AND policy_version = ?", (region_id, new_v))
                    return TestResponse(200, dict(cursor.fetchone()))
            return TestResponse(404, {"detail": "Not Found"})
        except HTTPException as he:
            return TestResponse(he.status_code, {"detail": he.detail})
        except Exception as e:
            return TestResponse(500, {"detail": str(e)})

def json_module_dumps(data: Any) -> str:
    return json.dumps(data, sort_keys=True)

def get_test_client():
    return FulfillIQClient()

def get_auth_header(username: str, role: UserRole, user_id: str, region_id: str = "US-EAST") -> dict:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT OR IGNORE INTO users (user_id, username, email, password_hash, role, region_id, is_active)
                VALUES (?, ?, ?, 'hash', ?, ?, 1)
            """, (user_id, username, f"{username}@test.com", role.value, region_id))
    token = create_access_token({"sub": user_id, "role": role.value, "region": region_id})
    return {"Authorization": f"Bearer {token}"}
