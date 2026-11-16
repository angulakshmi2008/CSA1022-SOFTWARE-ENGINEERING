import concurrent.futures
from tests.test_helpers import get_test_client, get_auth_header
from backend.app.models.enums import UserRole, OrderState
from backend.app.integrations.payment.mock_gateway import MockPaymentGateway
from backend.app.database import get_db

def test_t2_duplicate_callback():
    """T2: A repeated payment callback arriving while the original callback is being processed."""
    client = get_test_client()
    user_id = "user-t2-buyer"
    headers = get_auth_header("t2buyer", UserRole.CUSTOMER, user_id)
    
    # 1. Create Order
    order_res = client.post("/api/orders/", json={
        "items": [{"sku": "SKU-HEADSET-003", "quantity": 1}],
        "region_id": "US-EAST"
    }, headers=headers)
    assert order_res.status_code == 201, f"Order placement failed: {order_res.text}"
    order_data = order_res.json()
    order_id = order_data["order_id"]
    order_total = order_data["total_amount"]
    
    # 2. Generate signed callback payload
    event_id = "evt-t2-dedup-test-999"
    gateway_data = MockPaymentGateway.generate_signed_callback_payload(order_id, order_total, event_id=event_id)
    payload = gateway_data["payload"]
    signature = gateway_data["signature"]
    
    # 3. Deliver callback 10 times concurrently
    def deliver_webhook():
        c = get_test_client()
        return c.post("/api/payments/callback", json=payload, headers={"X-Signature": signature})
        
    responses = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(deliver_webhook) for _ in range(10)]
        for f in futures:
            responses.append(f.result())
            
    # All 10 deliveries must succeed with HTTP 200
    for idx, r in enumerate(responses):
        assert r.status_code == 200, f"Delivery {idx} failed with {r.status_code}: {r.text}"
        
    # Check duplicate flags
    duplicate_count = sum(1 for r in responses if r.json().get("is_duplicate") is True)
    confirmed_count = sum(1 for r in responses if r.json().get("status") == "PAYMENT_CONFIRMED")
    assert confirmed_count == 1, f"Expected exactly 1 PAYMENT_CONFIRMED, got {confirmed_count}"
    assert duplicate_count == 9, f"Expected exactly 9 duplicates, got {duplicate_count}"
    
    # 4. Verify Database Invariants
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Invariant 1: Exactly one payment record for this gateway/event_id
        cursor.execute("SELECT COUNT(*) FROM payment_events WHERE gateway_id = ? AND event_id = ?", (payload["gateway_id"], event_id))
        pay_count = cursor.fetchone()[0]
        assert pay_count == 1, f"Expected 1 payment event row, found {pay_count}"
        
        # Invariant 2: Order state is PAID
        cursor.execute("SELECT state FROM orders WHERE order_id = ?", (order_id,))
        assert cursor.fetchone()["state"] == OrderState.PAID.value
        
        # Invariant 3: Exactly one courier outbox intent created
        cursor.execute("SELECT COUNT(*) FROM outbox_intents WHERE aggregate_id = ?", (order_id,))
        intent_count = cursor.fetchone()[0]
        assert intent_count == 1, f"Expected 1 outbox intent, found {intent_count}"
        
    return {
        "test_id": "T2_DUPLICATE_CALLBACK",
        "description": "Repeated concurrent payment callback (10 deliveries)",
        "expected": "1 confirmation, 9 duplicate acknowledgements, 1 payment record, 1 outbox intent",
        "observed": f"{confirmed_count} confirmed, {duplicate_count} duplicates, {pay_count} DB row, {intent_count} outbox intent",
        "status": "PASSED"
    }

if __name__ == "__main__":
    res = test_t2_duplicate_callback()
    print("Test T2 Passed:", res)
