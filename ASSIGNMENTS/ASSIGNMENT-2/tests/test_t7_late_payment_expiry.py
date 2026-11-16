from tests.test_helpers import get_test_client, get_auth_header
from backend.app.models.enums import UserRole, OrderState, RefundState
from backend.app.integrations.payment.mock_gateway import MockPaymentGateway
from backend.app.workers.expiry_worker import expire_unpaid_reservations
from backend.app.database import get_db

def test_t7_late_payment_expiry():
    """T7: Late payment after reservation expiry (Weakness 1 Revision)."""
    client = get_test_client()
    buyer1_id = "user-t7-late-buyer"
    buyer2_id = "user-t7-sniper-buyer"
    
    b1_h = get_auth_header("t7latebuyer", UserRole.CUSTOMER, buyer1_id)
    b2_h = get_auth_header("t7sniperbuyer", UserRole.CUSTOMER, buyer2_id)
    
    # 1. Reset SKU-LIMITED-999 to exactly 1 on_hand and 0 reserved in US-EAST
    with get_db() as conn:
        conn.execute("""
            UPDATE stock_items
            SET on_hand = 1, reserved = 0, version = 1
            WHERE sku = 'SKU-LIMITED-999' AND region_id = 'US-EAST'
        """)
        
    # 2. Buyer 1 places order for the 1 unit (State: PLACED, Reserved = 1)
    ord1_res = client.post("/api/orders/", json={
        "items": [{"sku": "SKU-LIMITED-999", "quantity": 1}],
        "region_id": "US-EAST"
    }, headers=b1_h)
    assert ord1_res.status_code == 201
    ord1_id = ord1_res.json()["order_id"]
    ord1_total = ord1_res.json()["total_amount"]
    
    # 3. Simulate 15-minute lease expiry by updating expires_at to 20 minutes ago
    with get_db() as conn:
        conn.execute("""
            UPDATE reservations 
            SET expires_at = datetime('now', '-20 minutes') 
            WHERE order_id = ?
        """, (ord1_id,))
        # Run expiry reclamation worker
        exp_res = expire_unpaid_reservations(conn)
        assert exp_res["reclaimed_orders"] >= 1
        
        # Verify Buyer 1's order was marked CANCELLED and stock restored
        cursor = conn.cursor()
        cursor.execute("SELECT state FROM orders WHERE order_id = ?", (ord1_id,))
        assert cursor.fetchone()["state"] == OrderState.CANCELLED.value
        
        cursor.execute("SELECT on_hand, reserved FROM stock_items WHERE sku = 'SKU-LIMITED-999' AND region_id = 'US-EAST'")
        stock = cursor.fetchone()
        assert stock["on_hand"] == 1 and stock["reserved"] == 0
        
    # 4. Buyer 2 immediately places order and claims that same unit!
    ord2_res = client.post("/api/orders/", json={
        "items": [{"sku": "SKU-LIMITED-999", "quantity": 1}],
        "region_id": "US-EAST"
    }, headers=b2_h)
    assert ord2_res.status_code == 201
    
    # 5. Now, a delayed webhook callback arrives for Buyer 1's cancelled order!
    gw_data = MockPaymentGateway.generate_signed_callback_payload(ord1_id, ord1_total)
    late_callback_res = client.post("/api/payments/callback", json=gw_data["payload"], headers={"X-Signature": gw_data["signature"]})
    assert late_callback_res.status_code == 200
    
    # 6. Verify Design Revision: Order state must NOT be PAID; it must be NEEDS_REFUND!
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT state FROM orders WHERE order_id = ?", (ord1_id,))
        final_state = cursor.fetchone()["state"]
        assert final_state == OrderState.NEEDS_REFUND.value, f"Oversell bug! Order marked {final_state} instead of NEEDS_REFUND"
        
        # Verify automated refund request was created
        cursor.execute("SELECT state, amount, reason FROM refund_requests WHERE order_id = ?", (ord1_id,))
        refund = cursor.fetchone()
        assert refund is not None, "Automated refund request was not generated!"
        assert refund["state"] == RefundState.REQUESTED.value
        assert "Late payment arrived" in refund["reason"]
        
    return {
        "test_id": "T7_LATE_PAYMENT_EXPIRY",
        "description": "Late payment callback after reservation expiry and inventory resale",
        "expected": "Order marked NEEDS_REFUND; automatic refund request created; zero stock oversold",
        "observed": f"Order state: {final_state}, refund request created with state {refund['state']}",
        "status": "PASSED"
    }

if __name__ == "__main__":
    res = test_t7_late_payment_expiry()
    print("Test T7 Passed:", res)
