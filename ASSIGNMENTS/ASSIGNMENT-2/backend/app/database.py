import sqlite3
import os
import threading
from contextlib import contextmanager
from backend.app.config import settings

_db_lock = threading.RLock()

def get_connection(db_path: str = None) -> sqlite3.Connection:
    target_path = db_path or settings.DATABASE_PATH
    os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
    conn = sqlite3.connect(target_path, timeout=30.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn

@contextmanager
def get_db(db_path: str = None):
    with _db_lock:
        conn = get_connection(db_path)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

def init_db(db_path: str = None):
    with get_db(db_path) as conn:
        cursor = conn.cursor()
        
        # 1. Users Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            region_id TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'utc'))
        );
        """)

        # 2. Regional Policies Table (12 Regions, Versioned)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS regional_policies (
            region_id TEXT NOT NULL,
            region_name TEXT NOT NULL,
            policy_version INTEGER NOT NULL DEFAULT 1,
            tax_rate REAL NOT NULL,
            shipping_fee REAL NOT NULL,
            refund_approval_threshold REAL NOT NULL,
            effective_from TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
            is_active INTEGER NOT NULL DEFAULT 1,
            PRIMARY KEY (region_id, policy_version)
        );
        """)

        # 3. Products Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            sku TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            base_price REAL NOT NULL,
            category TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'utc'))
        );
        """)

        # 4. Stock Items Table (with non-negative constraint)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_items (
            sku TEXT NOT NULL,
            region_id TEXT NOT NULL,
            on_hand INTEGER NOT NULL DEFAULT 0,
            reserved INTEGER NOT NULL DEFAULT 0,
            version INTEGER NOT NULL DEFAULT 1,
            updated_at TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
            PRIMARY KEY (sku, region_id),
            FOREIGN KEY (sku) REFERENCES products(sku),
            CHECK ((on_hand - reserved) >= 0)
        );
        """)

        # 5. Orders Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            owner_id TEXT NOT NULL,
            state TEXT NOT NULL,
            region_id TEXT NOT NULL,
            policy_version INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            tax_amount REAL NOT NULL,
            shipping_fee REAL NOT NULL,
            total_amount REAL NOT NULL,
            dispatch_due_at TEXT,
            version INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
            FOREIGN KEY (owner_id) REFERENCES users(user_id)
        );
        """)

        # 6. Order Lines Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_lines (
            line_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            sku TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            tax_rate REAL NOT NULL,
            tax_amount REAL NOT NULL,
            line_total REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (sku) REFERENCES products(sku),
            CHECK (quantity > 0)
        );
        """)

        # 7. Reservations Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            reservation_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            sku TEXT NOT NULL,
            region_id TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            expires_at TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (sku) REFERENCES products(sku)
        );
        """)

        # 8. Payment Events Table (Composite Unique Key for Deduplication)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payment_events (
            event_pk TEXT PRIMARY KEY,
            gateway_id TEXT NOT NULL,
            event_id TEXT NOT NULL,
            order_id TEXT NOT NULL,
            amount REAL NOT NULL,
            currency TEXT NOT NULL DEFAULT 'USD',
            status TEXT NOT NULL,
            signature TEXT NOT NULL,
            verified_at TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            UNIQUE (gateway_id, event_id)
        );
        """)

        # 9. Refund Requests Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS refund_requests (
            refund_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            amount REAL NOT NULL,
            state TEXT NOT NULL,
            reason TEXT NOT NULL,
            requested_by TEXT NOT NULL,
            approved_by TEXT,
            idempotency_key TEXT UNIQUE NOT NULL,
            failure_reason TEXT,
            version INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
            resolved_at TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (requested_by) REFERENCES users(user_id),
            FOREIGN KEY (approved_by) REFERENCES users(user_id)
        );
        """)

        # 10. Transactional Outbox Intents Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS outbox_intents (
            intent_id TEXT PRIMARY KEY,
            aggregate_id TEXT NOT NULL,
            purpose TEXT NOT NULL,
            correlation_key TEXT UNIQUE NOT NULL,
            payload_json TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING',
            attempts INTEGER NOT NULL DEFAULT 0,
            max_attempts INTEGER NOT NULL DEFAULT 5,
            next_retry_at TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
            external_reference TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now', 'utc'))
        );
        """)

        # 11. Edge Scanner Event Logs Table (Deduplication by node_id + event_id)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scanner_event_logs (
            log_id TEXT PRIMARY KEY,
            node_id TEXT NOT NULL,
            event_id TEXT NOT NULL,
            sku TEXT NOT NULL,
            region_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            observation_time TEXT NOT NULL,
            received_at TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
            schema_version TEXT NOT NULL,
            is_stale INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (sku) REFERENCES products(sku),
            UNIQUE (node_id, event_id)
        );
        """)

        # 12. Append-Only Audit Trail Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_events (
            event_id TEXT PRIMARY KEY,
            actor_id TEXT NOT NULL,
            action TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            old_version INTEGER,
            new_version INTEGER,
            details_json TEXT,
            occurred_at TEXT NOT NULL DEFAULT (datetime('now', 'utc'))
        );
        """)

        # Indexes for Query Performance and Latency
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_owner ON orders(owner_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_state ON orders(state);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_outbox_pending ON outbox_intents(status, next_retry_at);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reservations_expiry ON reservations(status, expires_at);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_events(entity_type, entity_id);")
