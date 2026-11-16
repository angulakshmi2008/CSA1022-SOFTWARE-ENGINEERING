import hmac
import hashlib
import json
import uuid
from typing import Dict, Any
from backend.app.config import settings

class MockPaymentGateway:
    """Simulates external payment gateway webhook signing and refund APIs."""
    
    @staticmethod
    def generate_signed_callback_payload(order_id: str, amount: float, event_id: str = None) -> Dict[str, Any]:
        evt_id = event_id or f"evt_{uuid.uuid4().hex[:12]}"
        payload = {
            "gateway_id": "STRIPE_SANDBOX",
            "event_id": evt_id,
            "order_id": order_id,
            "amount": round(amount, 2),
            "currency": "USD",
            "status": "CAPTURED"
        }
        payload_bytes = json.dumps(payload, sort_keys=True).encode('utf-8')
        signature = hmac.new(settings.GATEWAY_HMAC_SECRET.encode('utf-8'), payload_bytes, hashlib.sha256).hexdigest()
        return {
            "payload": payload,
            "payload_bytes": payload_bytes,
            "signature": signature
        }

    @staticmethod
    def execute_refund(refund_id: str, amount: float, idempotency_key: str, simulate_fail: bool = False) -> Dict[str, Any]:
        if simulate_fail:
            return {
                "success": False,
                "error_code": "GATEWAY_TIMEOUT",
                "message": "Payment gateway connection timed out during refund authorization."
            }
        return {
            "success": True,
            "refund_reference": f"ref_tx_{uuid.uuid4().hex[:10]}",
            "idempotency_key": idempotency_key,
            "amount": amount,
            "status": "SETTLED"
        }
