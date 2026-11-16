# Task 5: Formal Operation Contracts

Below are formal operation contracts specified in the style of Design by Contract (DbC) for the platform's three most critical transactional operations.

---

## 1. Operation Contract: `PlaceOrder`

### Operation Signature
`create_order(user_id: UUID, items: List[OrderLineItem], region_id: String) -> Order`

### Cross-Reference
- **Requirements:** `FR01`, `FR02`, `FR03`, `FR04`
- **UML Elements:** Use Case `UC2 (Place Order)`, Class `Order`, `StockItem`, `Reservation`

### Preconditions
1. The caller is an authenticated principal whose session token is cryptographically valid and not expired (`current_user != NULL`).
2. The `items` array contains at least one line item (`LEN(items) >= 1`).
3. For every item $i \in \text{items}$, the requested quantity is strictly positive ($i.\text{quantity} > 0$).
4. Every SKU listed exists in the active product catalogue (`product.is_active == TRUE`).
5. For every requested SKU in `region_id`, the currently available inventory satisfies the requested quantity:
   $$\text{on\_hand} - \text{reserved} \ge i.\text{quantity}$$
6. The specified `region_id` matches an active regional policy configuration.

### Postconditions
1. A new `Order` record is inserted with unique UUID `order_id`, `owner_id = user_id`, `state = 'PLACED'`, and `version = 1`.
2. Authoritative line item totals, tax amount, shipping fee, and grand total are calculated from server policy and persisted; client-supplied prices are completely disregarded.
3. For each order line, an active reservation record is created with `expires_at = CURRENT_TIMESTAMP + 15m`.
4. In `stock_items`, `reserved` is incremented by $i.\text{quantity}$, while `on_hand` remains unchanged.
5. Invariant Invariant 2 (`on_hand - reserved >= 0`) is preserved.
6. An append-only audit entry (`action = 'ORDER_PLACED'`) is inserted into `audit_events`.
7. **Failure Exception Handling:** If any SKU has insufficient available stock, the entire transaction rolls back; zero order rows or reservations are persisted, and the caller receives HTTP 409 Conflict.

---

## 2. Operation Contract: `ConfirmPayment`

### Operation Signature
`process_payment_callback(gateway_id: String, event_id: String, order_id: UUID, amount: Decimal, currency: String, signature: String) -> PaymentOutcome`

### Cross-Reference
- **Requirements:** `FR05`, `FR06`, `FR08`, `FR11`
- **UML Elements:** Sequence Diagram `Payment Callback`, Class `PaymentEvent`, `IntegrationIntent`

### Preconditions
1. The incoming webhook request presents an `X-Signature` header containing a valid HMAC-SHA256 signature generated using the pre-shared secret and request raw payload.
2. The `order_id` references an existing order record in the database.
3. The received `amount` matches the stored `order.total_amount` exactly within ±$0.01 precision.
4. The event identity pair `(gateway_id, event_id)` is either:
   - Completely unseen (first delivery), OR
   - Already recorded in `payment_events` (duplicate delivery).

### Postconditions
1. **First Delivery Path:**
   - A new row is inserted into `payment_events` capturing `gateway_id`, `event_id`, `order_id`, `amount`, and `verified_at`.
   - **Reservation Active Case:** If the order's stock reservation is still active, order state is updated from `PLACED` to `PAID`, `paid_at` is set to current time, and `dispatch_due_at` is set to `paid_at + 24h (UTC)`. An outbox intent (`purpose = 'COURIER_DISPATCH'`) is inserted into `outbox_intents` with an immutable `correlation_key`.
   - **Reservation Expired Case (Revision):** If the reservation expired, the system attempts to re-reserve stock. If inventory is unavailable, the order state is updated to `NEEDS_REFUND`, and an automated refund request is queued. Physical stock is NOT oversold.
   - An audit record (`action = 'ORDER_PAID'` or `'ORDER_NEEDS_REFUND'`) is committed.
   - The gateway receives HTTP 200 OK with `status = 'PAYMENT_CONFIRMED'`.
2. **Duplicate Delivery Path:**
   - The database unique constraint on `(gateway_id, event_id)` prevents secondary insertion.
   - The transaction aborts changes and returns the previously recorded outcome.
   - No secondary state changes or duplicate outbox intents are generated.
   - The gateway receives HTTP 200 OK with `status = 'DUPLICATE_ACKNOWLEDGED'`.

---

## 3. Operation Contract: `ExecuteRefund`

### Operation Signature
`execute_refund_intent(refund_id: UUID, caller: User, simulate_failure: Boolean) -> RefundRecord`

### Cross-Reference
- **Requirements:** `FR10`, `FR12`
- **UML Elements:** State Machine `Refund State View`, Class `RefundRequest`

### Preconditions
1. The `refund_id` exists in the database.
2. The caller possesses an authenticated session with the `FINANCE_REVIEWER` or `ADMINISTRATOR` role.
3. The refund's current state is strictly `APPROVED` (or `FAILED` undergoing controlled retry).
4. The refund's `approved_by` field references an authorized finance reviewer distinct from `requested_by`.
5. The refund entity carries an immutable, pre-allocated `idempotency_key`.

### Postconditions
1. **Gateway Success Path:**
   - The external payment gateway refund API is invoked using `idempotency_key`.
   - Upon receiving HTTP 200/201 from the gateway, the refund state is transitioned to `EXECUTED`.
   - The associated `orders` record is transitioned to `CLOSED`.
   - An audit entry (`action = 'REFUND_EXECUTED'`) is appended.
2. **Gateway Failure / Timeout Path (Revision):**
   - If the gateway returns a 5xx error or connection timeout, the refund state is transitioned to `FAILED`.
   - **Critical Invariant Preservation:** The `approved_by` reference and original approval timestamp are **strictly preserved** in the database row.
   - An audit entry (`action = 'REFUND_EXECUTION_FAILED'`) is logged.
   - The refund remains eligible for immediate controlled retry without requiring re-approval.
