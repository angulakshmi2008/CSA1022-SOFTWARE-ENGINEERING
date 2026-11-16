import unittest
import os
import tempfile
import threading
import time

from Platform.src.database import seed_database
from Platform.src.auth_service import AuthService
from Platform.src.inventory_service import InventoryService, OutOfStockError, ConcurrencyConflictError

class TestStockConcurrency(unittest.TestCase):
    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        seed_database(self.temp_db_path)
        self.inventory_service = InventoryService(self.temp_db_path)

    def tearDown(self):
        try:
            os.close(self.temp_db_fd)
            os.remove(self.temp_db_path)
        except Exception:
            pass

    def test_concurrent_reservations_prevent_negative_stock(self):
        """
        MSC-02: Under 100 concurrent reservation attempts for a 10-unit item,
        exactly 10 reservations must succeed, 90 must fail cleanly with OutOfStock,
        and available stock must NEVER become negative.
        """
        target_sku = "SKU-SNEAKER-02"  # Initial stock = 10 units in synthetic catalog
        product_before = self.inventory_service.get_product(target_sku)
        initial_stock = product_before["stock_quantity"]
        self.assertEqual(initial_stock, 10)

        success_count = 0
        failure_count = 0
        lock = threading.Lock()

        def attempt_reservation(worker_id: int):
            nonlocal success_count, failure_count
            order_id = f"ORD-CONCUR-{worker_id:03d}"
            max_retries = 25
            for attempt in range(max_retries):
                try:
                    res_id = self.inventory_service.reserve_stock(order_id, target_sku, quantity=1)
                    with lock:
                        success_count += 1
                    return
                except OutOfStockError:
                    with lock:
                        failure_count += 1
                    return
                except ConcurrencyConflictError:
                    # Brief jitter backoff on SQLite lock busy
                    time.sleep(0.01 * (attempt + 1))
            
            with lock:
                failure_count += 1

        # Launch 100 concurrent worker threads
        threads = []
        for i in range(100):
            t = threading.Thread(target=attempt_reservation, args=(i,))
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Check final stock state
        product_after = self.inventory_service.get_product(target_sku)
        final_stock = product_after["stock_quantity"]

        # Assertions
        self.assertEqual(success_count, 10, f"Expected exactly 10 successes, got {success_count}")
        self.assertEqual(failure_count, 90, f"Expected exactly 90 failures, got {failure_count}")
        self.assertEqual(final_stock, 0, f"Final stock must be exactly 0, got {final_stock}")
        self.assertGreaterEqual(final_stock, 0, "Available stock must NEVER drop below zero!")

if __name__ == "__main__":
    unittest.main()
