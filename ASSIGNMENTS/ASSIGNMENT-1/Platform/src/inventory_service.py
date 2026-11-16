import sqlite3
import uuid
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional
from .database import get_connection

class OutOfStockError(Exception):
    """Raised when an item has insufficient available stock."""
    pass

class ConcurrencyConflictError(Exception):
    """Raised when concurrent reservation requests conflict."""
    pass

class InventoryService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def get_product(self, sku: str) -> Optional[Dict[str, Any]]:
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE sku = ?", (sku,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_all_products(self) -> List[Dict[str, Any]]:
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products ORDER BY sku")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def reserve_stock(self, order_id: str, sku: str, quantity: int, ttl_minutes: int = 15) -> str:
        """
        Atomically reserve stock for an order with a TTL.
        Uses SQLite transaction locks to guarantee zero negative stock under high concurrency.
        """
        if quantity <= 0:
            raise ValueError("Reservation quantity must be strictly greater than 0.")

        conn = get_connection(self.db_path)
        try:
            # Use immediate transaction to acquire an exclusive write lock immediately
            conn.execute("BEGIN IMMEDIATE")
            cursor = conn.cursor()

            # First, clean up any expired reservations to restore available capacity
            now_iso = datetime.now(timezone.utc).isoformat()
            cursor.execute("""
                SELECT reservation_id, sku, quantity FROM reservations
                WHERE status = 'ACTIVE' AND expires_at < ?
            """, (now_iso,))
            expired_rows = cursor.fetchall()
            for exp in expired_rows:
                cursor.execute("""
                    UPDATE products SET stock_quantity = stock_quantity + ?
                    WHERE sku = ?
                """, (exp["quantity"], exp["sku"]))
                cursor.execute("""
                    UPDATE reservations SET status = 'RELEASED'
                    WHERE reservation_id = ?
                """, (exp["reservation_id"],))

            # Query available stock with current transaction snapshot
            cursor.execute("SELECT stock_quantity, low_stock_threshold FROM products WHERE sku = ?", (sku,))
            product = cursor.fetchone()
            if not product:
                raise OutOfStockError(f"Product with SKU '{sku}' does not exist.")

            current_stock = product["stock_quantity"]
            threshold = product["low_stock_threshold"]

            if current_stock < quantity:
                raise OutOfStockError(
                    f"Insufficient stock for SKU '{sku}'. Available: {current_stock}, Requested: {quantity}"
                )

            # Atomically decrement stock
            cursor.execute("""
                UPDATE products
                SET stock_quantity = stock_quantity - ?
                WHERE sku = ? AND stock_quantity >= ?
            """, (quantity, sku, quantity))

            if cursor.rowcount == 0:
                raise ConcurrencyConflictError("Concurrent transaction modified stock; reservation aborted.")

            new_stock = current_stock - quantity

            # Create active reservation record
            res_id = f"RES-{uuid.uuid4().hex[:10].upper()}"
            expires_at = (datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)).isoformat()
            created_at = datetime.now(timezone.utc).isoformat()

            cursor.execute("""
                INSERT INTO reservations (reservation_id, order_id, sku, quantity, status, expires_at, created_at)
                VALUES (?, ?, ?, ?, 'ACTIVE', ?, ?)
            """, (res_id, order_id, sku, quantity, expires_at, created_at))

            # Check for deterministic low-stock threshold trigger
            if new_stock <= threshold:
                alert_id = f"ALT-{uuid.uuid4().hex[:8].upper()}"
                cursor.execute("""
                    INSERT INTO low_stock_alerts (alert_id, sku, current_stock, threshold, created_at, acknowledged)
                    VALUES (?, ?, ?, ?, ?, 0)
                """, (alert_id, sku, new_stock, threshold, created_at))

            conn.commit()
            return res_id
        except (OutOfStockError, ConcurrencyConflictError, ValueError):
            conn.rollback()
            raise
        except sqlite3.OperationalError as e:
            conn.rollback()
            raise ConcurrencyConflictError(f"Database lock contention: {str(e)}")
        finally:
            conn.close()

    def confirm_reservation(self, reservation_id: str):
        """Mark reservation as CONFIRMED upon successful payment."""
        conn = get_connection(self.db_path)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE reservations SET status = 'CONFIRMED'
                WHERE reservation_id = ? AND status = 'ACTIVE'
            """, (reservation_id,))
        conn.close()

    def release_reservation(self, reservation_id: str):
        """Release reservation manually or upon cancellation."""
        conn = get_connection(self.db_path)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sku, quantity, status FROM reservations WHERE reservation_id = ?", (reservation_id,))
            res = cursor.fetchone()
            if res and res["status"] in ("ACTIVE", "CONFIRMED"):
                cursor.execute("""
                    UPDATE products SET stock_quantity = stock_quantity + ? WHERE sku = ?
                """, (res["quantity"], res["sku"]))
                cursor.execute("""
                    UPDATE reservations SET status = 'RELEASED' WHERE reservation_id = ?
                """, (reservation_id,))
        conn.close()

    def get_low_stock_alerts(self) -> List[Dict[str, Any]]:
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM low_stock_alerts ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
