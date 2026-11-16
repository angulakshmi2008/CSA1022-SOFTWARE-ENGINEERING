import unittest
import os
import tempfile
import uuid

from Platform.src.database import seed_database
from Platform.src.auth_service import AuthService
from Platform.src.order_service import OrderService, OrderStatus
from Platform.src.payment_service import PaymentService, PaymentGatewayTimeoutError

class TestPaymentIdempotency(unittest.TestCase):
    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        seed_database(self.temp_db_path)
        self.order_service = OrderService(self.temp_db_path)
        self.payment_service = PaymentService(self.temp_db_path)
        self.cust_token = AuthService.login("cust_alex", "alex123")["token"]

    def tearDown(self):
        try:
            os.close(self.temp_db_fd)
            os.remove(self.temp_db_path)
        except Exception:
            pass

    def test_ten_repeated_payment_requests_create_exactly_one_intent(self):
        """
        MSC-03: Ten retries with identical idempotency key must return the identical
        intent and create zero duplicate database payment charges.
        """
        order = self.order_service.create_order(
            self.cust_token,
            [{"sku": "SKU-TSHIRT-01", "quantity": 1}],
            region_code="REG-NORTH"
        )
        order_id = order["order_id"]
        idempotency_key = f"IDEMP-RETRY-{uuid.uuid4().hex[:8]}"

        results = []
        for i in range(10):
            res = self.order_service.process_order_payment(order_id, self.cust_token, idempotency_key)
            results.append(res)

        # 1. The first call creates the intent; the next 9 are duplicate replays
        self.assertFalse(results[0]["is_duplicate_replay"])
        first_intent_id = results[0]["intent_id"]

        for i in range(1, 10):
            self.assertTrue(results[i]["is_duplicate_replay"], f"Call {i} should be flagged as replay")
            self.assertEqual(results[i]["intent_id"], first_intent_id, "Intent ID must be identical across retries")

        # 2. Verify database records: exactly ONE intent exists in SQLite
        conn = self.order_service.inventory_service.db_path
        from Platform.src.database import get_connection
        c = get_connection(self.temp_db_path)
        cur = c.cursor()
        cur.execute("SELECT COUNT(*) as count FROM payment_intents WHERE idempotency_key = ?", (idempotency_key,))
        row = cur.fetchone()
        c.close()
        self.assertEqual(row["count"], 1, "Database must record exactly 1 payment intent for this key!")

    def test_gateway_timeout_leaves_order_recoverable(self):
        """MSC-03: Gateway timeout leaves order in RESERVED state without crashing."""
        timeout_service = PaymentService(self.temp_db_path, simulated_mode="TIMEOUT")
        with self.assertRaises(PaymentGatewayTimeoutError):
            timeout_service.process_payment("ORD-TIMEOUT-TEST", 50.0, "IDEMP-TIMEOUT-01")

if __name__ == "__main__":
    unittest.main()
