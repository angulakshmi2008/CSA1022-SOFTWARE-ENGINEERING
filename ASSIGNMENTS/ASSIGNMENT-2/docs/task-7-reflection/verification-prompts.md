# Task 7: Assessment Verification Prompts and Traceability Proofs

This document prepares the engineering candidate for faculty oral evaluation and verification prompts as specified in Section 8 of the official CSA10 Assignment 2 Faculty Evaluation Guide.

---

## Verification Prompt 1: Trace a Requirement Through UML, Architecture, and Validation

### Target Requirement: FR05 (Idempotent Payment Confirmation)

1. **Requirements Specification (`FR05`):**
   - *Text:* The system shall verify payment callback authenticity and deduplicate incoming events by gateway identity and event identity.
   - *Acceptance Criterion:* Delivering the exact same signed webhook callback 10 times results in exactly 1 payment record inserted, exactly 1 order state update to `PAID`, exactly 1 shipment outbox entry, and 10 identical HTTP 200 acknowledgments.

2. **UML Representation:**
   - *Use Case Model (`use-case.puml`):* External actor `Payment Gateway` initiates `UC16 (Process Verified Callback)`.
   - *Class Diagram (`class.puml`):* Entity `PaymentEvent` defines attributes `gateway_id`, `event_id`, `amount`, and `verified_at` with an explicit composite unique constraint: `UNIQUE(gateway_id, event_id)`.
   - *Sequence Diagram (`payment-courier-sequence.puml`):* Steps 1–8 trace the incoming signed callback:
     - API verifies HMAC-SHA256 signature and matches amount against `order.total_amount`.
     - Transaction begins: attempts `INSERT INTO payment_events`.
     - Branch A (First Delivery): inserts event, updates `order.state = PAID`, writes `audit_events`, inserts `outbox_intents`, commits transaction, returns HTTP 200 (`PAYMENT_CONFIRMED`).
     - Branch B (Duplicate Collision): unique key collision triggers rollback, returns HTTP 200 (`DUPLICATE_ACKNOWLEDGED`) with zero secondary state mutations.

3. **Architectural Component Implementation:**
   - *Component View (`component-diagram.puml`):* `Payment Callback Handler` coordinates with `PostgreSQL Transactional DB` and inserts an intent into `Transactional Outbox Queue`.
   - *Code Module:* `backend/app/api/payments.py` (FastAPI route) delegating to `backend/app/services/payment_service.py` (`process_payment_callback`).

4. **Empirical Validation:**
   - *Test Case:* `tests/test_t2_duplicate_callback.py`.
   - *Observed Evidence:* A thread pool delivered 10 concurrent requests for event `evt-t2-dedup-test-999`. Exactly 1 confirmed, 9 returned duplicate, database confirmed exactly 1 row in `payment_events`, and exactly 1 row in `outbox_intents`. Duration: 91.2 ms.

---

## Verification Prompt 2: Explain a Critical System Invariant

### Target Invariant: Invariant 2 (Available Stock Never Falls Below Zero)

1. **Mathematical Definition:**
   $$\forall s \in \text{StockItems}, \quad \text{AvailableStock}(s) = \text{OnHand}(s) - \text{Reserved}(s) \ge 0$$

2. **Domain Meaning:**
   In an omnichannel retailer, physical warehouse shelves hold a finite number of physical goods. Overselling occurs when an e-commerce platform promises more inventory to online customers than physically exists in the warehouse, forcing humiliating order cancellations, customer frustration, and warehouse inventory adjustment write-offs.

3. **Multi-Layered Enforcement Architecture:**
   - *Database Schema Layer:* The `stock_items` table defines a declarative check constraint: `CHECK((on_hand - reserved) >= 0)`. Any SQL command that would push reserved past on-hand is immediately aborted by the database engine.
   - *Concurrency Isolation Layer:* The checkout service executes an atomic conditional update:
     ```sql
     UPDATE stock_items 
     SET reserved = reserved + :qty, version = version + 1 
     WHERE sku = :sku AND region_id = :region_id AND (on_hand - reserved) >= :qty;
     ```
   - *Lease Expiry Reconciliation:* When a reservation expires after 15 minutes, the expiry worker decrements `reserved`, returning stock to the public pool. If a late payment callback arrives for an expired order and the item has already been resold, the system **refuses to mark the order `PAID`**, transitions it to `NEEDS_REFUND`, and queues an automatic refund, guaranteeing that physical stock is never oversold.

4. **Empirical Evidence:**
   Validated in `tests/test_t1_stock_contention.py` (competing concurrent buyers for the final unit) and `tests/test_t7_late_payment_expiry.py` (late payment callback after inventory resale).

---

## Verification Prompt 3: Describe How a Failed Courier Synchronization Remains Recoverable

### Failure Scenario & Architectural Recovery Protocol

1. **The Problem:**
   A customer's payment is confirmed, and the order is marked `PAID`. At that exact millisecond, the third-party logistics API (e.g., FedEx or DHL) experiences a momentary network socket timeout, DNS failure, or 503 Service Unavailable.

2. **The Flawed Solution (Why Naive Approaches Fail):**
   If the application makes a synchronous HTTP call inside the payment transaction, a courier timeout causes the entire database transaction to roll back—cancelling a legitimately paid order. Alternatively, if the transaction commits before the network call and the network call fails immediately after, the customer is billed, but the order is never registered with the courier (silent drop).

3. **The Implemented Outbox Recovery Solution:**
   - **Step 1 (Atomic Local Commit):** Within the payment callback transaction, the system writes a row to `outbox_intents` with `purpose = 'COURIER_DISPATCH'`, `status = 'PENDING'`, and a pre-allocated UUID: `correlation_key`. The payment callback responds to the gateway immediately in under 20 ms.
   - **Step 2 (Asynchronous Worker Attempt):** The background outbox worker polls pending intents using `SELECT ... FOR UPDATE SKIP LOCKED`. It invokes the Courier API with the `correlation_key`.
   - **Step 3 (Failure Handling & Backoff):** If the courier API times out, the worker catches the exception. The intent remains in `status = 'PENDING'`, `attempts` is incremented to 1, and `next_retry_at` is scheduled using exponential backoff ($2^{\text{attempts}}$ seconds). The order remains safely `PAID`.
   - **Step 4 (Reconciliation Before Retry):** When the worker wakes up for the retry, it **does not blindly invoke the courier booking endpoint again**. It first queries the courier API: `GET /v1/shipments?correlation_key={UUID}`.
     - If the courier actually recorded the parcel during the previous attempt (acknowledgement dropped in flight), the worker retrieves the existing tracking number and marks the intent `COMPLETED`.
     - If the courier has no record, the worker re-transmits the booking request.
   - **Step 5 (Final Completion):** The intent transitions to `COMPLETED`, carrier tracking number `TRK-...` is persisted, and the customer UI displays live tracking milestones.

4. **Empirical Evidence:**
   Demonstrated and verified in `tests/test_t5_courier_retry.py`. In Run 1 with simulated timeout, the intent remained `PENDING` with `attempts = 1`. In Run 2 with restored network, the worker reconciled and completed booking with tracking number `TRK-DB3AE309`.
