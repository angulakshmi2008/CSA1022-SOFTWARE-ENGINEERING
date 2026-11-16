from tests.test_helpers import get_test_client, get_auth_header
from backend.app.models.enums import UserRole
from backend.app.database import get_db

def test_t8_scanner_deduplication():
    """T8: Replayed scan burst after reconnect with deduplication by (node_id, event_id)."""
    client = get_test_client()
    picker_id = "user-t8-scanner-operator"
    headers = get_auth_header("scanner_op", UserRole.PICKER, picker_id)
    
    # Baseline stock for SKU-PHONE-002 in US-EAST
    with get_db() as conn:
        conn.execute("UPDATE stock_items SET on_hand = 50, reserved = 0 WHERE sku = 'SKU-PHONE-002' AND region_id = 'US-EAST'")
        
    # Construct batch of 10 events: 5 unique events repeated twice (simulating edge retry burst)
    batch_events = []
    for i in range(5):
        event_dict = {
            "node_id": "SCANNER-WH-A1",
            "event_id": f"scan-evt-{i:03d}",
            "sku": "SKU-PHONE-002",
            "region_id": "US-EAST",
            "event_type": "RECEIVE",
            "quantity": 10,
            "observation_time": "2026-11-14T10:00:00Z",
            "schema_version": "1.0"
        }
        batch_events.append(event_dict)
        batch_events.append(event_dict) # duplicate in same batch
        
    assert len(batch_events) == 10
    
    sync_res = client.post("/api/scanner/sync-batch", json={"events": batch_events}, headers=headers)
    assert sync_res.status_code == 200, f"Sync failed: {sync_res.text}"
    sync_data = sync_res.json()
    
    assert sync_data["received_count"] == 10
    assert sync_data["processed_count"] == 5
    assert sync_data["duplicate_count"] == 5
    
    # Verify inventory was incremented by exactly 5 * 10 = 50 units (not 100!)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT on_hand FROM stock_items WHERE sku = 'SKU-PHONE-002' AND region_id = 'US-EAST'")
        final_on_hand = cursor.fetchone()["on_hand"]
        assert final_on_hand == 100, f"Expected on_hand == 100 (50 initial + 50 received), got {final_on_hand}"
        
    return {
        "test_id": "T8_SCANNER_DEDUPLICATION",
        "description": "Replayed scan burst after reconnect deduplicated by (node_id, event_id)",
        "expected": "10 received, 5 processed, 5 duplicates ignored, stock updated by 50",
        "observed": f"Processed {sync_data['processed_count']}, Duplicates {sync_data['duplicate_count']}, final stock {final_on_hand}",
        "status": "PASSED"
    }

if __name__ == "__main__":
    res = test_t8_scanner_deduplication()
    print("Test T8 Passed:", res)
