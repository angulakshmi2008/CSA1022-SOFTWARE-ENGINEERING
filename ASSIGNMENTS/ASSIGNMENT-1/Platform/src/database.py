import sqlite3
import os
import json
import threading
from typing import Optional

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "order_fulfilment.db")

_lock = threading.Lock()

def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    target_db = db_path if db_path else DB_FILE
    conn = sqlite3.connect(target_db, timeout=20.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_database(db_path: Optional[str] = None):
    with _lock:
        conn = get_connection(db_path)
        cursor = conn.cursor()

        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            sku TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL CHECK(stock_quantity >= 0),
            low_stock_threshold INTEGER NOT NULL,
            barcode TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            region_code TEXT NOT NULL,
            warehouse_id TEXT NOT NULL,
            subtotal REAL NOT NULL,
            tax_amount REAL NOT NULL,
            shipping_amount REAL NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            delivered_at TEXT,
            tracking_number TEXT,
            return_reason TEXT
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL,
            sku TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (sku) REFERENCES products(sku)
        );

        CREATE TABLE IF NOT EXISTS reservations (
            reservation_id TEXT PRIMARY KEY,
            order_id TEXT,
            sku TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            status TEXT NOT NULL, -- ACTIVE, RELEASED, CONFIRMED
            expires_at TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (sku) REFERENCES products(sku)
        );

        CREATE TABLE IF NOT EXISTS payment_intents (
            intent_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            idempotency_key TEXT NOT NULL UNIQUE,
            amount REAL NOT NULL,
            status TEXT NOT NULL, -- PENDING, SUCCESS, FAILED, REFUNDED
            gateway_transaction_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        );

        CREATE TABLE IF NOT EXISTS audit_records (
            audit_id TEXT PRIMARY KEY,
            entity_type TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            actor_id TEXT NOT NULL,
            actor_role TEXT NOT NULL,
            action TEXT NOT NULL,
            from_state TEXT,
            to_state TEXT,
            timestamp TEXT NOT NULL,
            details TEXT
        );

        CREATE TABLE IF NOT EXISTS low_stock_alerts (
            alert_id TEXT PRIMARY KEY,
            sku TEXT NOT NULL,
            current_stock INTEGER NOT NULL,
            threshold INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            acknowledged INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (sku) REFERENCES products(sku)
        );
        """)
        conn.commit()
        conn.close()

def seed_database(db_path: Optional[str] = None):
    initialize_database(db_path)
    catalog_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test-data", "synthetic_catalog.json")
    if not os.path.exists(catalog_path):
        return

    with open(catalog_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    conn = get_connection(db_path)
    cursor = conn.cursor()
    for p in products:
        cursor.execute("""
            INSERT OR REPLACE INTO products (sku, name, category, price, stock_quantity, low_stock_threshold, barcode)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (p["sku"], p["name"], p["category"], p["price"], p["stock_quantity"], p["low_stock_threshold"], p["barcode"]))
    conn.commit()
    conn.close()
