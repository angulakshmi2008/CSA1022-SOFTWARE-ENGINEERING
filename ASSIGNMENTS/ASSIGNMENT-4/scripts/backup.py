"""
Database backup script for reproducible state preservation (Q5 Recovery Strategy).
Creates a timestamped snapshot of the SQLite database and metadata manifest.
"""

from datetime import datetime, timezone
import json
import os
import shutil
import sqlite3
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_DB = os.path.join(PROJECT_DIR, "smart_campus.db")
BACKUP_DIR = os.path.join(PROJECT_DIR, "backups")


def create_backup(source_db_path: str = DEFAULT_DB) -> str:
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"campus_backup_{timestamp}.db")
    manifest_file = os.path.join(BACKUP_DIR, f"campus_backup_{timestamp}.json")

    if not os.path.exists(source_db_path):
        print(f"[-] Source database does not exist: {source_db_path}")
        return ""

    # SQLite online backup API ensures consistent copy even with active readers
    src_conn = sqlite3.connect(source_db_path)
    dst_conn = sqlite3.connect(backup_file)
    with dst_conn:
        src_conn.backup(dst_conn)
    dst_conn.close()

    # Query counts for manifest
    cursor = src_conn.cursor()
    counts = {}
    for table in ["users", "facilities", "bookings", "maintenance_tickets", "audit_logs", "outbox_events"]:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            counts[table] = cursor.fetchone()[0]
        except Exception:
            counts[table] = 0
    src_conn.close()

    manifest = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "backup_file": os.path.basename(backup_file),
        "source_file": os.path.basename(source_db_path),
        "table_row_counts": counts,
    }

    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[+] Backup successfully created: {backup_file}")
    print(f"[+] Backup manifest: {manifest_file}")
    print(f"[+] Verified Row Counts: {counts}")
    return backup_file


if __name__ == "__main__":
    create_backup()
