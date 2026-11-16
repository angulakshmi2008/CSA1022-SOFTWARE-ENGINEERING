from tests.test_helpers import get_test_client, get_auth_header
from backend.app.models.enums import UserRole, RefundState
from backend.app.database import get_db

def test_t3_refund_failure_retry():
    """T3: An approved refund failing at the gateway and requiring a controlled retry or rollback."""
    client = get_test_client()
    customer_id = "user-t3-cust"
    finance_id = "user-t3-finance"
    
    cust_h = get_auth_header("t3cust", UserRole.CUSTOMER, customer_id)
    fin_h = get_auth_header("t3finance", UserRole.FINANCE_REVIEWER, finance_id)
    
    # 1. Place order
    ord_res = client.post("/api/orders/", json={
        "items": [{"sku": "SKU-WATCH-004", "quantity": 1}],
        "region_id": "US-EAST"
    }, headers=cust_h)
    assert ord_res.status_code == 201
    order_id = ord_res.json()["order_id"]
    
    # 2. Create Refund Request ($199.99 > $50.00 threshold)
    refund_res = client.post("/api/refunds/", json={
        "order_id": order_id,
        "amount": 199.99,
        "reason": "Defective sensor unit"
    }, headers=cust_h)
    assert refund_res.status_code == 201
    refund_data = refund_res.json()
    refund_id = refund_data["refund_id"]
    assert refund_data["state"] == RefundState.REQUESTED.value
    
    # 3. Finance Reviewer Approves
    approve_res = client.post(f"/api/refunds/{refund_id}/decide", json={
        "decision": "APPROVE",
        "notes": "Verified return receipt; approved for gateway refund."
    }, headers=fin_h)
    assert approve_res.status_code == 200
    approved_data = approve_res.json()
    assert approved_data["state"] == RefundState.APPROVED.value
    assert approved_data["approved_by"] == finance_id
    
    # 4. First Execution Attempt: Gateway Failure (Simulate 504 Gateway Timeout)
    fail_exec_res = client.post(f"/api/refunds/{refund_id}/execute", json={
        "simulate_gateway_failure": True
    }, headers=fin_h)
    assert fail_exec_res.status_code == 200
    failed_data = fail_exec_res.json()
    assert failed_data["state"] == RefundState.FAILED.value
    # CRITICAL INVARIANT: The approval MUST be retained even though gateway execution failed!
    assert failed_data["approved_by"] == finance_id, "Weakness regression: Failed execution cleared approval!"
    assert "timeout" in failed_data["failure_reason"].lower()
    
    # 5. Second Execution Attempt: Controlled Retry with identical idempotency key
    retry_exec_res = client.post(f"/api/refunds/{refund_id}/execute", json={
        "simulate_gateway_failure": False
    }, headers=fin_h)
    assert retry_exec_res.status_code == 200
    executed_data = retry_exec_res.json()
    assert executed_data["state"] == RefundState.EXECUTED.value
    assert executed_data["approved_by"] == finance_id
    assert executed_data["idempotency_key"] == refund_data["idempotency_key"]
    
    return {
        "test_id": "T3_REFUND_FAILURE_RETRY",
        "description": "Approved refund failing at gateway followed by controlled retry",
        "expected": "Transitions REQUESTED -> APPROVED -> FAILED (approval retained) -> EXECUTED",
        "observed": f"Final state: {executed_data['state']}, approved_by retained: {executed_data['approved_by']}",
        "status": "PASSED"
    }

if __name__ == "__main__":
    res = test_t3_refund_failure_retry()
    print("Test T3 Passed:", res)
