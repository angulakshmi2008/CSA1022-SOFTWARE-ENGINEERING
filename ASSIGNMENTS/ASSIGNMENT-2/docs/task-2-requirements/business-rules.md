# Task 2: Business and Order Rules Specification

The Omnichannel Order Fulfilment Platform enforces the following formal business and operational rules across its order lifecycle:

---

### Rule 1: Authoritative Server-Side Pricing and Tax Calculation
1. The client browser or mobile application submits an array of `{ sku, quantity }` items.
2. The server queries the authoritative `products` table for unit base prices. Client-supplied price parameters are completely ignored.
3. The server inspects the customer's selected delivery region to retrieve active policy parameters from `regional_policies`:
   - `tax_rate` (e.g., 0.08 for US-EAST, 0.20 for UK-SOUTH, 0.19 for EU-CENTRAL).
   - `shipping_fee` (e.g., \$5.00 flat fee, or waived if subtotal > \$100.00).
4. The final order total is computed as:
   $$\text{Subtotal} = \sum (\text{Quantity}_i \times \text{UnitPrice}_i)$$
   $$\text{TaxAmount} = \text{Subtotal} \times \text{TaxRate}$$
   $$\text{OrderTotal} = \text{Subtotal} + \text{ShippingFee} + \text{TaxAmount}$$
5. The `tax_rate`, `shipping_fee`, and `policy_version` are snapshotted into the `orders` and `order_lines` tables to preserve historical immutability.

---

### Rule 2: Single Customer Ownership and Data Isolation
1. An order has exactly one immutable customer owner (`owner_id`).
2. When any customer endpoint (`GET /api/orders`, `GET /api/orders/{id}`) is invoked, the server filters orders by the authenticated caller's `user_id`.
3. If an authenticated user attempts to inspect or mutate an order where `order.owner_id != caller.user_id`, the system immediately aborts with HTTP 403 Forbidden.
4. Support agents and store managers can inspect orders only via designated staff endpoints that strip sensitive billing fields and apply redaction filters.

---

### Rule 3: Atomic Stock Reservation and 15-Minute Expiry
1. Stock availability is defined as:
   $$\text{AvailableQuantity} = \text{OnHand} - \text{Reserved}$$
2. The system enforces the invariant:
   $$\text{AvailableQuantity} \ge 0$$
3. When an order is placed (`state = PLACED`), a reservation record is created with `expires_at = CURRENT_TIMESTAMP + 15 MINUTES`.
4. The inventory row is updated atomically using a conditional SQL statement:
   ```sql
   UPDATE stock_items 
   SET reserved = reserved + :qty, version = version + 1 
   WHERE sku = :sku AND (on_hand - reserved) >= :qty;
   ```
5. If the customer does not complete payment within 15 minutes, a background expiry worker marks the reservation as `EXPIRED` and decrements `reserved`, restoring availability to the public catalogue.

---

### Rule 4: Permitted Order Lifecycle Transitions and Guards
1. Permitted order status transitions strictly follow:
   $$\text{PLACED} \longrightarrow \text{PAID} \longrightarrow \text{PACKED} \longrightarrow \text{DISPATCHED} \longrightarrow \text{DELIVERED} \longrightarrow \text{CLOSED}$$
2. **Cancellation Guard:** An order may transition from `PLACED` to `CANCELLED` only prior to payment confirmation. Once marked `PAID`, cancellation is prohibited; customers must proceed through the returns workflow.
3. **Dispatch Guard:** Transition to `DISPATCHED` requires two preconditions:
   - Order state must currently be `PACKED`.
   - The order must have verified payment (`state == PAID` previously) and a recorded pick confirmation from an authorized picker.
   - Any attempt to dispatch an unpaid or unpicked order returns HTTP 400 Bad Request.

---

### Rule 5: Dispatch Service Level Agreement (SLA)
1. The target dispatch deadline is **24 hours after payment confirmation, measured in UTC**.
2. A database timestamp `dispatch_due_at = paid_at + INTERVAL '24 hours'` is persisted upon payment receipt.
3. The warehouse dashboard visually flags and prioritizes orders nearing or exceeding their 24-hour dispatch SLA window.

---

### Rule 6: Duplicate Payment Webhook Deduplication
1. Payment gateways operate under at-least-once delivery semantics.
2. Webhook callbacks arriving at `/api/payments/callback` must present a valid HMAC-SHA256 signature in the `X-Signature` header.
3. The callback payload contains `(gateway_id, event_id, order_id, amount, status)`.
4. The system attempts an atomic insert into the `payment_events` table, which possesses a database-enforced unique constraint `UNIQUE(gateway_id, event_id)`.
5. If a duplicate event arrives:
   - The database unique constraint is violated.
   - The transaction catches the unique collision and returns the previously persisted outcome (`HTTP 200 OK - Duplicate event acknowledged`).
   - No secondary state changes, duplicate outbox intents, or double order confirmations occur.

---

### Rule 7: Segregation of Duties and Approval-Gated Refunds
1. The return and refund lifecycle maintains separate status tracking:
   $$\text{REQUESTED} \longrightarrow \text{APPROVED} \text{ / } \text{REJECTED} \longrightarrow \text{EXECUTING} \longrightarrow \text{EXECUTED} \text{ / } \text{FAILED}$$
2. **Threshold Governance:**
   - Any refund request where $\text{Amount} \le \text{Threshold}$ (default \$50.00) may be approved via automated policy checks if the return condition is verified.
   - Any refund request where $\text{Amount} > \text{Threshold}$ requires explicit review and approval by an authenticated user possessing the `FINANCE_REVIEWER` role.
3. **Four-Eyes Principle:** The actor who requested the return (`requested_by`) cannot approve the refund (`approved_by`).
4. **Execution Precondition:** A refund cannot execute against the external payment gateway unless its database state is strictly `APPROVED`.
5. **Failure Resilience:** If the external payment gateway call fails or times out during refund execution, the refund state is transitioned to `FAILED`. Crucially, **the prior approval record remains intact**, allowing controlled retry with a stable idempotency key without requiring re-approval.
