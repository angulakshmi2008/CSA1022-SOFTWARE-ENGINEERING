import concurrent.futures
from tests.test_helpers import get_test_client, get_auth_header
from backend.app.models.enums import UserRole
from backend.app.database import get_db

def test_t1_stock_contention():
    """T1: Two customers attempting to buy the last unit of a product concurrently."""
    # Setup test users
    user1_id = "user-t1-buyer-001"
    user2_id = "user-t1-buyer-002"
    h1 = get_auth_header("buyer1", UserRole.CUSTOMER, user1_id)
    h2 = get_auth_header("buyer2", UserRole.CUSTOMER, user2_id)
    
    # Reset SKU-LIMITED-999 to exactly 1 on_hand and 0 reserved in US-EAST
    with get_db() as conn:
        conn.execute("""
            UPDATE stock_items 
            SET on_hand = 1, reserved = 0, version = 1 
            WHERE sku = 'SKU-LIMITED-999' AND region_id = 'US-EAST'
        """)
        
    client = get_test_client()
    order_payload = {
        "items": [{"sku": "SKU-LIMITED-999", "quantity": 1}],
        "region_id": "US-EAST"
    }
    
    def place_order(headers):
        c = get_test_client()
        return c.post("/api/orders/", json=order_payload, headers=headers)
        
    # Execute concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        f1 = executor.submit(place_order, h1)
        f2 = executor.submit(place_order, h2)
        r1 = f1.result()
        r2 = f2.result()
        
    statuses = sorted([r1.status_code, r2.status_code])
    assert statuses == [201, 409], f"Expected one 201 Created and one 409 Conflict, got: {statuses}"
    
    # Verify Invariant: Available stock (on_hand - reserved) >= 0
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT on_hand, reserved FROM stock_items WHERE sku = 'SKU-LIMITED-999' AND region_id = 'US-EAST'")
        stock = cursor.fetchone()
        available = stock["on_hand"] - stock["reserved"]
        assert available == 0, f"Expected available stock == 0, got {available}"
        assert stock["on_hand"] >= stock["reserved"], "Invariant violated: available stock is negative!"
        
    return {
        "test_id": "T1_STOCK_CONTENTION",
        "description": "Two buyers competing for the last unit",
        "expected": "One 201 Created, one 409 Conflict, available stock == 0",
        "observed": f"HTTP {statuses[0]} and {statuses[1]}, available stock == 0",
        "status": "PASSED"
    }

if __name__ == "__main__":
    res = test_t1_stock_contention()
    print("Test T1 Passed:", res)
