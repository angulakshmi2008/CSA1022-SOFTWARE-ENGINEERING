import sqlite3
from typing import List, Dict, Any, Optional
from .database import get_connection

class BarcodeMismatchError(Exception):
    """Raised when scanned barcode does not match the pick item."""
    pass

class WarehouseService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def get_pick_list(self, warehouse_id: str) -> List[Dict[str, Any]]:
        """
        Generate digital pick list for warehouse pickers.
        Strictly filters orders that are in PAID state and assigned to the specified warehouse.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.order_id, o.warehouse_id, o.status, oi.sku, oi.quantity, p.name, p.barcode
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.sku = p.sku
            WHERE o.warehouse_id = ? AND o.status = 'PAID'
            ORDER BY o.created_at ASC
        """, (warehouse_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def verify_barcode(self, sku: str, scanned_barcode: str) -> bool:
        """
        Software-based barcode scanner emulation.
        Confirms whether the scanned barcode string matches the product SKU.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT barcode, name FROM products WHERE sku = ?", (sku,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            raise BarcodeMismatchError(f"SKU '{sku}' does not exist.")

        expected_barcode = row["barcode"]
        if scanned_barcode.strip() != expected_barcode:
            raise BarcodeMismatchError(
                f"Barcode mismatch for {row['name']} ({sku})! Scanned: '{scanned_barcode}', Expected: '{expected_barcode}'"
            )

        return True
