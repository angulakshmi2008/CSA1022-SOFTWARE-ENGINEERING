from tests.test_helpers import get_test_client, get_auth_header
from backend.app.models.enums import UserRole, RefundState

def test_t11_offline_refund_approval():
    """T11: Offline refund approval queued locally remains Pending until server validates permissions."""
    client = get_test_client()
    customer_id = "user-t11-cust"
    picker_id = "user-t11-picker"
    finance_id = "user-t11-finance"
    
    cust_h = get_auth_header("t11cust", UserRole.CUSTOMER, customer_id)
    picker_h = get_auth_header("t11picker", UserRole.PICKER, picker_id)
    fin_h = get_auth_header("t11finance", UserRole.FINANCE_REVIEWER, finance_id)
    
    # 1. Place order
    ord_res = client.post("/api/orders/", json={
        "items": [{"sku": "SKU-HEADSET-003", "quantity": 1}],
        "region_id": "US-EAST"
    }, headers=cust_h)
    assert ord_res.status_code == 201
    order_id = ord_res.json()["order_id"]
    
    # 2. Customer creates refund request ($149.00 > $50 threshold)
    refund_res = client.post("/api/refunds/", json={
        "order_id": order_id,
        "amount": 149.00,
        "reason": "Customer changed mind"
    }, headers=cust_h)
    assert refund_res.status_code == 201
    refund_id = refund_res.json()["refund_id"]
    
    # Verify Initial State: Must be REQUESTED (Pending)
    assert refund_res.json()["state"] == RefundState.REQUESTED.value
    
    # ATTACK / EDGE CASE: Handheld warehouse terminal or unprivileged staff claims offline approval
    offline_fraud_res = client.post(f"/api/refunds/{refund_id}/decide", json={"decision": "APPROVE"}, headers=picker_h)
    assert offline_fraud_res.status_code == 403, "Security flaw: Non-finance staff approved refund!"
    
    # Check that refund state is STILL REQUESTED (Pending) in database
    refund_check = client.get("/api/refunds/", headers=cust_h).json()
    target_refund = next(r for r in refund_check if r["refund_id"] == refund_id)
    assert target_refund["state"] == RefundState.REQUESTED.value, "State was altered without server approval!"
    
    # Legitimate Server-Side Approval by Finance Reviewer
    legit_approve_res = client.post(f"/api/refunds/{refund_id}/decide", json={"decision": "APPROVE"}, headers=fin_h)
    assert legit_approve_res.status_code == 200
    assert legit_approve_res.json()["state"] == RefundState.APPROVED.value
    
    return {
        "test_id": "T11_OFFLINE_REFUND_APPROVAL",
        "description": "Offline queued refund approval remains Pending until authenticated server validation",
        "expected": "Unauthenticated or unprivileged attempt rejected with HTTP 403; remains REQUESTED until Finance approval",
        "observed": f"Rejected unauthorized decision ({offline_fraud_res.status_code}), validated server approval ({legit_approve_res.status_code})",
        "status": "PASSED"
    }

if __name__ == "__main__":
    res = test_t11_offline_refund_approval()
    print("Test T11 Passed:", res)
