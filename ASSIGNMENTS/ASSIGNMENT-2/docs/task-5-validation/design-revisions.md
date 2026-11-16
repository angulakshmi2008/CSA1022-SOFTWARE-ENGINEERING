# Task 5: Documented Design Weaknesses and Implemented Revisions

In rigorous software engineering, system validation must not simply demonstrate nominal success; it must expose design vulnerabilities and drive documented architectural revisions. Two significant design weaknesses were uncovered and resolved during the validation phase.

---

## 1. Design Weakness 1: Silent Inventory Overselling on Delayed Payment Callbacks

### The Vulnerability Diagnosed
In the preliminary design, when a payment gateway callback arrived at `POST /api/payments/callback`, the handler verified the HMAC signature, matched the order total, inserted the `payment_event`, and unconditionally transitioned the order from `PLACED` to `PAID`:
```python
# Flawed Preliminary Implementation
if verify_signature(payload, sig) and amount == order["total_amount"]:
    db.execute("UPDATE orders SET state = 'PAID' WHERE order_id = :id")
    enqueue_outbox_intent(order_id)
```
**Failure Scenario:**
1. Customer 1 placed an order for the final unit of `SKU-LIMITED-999` at 10:00 AM.
2. The 15-minute lease expired at 10:15 AM without payment. The background expiry worker reclaimed the stock (`reserved -= 1`), setting available stock back to 1, and marked Customer 1's order as `CANCELLED`.
3. At 10:16 AM, Customer 2 placed an order for that same SKU, legitimately reserving the unit.
4. At 10:20 AM, a delayed network callback from the payment gateway finally arrived for Customer 1's expired transaction.
5. The naive callback handler marked Customer 1's order as `PAID`. As a result, **two separate customers held confirmed orders for a single physical unit of inventory**—a direct violation of Invariant 2.

### Implemented Architectural Revision
The payment callback logic and order state machine were revised to incorporate an **explicit re-reservation check and reconciliation path**:
1. When a callback arrives, the system queries the `reservations` table for an `ACTIVE` reservation matching the order.
2. If active reservations exist, the order transitions normally to `PAID`.
3. If reservations have expired, the system queries `stock_items` to evaluate if unreserved inventory is still available:
   - **Case A (Stock Available):** The system atomically creates a fresh reservation and marks the order `PAID`.
   - **Case B (Stock Resold / Out of Stock):** The system **strictly refuses to mark the order `PAID`**. Instead, it transitions the order to an explicit intermediate state: **`NEEDS_REFUND`** (Payment Captured, Stock Unavailable).
4. Within the exact same database transaction, the system automatically inserts a row into `refund_requests` with `state = 'REQUESTED'`, reason `'Late payment arrived after stock reservation expired and unit resold'`, and flags the incident in `audit_events`.
5. This revision was codified in requirement `FR08`, modeled in the state diagram, and verified empirically in test `T7_LATE_PAYMENT_EXPIRY`.

---

## 2. Design Weakness 2: Erasure of Governance Approval upon Gateway Refund Failure

### The Vulnerability Diagnosed
In early modeling of the refund workflow, the execution step treated a failure response from the external payment gateway (e.g., HTTP 504 Gateway Timeout or temporary 503 Service Unavailable) as a complete rejection or rollback:
```text
[APPROVED] ---> (Execute Gateway Call) ---> [FAILED / RESET TO REQUESTED]
```
**Failure Scenario:**
1. A customer requested a $199.99 return for a defective smartwatch.
2. A Finance Reviewer investigated the return tracking slip and formally approved the refund.
3. When the execution command was transmitted to the payment gateway, a momentary ISP fiber cut caused an HTTP socket timeout.
4. If the entity was rolled back to `REQUESTED` or deleted, the evidence of the Finance Reviewer's authorization was destroyed. To retry the refund, the support agent would have to re-petition the finance team for approval.
5. More critically, if the gateway actually captured the refund request on its backend but failed during outbound acknowledgement transmission, re-requesting and re-approving a new refund created a second distinct request with a new key, leading to **double refund disbursement**.

### Implemented Architectural Revision
The refund state machine was revised to introduce an explicit, resilient **`FAILED` (Retryable)** state:
1. When an external gateway call fails or times out, the entity state is set to `FAILED`.
2. **Approval Retention Invariant:** The database update modifies only the `state` and `failure_reason` columns. The original `approved_by` user UUID, the approval timestamp (`resolved_at`), and the pre-allocated `idempotency_key` **remain completely intact**.
3. A subsequent retry by the finance reviewer or background outbox worker does NOT require a second approval. The execution handler verifies that `state IN ('APPROVED', 'FAILED')` and re-transmits the request to the payment gateway **reusing the exact same `idempotency_key`**.
4. The payment gateway inspects the idempotency key, recognizes the previous attempt, and returns the cached execution result, guaranteeing zero duplicate money disbursements.
5. This revision was codified in requirement `FR10`, modeled in `refund-state-machine.puml`, and empirically verified in test `T3_REFUND_FAILURE_RETRY`.
