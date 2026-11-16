import unittest
import os
import tempfile
import uuid

from Platform.src.database import seed_database
from Platform.src.auth_service import AuthService, PermissionDeniedError, AuthenticationError
from Platform.src.order_service import OrderService, OrderStatus

class TestSecurityRoles(unittest.TestCase):
    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        seed_database(self.temp_db_path)
        self.order_service = OrderService(self.temp_db_path)

        self.cust_token = AuthService.login("cust_alex", "alex123")["token"]
        self.support_token = AuthService.login("support_sarah", "support123")["token"]
        self.picker_token = AuthService.login("picker_john", "picker123")["token"]
        self.finance_token = AuthService.login("finance_frank", "finance123")["token"]

        # Helper to advance an order to RETURN_REQUESTED
        order = self.order_service.create_order(
            self.cust_token,
            [{"sku": "SKU-TSHIRT-01", "quantity": 1}],
            region_code="REG-NORTH"
        )
        self.order_id = order["order_id"]
        self.order_service.process_order_payment(self.order_id, self.cust_token, f"IDEMP-{uuid.uuid4().hex[:6]}")
        self.order_service.transition_order_status(self.order_id, OrderStatus.PICKING, self.picker_token)
        self.order_service.transition_order_status(self.order_id, OrderStatus.PICKED, self.picker_token)
        self.order_service.transition_order_status(self.order_id, OrderStatus.DISPATCHED, self.picker_token)
        self.order_service.transition_order_status(self.order_id, OrderStatus.DELIVERED, self.picker_token)
        self.order_service.request_return(self.order_id, self.cust_token, "Wrong size")

    def tearDown(self):
        try:
            os.close(self.temp_db_fd)
            os.remove(self.temp_db_path)
        except Exception:
            pass

    def test_support_agent_cannot_approve_refund(self):
        """MSC-04: Support agent role must be rejected when attempting to approve a refund."""
        with self.assertRaises(PermissionDeniedError):
            self.order_service.approve_refund(self.order_id, self.support_token, "Agent trying to refund")

    def test_warehouse_picker_cannot_approve_refund(self):
        """MSC-04: Warehouse picker role must be rejected when attempting to approve a refund."""
        with self.assertRaises(PermissionDeniedError):
            self.order_service.approve_refund(self.order_id, self.picker_token, "Picker trying to refund")

    def test_finance_reviewer_can_approve_refund(self):
        """MSC-04: Finance reviewer role successfully approves refund and logs audit."""
        res = self.order_service.approve_refund(self.order_id, self.finance_token, "Legitimate return verified")
        self.assertEqual(res["status"], OrderStatus.REFUNDED.value)

        # Verify audit log contains finance approver identity
        audit_trail = self.order_service.get_audit_trail(self.order_id)
        refund_logs = [a for a in audit_trail if a["action"] == "REFUND_APPROVED"]
        self.assertEqual(len(refund_logs), 1)
        self.assertEqual(refund_logs[0]["actor_role"], "FINANCE_REVIEWER")
        self.assertEqual(refund_logs[0]["actor_id"], "finance_frank")

    def test_tampered_token_rejected(self):
        """Security: Tampered token must raise AuthenticationError."""
        tampered_token = self.cust_token[:-4] + "XXXX"
        with self.assertRaises(AuthenticationError):
            AuthService.verify_token(tampered_token)

if __name__ == "__main__":
    unittest.main()
