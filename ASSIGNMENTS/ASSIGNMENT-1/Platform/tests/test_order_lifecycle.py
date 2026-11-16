import unittest
import os
import tempfile
import uuid

from Platform.src.database import seed_database
from Platform.src.auth_service import AuthService
from Platform.src.order_service import OrderService, OrderStatus, InvalidStateTransitionError

class TestOrderLifecycle(unittest.TestCase):
    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        seed_database(self.temp_db_path)
        self.order_service = OrderService(self.temp_db_path)

        self.cust_token = AuthService.login("cust_alex", "alex123")["token"]
        self.picker_token = AuthService.login("picker_john", "picker123")["token"]
        self.finance_token = AuthService.login("finance_frank", "finance123")["token"]

    def tearDown(self):
        try:
            os.close(self.temp_db_fd)
            os.remove(self.temp_db_path)
        except Exception:
            pass

    def test_full_successful_order_to_refund_lifecycle(self):
        """MSC-01: Verifies the complete 10-state operational lifecycle."""
        # 1. Create order (CREATED -> RESERVED)
        order = self.order_service.create_order(
            self.cust_token,
            [{"sku": "SKU-TSHIRT-01", "quantity": 1}],
            region_code="REG-NORTH"
        )
        order_id = order["order_id"]
        self.assertEqual(order["status"], OrderStatus.RESERVED.value)

        # 2. Payment (RESERVED -> PAID)
        idemp_key = f"IDEMP-TEST-{uuid.uuid4().hex[:8]}"
        pay_res = self.order_service.process_order_payment(order_id, self.cust_token, idemp_key)
        self.assertEqual(pay_res["status"], "SUCCESS")
        updated = self.order_service.get_order(order_id)
        self.assertEqual(updated["status"], OrderStatus.PAID.value)

        # 3. Warehouse picking (PAID -> PICKING -> PICKED)
        self.order_service.transition_order_status(order_id, OrderStatus.PICKING, self.picker_token, "Picking started")
        self.order_service.transition_order_status(order_id, OrderStatus.PICKED, self.picker_token, "Pick completed")
        updated = self.order_service.get_order(order_id)
        self.assertEqual(updated["status"], OrderStatus.PICKED.value)

        # 4. Dispatch and delivery (PICKED -> DISPATCHED -> DELIVERED)
        self.order_service.transition_order_status(order_id, OrderStatus.DISPATCHED, self.picker_token, "Courier pickup")
        self.order_service.transition_order_status(order_id, OrderStatus.DELIVERED, self.picker_token, "Delivered to address")
        updated = self.order_service.get_order(order_id)
        self.assertEqual(updated["status"], OrderStatus.DELIVERED.value)
        self.assertIsNotNone(updated["delivered_at"])

        # 5. Customer return (DELIVERED -> RETURN_REQUESTED)
        self.order_service.request_return(order_id, self.cust_token, "Damaged during shipment")
        updated = self.order_service.get_order(order_id)
        self.assertEqual(updated["status"], OrderStatus.RETURN_REQUESTED.value)

        # 6. Finance refund approval (RETURN_REQUESTED -> REFUNDED)
        ref_res = self.order_service.approve_refund(order_id, self.finance_token, "Goods inspected; refund approved")
        self.assertEqual(ref_res["status"], OrderStatus.REFUNDED.value)

        # 7. Audit records verification
        audit_trail = self.order_service.get_audit_trail(order_id)
        self.assertGreaterEqual(len(audit_trail), 6)
        actions = [a["action"] for a in audit_trail]
        self.assertIn("ORDER_CREATED", actions)
        self.assertIn("STATUS_CHANGE", actions)
        self.assertIn("REFUND_APPROVED", actions)

    def test_invalid_lifecycle_transition_rejected(self):
        """MSC-01 Negative Test: Asserts invalid transition jumps are rejected."""
        order = self.order_service.create_order(
            self.cust_token,
            [{"sku": "SKU-TSHIRT-01", "quantity": 1}],
            region_code="REG-NORTH"
        )
        order_id = order["order_id"]

        # Attempt to jump directly from RESERVED to DISPATCHED without paying
        with self.assertRaises(InvalidStateTransitionError):
            self.order_service.transition_order_status(order_id, OrderStatus.DISPATCHED, self.picker_token, "Illegal bypass")

if __name__ == "__main__":
    unittest.main()
