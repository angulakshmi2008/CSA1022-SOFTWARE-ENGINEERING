import uuid
import time
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from .database import get_connection

class PaymentError(Exception):
    """Raised when payment processing encounters a decline or failure."""
    pass

class PaymentGatewayTimeoutError(PaymentError):
    """Raised when simulated gateway encounters a network timeout."""
    pass

class PaymentService:
    def __init__(self, db_path: Optional[str] = None, simulated_mode: str = "SUCCESS"):
        """
        simulated_mode:
            - 'SUCCESS': Standard approved charge
            - 'DECLINED': Insufficient funds / card declined
            - 'TIMEOUT': Network timeout (simulates Week 1-3 sandbox unavailability)
        """
        self.db_path = db_path
        self.simulated_mode = simulated_mode

    def process_payment(self, order_id: str, amount: float, idempotency_key: str) -> Dict[str, Any]:
        """
        Process payment with strict idempotency verification.
        If idempotency_key already exists, returns the existing record immediately without re-charging.
        """
        if not idempotency_key or not idempotency_key.strip():
            raise ValueError("Idempotency key is strictly required to prevent duplicate charges.")
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        conn = get_connection(self.db_path)
        try:
            cursor = conn.cursor()

            # 1. Check if idempotency key has already been processed
            cursor.execute("""
                SELECT intent_id, order_id, idempotency_key, amount, status, gateway_transaction_id, created_at
                FROM payment_intents
                WHERE idempotency_key = ?
            """, (idempotency_key,))
            existing = cursor.fetchone()

            if existing:
                # Return the existing transaction idempotently
                conn.close()
                return {
                    "is_duplicate_replay": True,
                    "intent_id": existing["intent_id"],
                    "order_id": existing["order_id"],
                    "idempotency_key": existing["idempotency_key"],
                    "amount": existing["amount"],
                    "status": existing["status"],
                    "gateway_transaction_id": existing["gateway_transaction_id"],
                    "created_at": existing["created_at"],
                    "message": "Idempotent response: Returning previously processed transaction intent."
                }

            # 2. Simulate gateway behavior
            if self.simulated_mode == "TIMEOUT":
                conn.close()
                raise PaymentGatewayTimeoutError("Simulated payment gateway timeout: No response received.")
            elif self.simulated_mode == "DECLINED":
                conn.close()
                raise PaymentError("Simulated payment gateway decline: Insufficient synthetic balance.")

            # 3. Successful charge simulation
            intent_id = f"PI-{uuid.uuid4().hex[:12].upper()}"
            gw_txn_id = f"GW-TXN-{uuid.uuid4().hex[:10].upper()}"
            created_at = datetime.now(timezone.utc).isoformat()

            cursor.execute("""
                INSERT INTO payment_intents (intent_id, order_id, idempotency_key, amount, status, gateway_transaction_id, created_at)
                VALUES (?, ?, ?, ?, 'SUCCESS', ?, ?)
            """, (intent_id, order_id, idempotency_key, amount, gw_txn_id, created_at))
            conn.commit()

            return {
                "is_duplicate_replay": False,
                "intent_id": intent_id,
                "order_id": order_id,
                "idempotency_key": idempotency_key,
                "amount": amount,
                "status": "SUCCESS",
                "gateway_transaction_id": gw_txn_id,
                "created_at": created_at,
                "message": "Payment charged successfully via mock gateway adapter."
            }
        finally:
            conn.close()

    def process_refund(self, order_id: str, amount: float, reason: str) -> Dict[str, Any]:
        """Process refund reversal against an existing payment intent."""
        conn = get_connection(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT intent_id, amount, status FROM payment_intents
                WHERE order_id = ? AND status = 'SUCCESS'
            """, (order_id,))
            intent = cursor.fetchone()

            if not intent:
                raise PaymentError(f"No successful payment intent found for Order '{order_id}' to refund.")

            if amount > intent["amount"]:
                raise ValueError(f"Refund amount ({amount}) cannot exceed original charged amount ({intent['amount']}).")

            refund_txn_id = f"GW-REF-{uuid.uuid4().hex[:10].upper()}"
            cursor.execute("""
                UPDATE payment_intents
                SET status = 'REFUNDED'
                WHERE intent_id = ?
            """, (intent["intent_id"],))
            conn.commit()

            return {
                "refund_transaction_id": refund_txn_id,
                "intent_id": intent["intent_id"],
                "order_id": order_id,
                "amount": amount,
                "status": "REFUNDED",
                "reason": reason
            }
        finally:
            conn.close()
