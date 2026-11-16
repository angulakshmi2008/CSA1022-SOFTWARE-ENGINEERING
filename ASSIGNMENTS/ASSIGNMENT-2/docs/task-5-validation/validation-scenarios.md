# Task 5: Detailed Validation Scenarios Specification

This document details the seven primary validation scenarios (T1 through T7) constructed to deliberately test edge cases, race conditions, failure recovery, and invariant preservation.

---

### Scenario T1: Last-Unit Stock Concurrency Contention
- **Target Invariant:** Invariant 2 (Available stock never falls below zero).
- **Setup & Input Vector:**
  - SKU `SKU-LIMITED-999` in region `US-EAST` initialized with `on_hand = 1` and `reserved = 0`.
  - Two distinct authenticated customers (`buyer1`, `buyer2`) simultaneously submit checkout requests for quantity = 1 within the same concurrent execution window using a thread pool.
- **Predicted Specification Behavior:** Exactly one transaction acquires the row lock, successfully commits the reservation, and receives HTTP 201 Created. The competing transaction receives HTTP 409 Conflict with `detail = 'Insufficient available stock'`. Available stock remains exactly 0.
- **Observed Test Evidence:** Executed in `test_t1_stock_contention.py`. Two concurrent threads produced sorted HTTP statuses `[201, 409]`. Final database query confirmed `on_hand = 1, reserved = 1, available = 0`. Test PASSED in 63.8 ms.

---

### Scenario T2: Repeated Concurrent Payment Callback
- **Target Invariant:** Invariant 1 (One gateway event identity results in at most one payment effect).
- **Setup & Input Vector:**
  - Order placed for `SKU-HEADSET-003` (total $166.29).
  - External payment gateway transmits 10 identical webhook callbacks for event ID `evt-t2-dedup-test-999` concurrently across 5 thread workers.
- **Predicted Specification Behavior:** Exactly one request executes the first-time insertion, transitions the order to `PAID`, and enqueues an outbox intent. The subsequent 9 requests encounter unique constraint collisions, return HTTP 200 with `is_duplicate = True`, and produce zero secondary state mutations.
- **Observed Test Evidence:** Executed in `test_t2_duplicate_callback.py`. Out of 10 concurrent HTTP deliveries, exactly 1 returned `PAYMENT_CONFIRMED` and 9 returned `DUPLICATE_ACKNOWLEDGED`. Database inspection verified exactly 1 row in `payment_events` and exactly 1 row in `outbox_intents`. Test PASSED in 91.2 ms.

---

### Scenario T3: Approved Refund Gateway Failure and Controlled Retry
- **Target Invariant:** Invariant 3 (Dual-control refund gate; approval retention on failure).
- **Setup & Input Vector:**
  - Customer requests a refund of $199.99 for `SKU-WATCH-004`.
  - Finance Reviewer approves the refund (`state = APPROVED`).
  - First execution attempt simulates a gateway network timeout (`504 Gateway Timeout`).
  - Second execution attempt retries with restored network connectivity.
- **Predicted Specification Behavior:** The first execution fails and transitions state to `FAILED`, but **strictly retains** the `approved_by` reviewer reference. The second execution retries under the same pre-allocated idempotency key, successfully reaches the gateway, and transitions state to `EXECUTED`.
- **Observed Test Evidence:** Executed in `test_t3_refund_failure_retry.py`. First attempt returned state `FAILED` with `approved_by = user-t3-finance`. Second attempt succeeded, transitioning state to `EXECUTED`. Test PASSED in 91.2 ms.

---

### Scenario T4: Dispatch Attempt Without Confirmed Payment or Pick Confirmation
- **Target Invariant:** Invariant 5 (Guarded dispatch lifecycle).
- **Setup & Input Vector:**
  - Order placed (`state = PLACED`).
  - Picker attempts to dispatch the order directly.
  - Order payment confirmed (`state = PAID`), but pick confirmation not yet performed.
  - Picker attempts to dispatch the order again.
  - Picker executes pick & pack (`state = PACKED`).
  - Picker executes dispatch.
- **Predicted Specification Behavior:** Direct dispatch from `PLACED` is rejected with HTTP 400. Dispatch from `PAID` without pick confirmation is rejected with HTTP 400. Dispatch from `PACKED` succeeds with HTTP 200 and transitions order to `DISPATCHED`.
- **Observed Test Evidence:** Executed in `test_t4_dispatch_guards.py`. Both invalid dispatch attempts were rejected with HTTP 400 Bad Request; valid dispatch after pick confirmation succeeded with HTTP 200. Test PASSED in 95.8 ms.

---

### Scenario T5: Courier Synchronization Timeout and Reconciliation
- **Target Invariant:** Invariant 6 and Invariant 7 (Resilient outbox and correlation key reconciliation).
- **Setup & Input Vector:**
  - Order paid; outbox intent created with `status = PENDING`.
  - Worker runs against mock courier with timeout simulation enabled.
  - Worker runs again with restored network.
- **Predicted Specification Behavior:** In Run 1, the worker catches the network timeout, keeps the intent in `PENDING` status, increments `attempts = 1`, and schedules exponential backoff. In Run 2, the worker reconciles using `correlation_key`, completes courier booking, marks intent `COMPLETED`, and saves carrier tracking number `TRK-...`.
- **Observed Test Evidence:** Executed in `test_t5_courier_retry.py`. Run 1 failed with `attempts = 1, status = PENDING`. Run 2 completed with `attempts = 2, status = COMPLETED, tracking_no = TRK-DB3AE309`. Zero duplicate shipments occurred. Test PASSED in 50.8 ms.

---

### Scenario T6: Security RBAC and Cross-Customer Access Isolation
- **Target Invariant:** Invariant 4 (Customer resource isolation and least privilege).
- **Setup & Input Vector:**
  - Customer A places an order.
  - Customer B attempts to read Customer A's order (`GET /api/orders/{id}`).
  - Customer A attempts to approve their own refund ($150.00).
  - Support Agent attempts to approve Customer A's refund ($150.00 > $50.00).
  - Finance Reviewer approves Customer A's refund.
- **Predicted Specification Behavior:** Customer B's cross-read is rejected with HTTP 403 Forbidden. Customer A's self-approval is rejected with HTTP 403 Forbidden. Support Agent's high-value approval is rejected with HTTP 403 Forbidden. Finance Reviewer's approval succeeds with HTTP 200 OK.
- **Observed Test Evidence:** Executed in `test_t6_security_rbac.py`. All three unauthorized access vectors received HTTP 403 Forbidden; Finance Reviewer approval succeeded with HTTP 200 OK. Test PASSED in 110.5 ms.

---

### Scenario T7: Late Payment Callback After Reservation Expiry (Weakness Revision)
- **Target Invariant:** Invariant 2 (Zero stock overselling under lease expiration).
- **Setup & Input Vector:**
  - Buyer 1 places order for final unit of `SKU-LIMITED-999`.
  - Reservation lease (15 minutes) expires; expiry worker reclaims inventory.
  - Buyer 2 places order and claims that same unit.
  - Delayed payment callback arrives for Buyer 1's expired order.
- **Predicted Specification Behavior:** The callback handler detects that the reservation expired and no available inventory remains. To prevent overselling, the order is transitioned to `NEEDS_REFUND` (instead of `PAID`), and an automated refund request is queued for finance resolution.
- **Observed Test Evidence:** Executed in `test_t7_late_payment_expiry.py`. Buyer 1's order was marked `NEEDS_REFUND`, and an automated refund request was created with state `REQUESTED`. Available stock was preserved. Test PASSED in 82.2 ms.
