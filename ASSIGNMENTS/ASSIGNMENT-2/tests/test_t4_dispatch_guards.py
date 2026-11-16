from tests.test_helpers import get_test_client, get_auth_header
from backend.app.models.enums import UserRole, OrderState
from backend.app.integrations.payment.mock_gateway import MockPaymentGateway

def test_t4_dispatch_guards():
    """T4: A dispatch attempt without confirmed payment or pick confirmation."""
    client = get_test_client()
    customer_id = "user-t4-cust"
    picker_id = "user-t4-picker"
    
    cust_h = get_auth_header("t4cust", UserRole.CUSTOMER, customer_id)
    picker_h = get_auth_header("t4picker", UserRole.PICKER, picker_id)
    
    # 1. Place order (State: PLACED)
    ord_res = client.post("/api/orders/", json={
        "items": [{"sku": "SKU-DESK-005", "quantity": 1}],
        "region_id": "US-EAST"
    }, headers=cust_h)
    assert ord_res.status_code == 201
    order_data = ord_res.json()
    order_id = order_data["order_id"]
    order_total = order_data["total_amount"]
    
    # GUARD TEST 1: Dispatch directly from PLACED state (Unpaid & Unpicked)
    dispatch_attempt_1 = client.post(f"/api/warehouse/orders/{order_id}/dispatch", headers=picker_h)
    assert dispatch_attempt_1.status_code == 400, f"Expected 400 Bad Request, got {dispatch_attempt_1.status_code}"
    assert "Lifecycle Guard Violation" in dispatch_attempt_1.json()["detail"]
    
    # 2. Confirm Payment via verified webhook callback (State: PAID)
    gw_data = MockPaymentGateway.generate_signed_callback_payload(order_id, order_total)
    pay_res = client.post("/api/payments/callback", json=gw_data["payload"], headers={"X-Signature": gw_data["signature"]})
    assert pay_res.status_code == 200
    
    # GUARD TEST 2: Dispatch from PAID state without pick confirmation (Unpicked)
    dispatch_attempt_2 = client.post(f"/api/warehouse/orders/{order_id}/dispatch", headers=picker_h)
    assert dispatch_attempt_2.status_code == 400, f"Expected 400 Bad Request, got {dispatch_attempt_2.status_code}"
    assert "PACKED" in dispatch_attempt_2.json()["detail"]
    
    # 3. Confirm Pick & Pack (State: PACKED)
    pack_res = client.post(f"/api/warehouse/orders/{order_id}/pack", headers=picker_h)
    assert pack_res.status_code == 200
    assert pack_res.json()["state"] == OrderState.PACKED.value
    
    # GUARD TEST 3: Dispatch after valid Pick & Pack confirmation -> SUCCEEDS
    dispatch_attempt_3 = client.post(f"/api/warehouse/orders/{order_id}/dispatch", headers=picker_h)
    assert dispatch_attempt_3.status_code == 200
    assert dispatch_attempt_3.json()["state"] == OrderState.DISPATCHED.value
    
    return {
        "test_id": "T4_DISPATCH_GUARDS",
        "description": "Dispatch attempt without payment or pick confirmation",
        "expected": "HTTP 400 on PLACED, HTTP 400 on PAID, HTTP 200 on PACKED",
        "observed": f"Rejected PLACED ({dispatch_attempt_1.status_code}), rejected PAID ({dispatch_attempt_2.status_code}), allowed PACKED ({dispatch_attempt_3.status_code})",
        "status": "PASSED"
    }

if __name__ == "__main__":
    res = test_t4_dispatch_guards()
    print("Test T4 Passed:", res)
