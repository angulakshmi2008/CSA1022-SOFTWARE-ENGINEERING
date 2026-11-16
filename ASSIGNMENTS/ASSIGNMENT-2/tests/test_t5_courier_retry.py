from tests.test_helpers import get_test_client, get_auth_header
from backend.app.models.enums import UserRole, IntentStatus
from backend.app.integrations.payment.mock_gateway import MockPaymentGateway
from backend.app.integrations.courier.mock_courier import MockCourierAPI
from backend.app.workers.outbox_worker import process_pending_outbox_intents
from backend.app.database import get_db

def test_t5_courier_retry():
    """T5: A courier synchronization request failing and then being retried."""
    client = get_test_client()
    customer_id = "user-t5-cust"
    cust_h = get_auth_header("t5cust", UserRole.CUSTOMER, customer_id)
    MockCourierAPI.reset()
    
    # 1. Place order
    ord_res = client.post("/api/orders/", json={
        "items": [{"sku": "SKU-CHAIR-006", "quantity": 1}],
        "region_id": "US-EAST"
    }, headers=cust_h)
    assert ord_res.status_code == 201
    order_id = ord_res.json()["order_id"]
    order_total = ord_res.json()["total_amount"]
    
    # 2. Confirm payment to generate outbox intent
    gw_data = MockPaymentGateway.generate_signed_callback_payload(order_id, order_total)
    pay_res = client.post("/api/payments/callback", json=gw_data["payload"], headers={"X-Signature": gw_data["signature"]})
    assert pay_res.status_code == 200
    
    # 3. First Worker Run: Simulate Courier Partner Network Timeout
    with get_db() as conn:
        run1 = process_pending_outbox_intents(conn, simulate_courier_timeout=True, target_order_id=order_id)
        assert run1["processed"] == 1
        assert run1["failed"] == 1
        assert run1["succeeded"] == 0
        
        # Verify intent remains PENDING with incremented attempts
        cursor = conn.cursor()
        cursor.execute("SELECT status, attempts FROM outbox_intents WHERE aggregate_id = ?", (order_id,))
        intent_state = cursor.fetchone()
        assert intent_state["status"] == IntentStatus.PENDING.value
        assert intent_state["attempts"] == 1
        
    # 4. Second Worker Run: Courier Network Restored -> Retry Succeeds
    with get_db() as conn:
        # Fast-forward next_retry_at to current time for immediate execution
        conn.execute("UPDATE outbox_intents SET next_retry_at = datetime('now', 'utc') WHERE aggregate_id = ?", (order_id,))
        run2 = process_pending_outbox_intents(conn, simulate_courier_timeout=False, target_order_id=order_id)
        assert run2["succeeded"] == 1
        
        cursor = conn.cursor()
        cursor.execute("SELECT status, attempts, external_reference FROM outbox_intents WHERE aggregate_id = ?", (order_id,))
        final_intent = cursor.fetchone()
        assert final_intent["status"] == IntentStatus.COMPLETED.value
        assert final_intent["attempts"] == 2
        assert final_intent["external_reference"].startswith("TRK-")
        tracking_no = final_intent["external_reference"]
        
    return {
        "test_id": "T5_COURIER_RETRY",
        "description": "Courier synchronization request timeout and idempotent retry",
        "expected": "Run 1 fails (attempts=1, status=PENDING), Run 2 succeeds (attempts=2, status=COMPLETED)",
        "observed": f"Run 1 failed as expected; Run 2 completed with tracking number {tracking_no}",
        "status": "PASSED"
    }

if __name__ == "__main__":
    res = test_t5_courier_retry()
    print("Test T5 Passed:", res)
