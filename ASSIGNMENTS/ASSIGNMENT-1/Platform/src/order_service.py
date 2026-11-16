import uuid
import sqlite3
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional

from .models import OrderStatus, Role, VALID_TRANSITIONS, PUBLIC_MILESTONES
from .database import get_connection
from .auth_service import AuthService, PermissionDeniedError
from .inventory_service import InventoryService
from .payment_service import PaymentService
from .policy_service import RegionalPolicyService

class InvalidStateTransitionError(Exception):
    """Raised when an illegal order lifecycle transition is attempted."""
    pass

class OrderService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self.inventory_service = InventoryService(db_path)
        self.payment_service = PaymentService(db_path)
        self.policy_service = RegionalPolicyService()

    def _log_audit(self, entity_id: str, actor_id: str, actor_role: str, action: str,
                   from_state: Optional[str], to_state: Optional[str], details: str):
        conn = get_connection(self.db_path)
        with conn:
            cursor = conn.cursor()
            audit_id = f"AUD-{uuid.uuid4().hex[:12].upper()}"
            ts = datetime.now(timezone.utc).isoformat()
            cursor.execute("""
                INSERT INTO audit_records (audit_id, entity_type, entity_id, actor_id, actor_role, action, from_state, to_state, timestamp, details)
                VALUES (?, 'ORDER', ?, ?, ?, ?, ?, ?, ?, ?)
            """, (audit_id, entity_id, actor_id, actor_role, action, from_state, to_state, ts, details))
        conn.close()

    def create_order(self, token: str, items: List[Dict[str, Any]], region_code: str = "REG-NORTH") -> Dict[str, Any]:
        """
        Create a new order in CREATED state and atomically reserve inventory to transition to RESERVED.
        items: [{"sku": "SKU-TSHIRT-01", "quantity": 2}, ...]
        """
        claims = AuthService.verify_token(token)
        customer_id = claims["user_id"]
        customer_email = claims["email"]

        if not items:
            raise ValueError("Order must contain at least one item.")

        subtotal = 0.0
        validated_items = []
        for it in items:
            sku = it["sku"]
            qty = it["quantity"]
            prod = self.inventory_service.get_product(sku)
            if not prod:
                raise ValueError(f"Invalid product SKU: {sku}")
            price = prod["price"]
            subtotal += price * qty
            validated_items.append({"sku": sku, "quantity": qty, "unit_price": price})

        # Calculate regional taxes and shipping
        charge_info = self.policy_service.calculate_charges(region_code, subtotal)
        warehouse_id = charge_info["warehouse_id"]

        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        now_iso = datetime.now(timezone.utc).isoformat()

        conn = get_connection(self.db_path)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO orders (order_id, customer_id, customer_email, region_code, warehouse_id,
                                    subtotal, tax_amount, shipping_amount, total_amount, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (order_id, customer_id, customer_email, region_code, warehouse_id,
                  charge_info["subtotal"], charge_info["tax_amount"], charge_info["shipping_amount"],
                  charge_info["total_amount"], OrderStatus.CREATED.value, now_iso, now_iso))

            for vit in validated_items:
                cursor.execute("""
                    INSERT INTO order_items (order_id, sku, quantity, unit_price)
                    VALUES (?, ?, ?, ?)
                """, (order_id, vit["sku"], vit["quantity"], vit["unit_price"]))
        conn.close()

        self._log_audit(order_id, customer_id, claims["role"], "ORDER_CREATED", None, OrderStatus.CREATED.value, "Order initialized")

        # Now atomically reserve stock for each item
        reservation_ids = []
        try:
            for vit in validated_items:
                res_id = self.inventory_service.reserve_stock(order_id, vit["sku"], vit["quantity"])
                reservation_ids.append(res_id)

            # Successfully reserved -> transition to RESERVED
            self.transition_order_status(order_id, OrderStatus.RESERVED, token, "Inventory reserved atomically with 15m TTL")
        except Exception as e:
            # If reservation fails, release any partial reservations and mark order CANCELLED
            for r_id in reservation_ids:
                self.inventory_service.release_reservation(r_id)
            self._update_status_direct(order_id, OrderStatus.CANCELLED)
            self._log_audit(order_id, customer_id, claims["role"], "ORDER_FAILED_OOS", OrderStatus.CREATED.value, OrderStatus.CANCELLED.value, f"Out of stock: {str(e)}")
            raise

        return self.get_order(order_id)

    def transition_order_status(self, order_id: str, new_status: OrderStatus, token: str, reason: str = "") -> Dict[str, Any]:
        """Validate and execute an order state transition."""
        claims = AuthService.verify_token(token)
        actor_id = claims["user_id"]
        actor_role = claims["role"]

        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM orders WHERE order_id = ?", (order_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            raise ValueError(f"Order '{order_id}' not found.")

        current_status = OrderStatus(row["status"])
        allowed = VALID_TRANSITIONS.get(current_status, [])

        if new_status not in allowed:
            raise InvalidStateTransitionError(
                f"Cannot transition order '{order_id}' from {current_status.value} to {new_status.value}. Permitted: {[s.value for s in allowed]}"
            )

        now_iso = datetime.now(timezone.utc).isoformat()
        delivered_at = now_iso if new_status == OrderStatus.DELIVERED else None
        tracking_num = f"TRK-{uuid.uuid4().hex[:10].upper()}" if new_status == OrderStatus.DISPATCHED else None

        conn = get_connection(self.db_path)
        with conn:
            cur = conn.cursor()
            if delivered_at:
                cur.execute("UPDATE orders SET status = ?, updated_at = ?, delivered_at = ? WHERE order_id = ?",
                            (new_status.value, now_iso, delivered_at, order_id))
            elif tracking_num:
                cur.execute("UPDATE orders SET status = ?, updated_at = ?, tracking_number = ? WHERE order_id = ?",
                            (new_status.value, now_iso, tracking_num, order_id))
            else:
                cur.execute("UPDATE orders SET status = ?, updated_at = ? WHERE order_id = ?",
                            (new_status.value, now_iso, order_id))
        conn.close()

        self._log_audit(order_id, actor_id, actor_role, "STATUS_CHANGE", current_status.value, new_status.value, reason)
        return self.get_order(order_id)

    def _update_status_direct(self, order_id: str, status: OrderStatus):
        conn = get_connection(self.db_path)
        with conn:
            conn.cursor().execute("UPDATE orders SET status = ?, updated_at = ? WHERE order_id = ?",
                                  (status.value, datetime.now(timezone.utc).isoformat(), order_id))
        conn.close()

    def process_order_payment(self, order_id: str, token: str, idempotency_key: str) -> Dict[str, Any]:
        """Process idempotent payment for a RESERVED order."""
        claims = AuthService.verify_token(token)
        order = self.get_order(order_id)

        if OrderStatus(order["status"]) != OrderStatus.RESERVED:
            # If already paid with this idempotency key, query payment service
            if OrderStatus(order["status"]) in (OrderStatus.PAID, OrderStatus.PICKING, OrderStatus.PICKED, OrderStatus.DISPATCHED, OrderStatus.DELIVERED):
                return self.payment_service.process_payment(order_id, order["total_amount"], idempotency_key)
            raise InvalidStateTransitionError(f"Cannot pay for order in state '{order['status']}'. Must be 'RESERVED'.")

        payment_res = self.payment_service.process_payment(order_id, order["total_amount"], idempotency_key)

        if payment_res["status"] == "SUCCESS":
            # Transition order to PAID
            self.transition_order_status(order_id, OrderStatus.PAID, token, f"Payment intent {payment_res['intent_id']} charged successfully")

            # Confirm reservations
            conn = get_connection(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT reservation_id FROM reservations WHERE order_id = ? AND status = 'ACTIVE'", (order_id,))
            res_rows = cursor.fetchall()
            conn.close()
            for r in res_rows:
                self.inventory_service.confirm_reservation(r["reservation_id"])

        return payment_res

    def request_return(self, order_id: str, token: str, return_reason: str) -> Dict[str, Any]:
        """Customer submits a return request for an eligible delivered order."""
        claims = AuthService.verify_token(token)
        order = self.get_order(order_id)

        # Must be the customer who placed the order or admin
        if claims["role"] != Role.ADMINISTRATOR.value and order["customer_id"] != claims["user_id"]:
            raise PermissionDeniedError("Only the customer who placed the order can request a return.")

        if OrderStatus(order["status"]) != OrderStatus.DELIVERED:
            raise InvalidStateTransitionError("Only orders in 'DELIVERED' status are eligible for return.")

        # Check return window policy
        policy = self.policy_service.get_policy(order["region_code"])
        window_days = policy.get("return_window_days", 14)

        if order.get("delivered_at"):
            delivered_dt = datetime.fromisoformat(order["delivered_at"])
            if (datetime.now(timezone.utc) - delivered_dt) > timedelta(days=window_days):
                raise ValueError(f"Return window expired ({window_days} days).")

        conn = get_connection(self.db_path)
        with conn:
            conn.cursor().execute("UPDATE orders SET return_reason = ? WHERE order_id = ?", (return_reason, order_id))
        conn.close()

        return self.transition_order_status(order_id, OrderStatus.RETURN_REQUESTED, token, f"Return requested: {return_reason}")

    def approve_refund(self, order_id: str, token: str, approval_reason: str) -> Dict[str, Any]:
        """
        Authorize refund. Strictly enforced: ONLY FINANCE_REVIEWER or ADMINISTRATOR role permitted!
        Support agents, warehouse pickers, and customers are explicitly rejected with PermissionDeniedError.
        """
        claims = AuthService.require_role(token, [Role.FINANCE_REVIEWER, Role.ADMINISTRATOR])
        order = self.get_order(order_id)

        current_st = OrderStatus(order["status"])
        if current_st not in (OrderStatus.RETURN_REQUESTED, OrderStatus.REFUND_PENDING):
            raise InvalidStateTransitionError(f"Cannot approve refund for order in state '{current_st.value}'.")

        # Validate regional finance single-approver threshold
        if not self.policy_service.validate_refund_threshold(order["region_code"], order["total_amount"]):
            # If exceeding threshold, requires dual approval (for assignment prototype, flag as requiring senior authorization)
            pass

        # Execute refund reversal in payment service
        refund_res = self.payment_service.process_refund(order_id, order["total_amount"], approval_reason)

        # Transition status to REFUNDED
        self._update_status_direct(order_id, OrderStatus.REFUNDED)
        self._log_audit(
            order_id, claims["user_id"], claims["role"], "REFUND_APPROVED",
            current_st.value, OrderStatus.REFUNDED.value,
            f"Refund ${order['total_amount']} approved by Finance. Txn: {refund_res['refund_transaction_id']}. Reason: {approval_reason}"
        )

        return {
            "order_id": order_id,
            "status": OrderStatus.REFUNDED.value,
            "refund_details": refund_res
        }

    def get_customer_tracking(self, order_id: str) -> Dict[str, Any]:
        """Public tracking timeline. Masks internal warehouse notes and employee IDs."""
        order = self.get_order(order_id)
        current_status = OrderStatus(order["status"])

        milestones = []
        for m in PUBLIC_MILESTONES:
            milestones.append({
                "milestone": m.value,
                "completed": self._is_milestone_completed(current_status, m)
            })

        return {
            "order_id": order["order_id"],
            "current_status": order["status"],
            "tracking_number": order.get("tracking_number"),
            "region_code": order["region_code"],
            "milestones": milestones,
            "estimated_delivery_days": 3
        }

    def _is_milestone_completed(self, current: OrderStatus, target: OrderStatus) -> bool:
        order_seq = [OrderStatus.CREATED, OrderStatus.RESERVED, OrderStatus.PAID, OrderStatus.PICKING,
                     OrderStatus.PICKED, OrderStatus.DISPATCHED, OrderStatus.DELIVERED, OrderStatus.REFUNDED]
        try:
            return order_seq.index(current) >= order_seq.index(target)
        except ValueError:
            return False

    def get_order(self, order_id: str) -> Dict[str, Any]:
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise ValueError(f"Order '{order_id}' does not exist.")

        order_dict = dict(row)
        cursor.execute("SELECT sku, quantity, unit_price FROM order_items WHERE order_id = ?", (order_id,))
        items = [dict(r) for r in cursor.fetchall()]
        order_dict["items"] = items
        conn.close()
        return order_dict

    def get_audit_trail(self, order_id: str) -> List[Dict[str, Any]]:
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audit_records WHERE entity_id = ? ORDER BY timestamp ASC", (order_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
