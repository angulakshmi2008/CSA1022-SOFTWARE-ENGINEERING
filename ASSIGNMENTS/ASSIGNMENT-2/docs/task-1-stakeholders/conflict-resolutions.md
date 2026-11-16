# Task 1: Stakeholder Conflicts and Justified Resolutions

During requirement elicitation, four fundamental stakeholder conflicts were identified where conflicting operational goals compete. Below are the reasoned trade-offs, engineering resolutions, and observable acceptance criteria.

---

### Conflict 1: Checkout Speed vs. Stock Accuracy and Concurrency Contention
- **Competing Stakeholders:** Customer (demands sub-second, frictionless checkout) vs. Warehouse Picker / Store Manager (demands 100% physical stock accuracy and zero overselling).
- **The Core Dilemma:** An asynchronous or optimistic checkout without strict stock reservation allows blisteringly fast response times (~100 ms). However, when multiple customers attempt to purchase the final unit of a product, naive systems oversell inventory, forcing order cancellations, customer frustration, and warehouse inventory adjustments. Conversely, heavy pessimistic locking across entire product tables introduces transaction serialization bottlenecks that degrade checkout responsiveness during traffic spikes.
- **Reasoned Architectural Resolution:** 
  Implement an **atomic, row-level transactional stock reservation with a 15-minute lease expiry**. 
  When a customer submits an order, the system executes an atomic conditional update:
  ```sql
  UPDATE stock_items 
  SET reserved = reserved + :qty, version = version + 1 
  WHERE sku = :sku AND (on_hand - reserved) >= :qty;
  ```
  If zero rows are updated, the product is genuinely out of stock, and the transaction is aborted immediately with HTTP 409 Conflict. A dedicated background expiry worker periodically inspects active reservations and releases unfulfilled units where `expires_at < CURRENT_TIMESTAMP` and order state is `PLACED`.
- **Acceptance Implication & Observable Criteria:** 
  In a concurrent race condition where two simultaneous buyers attempt to purchase the final remaining unit of a product, exactly one transaction succeeds (Order `PLACED`), and the second transaction is immediately rejected with an out-of-stock notification. Available stock (`on_hand - reserved`) never falls below zero under any concurrency level.

---

### Conflict 2: Frontline Support Visibility vs. Customer Privacy and PCI/GDPR Compliance
- **Competing Stakeholders:** Support Agent (requires comprehensive customer order history and shipping details to resolve complaints rapidly) vs. Customer / Compliance Officer (mandates least-privilege access and zero exposure of sensitive financial credentials).
- **The Core Dilemma:** Support staff frequently request complete visibility into transaction logs, including payment card details and billing addresses, to diagnose failed orders. However, exposing Primary Account Numbers (PAN), CVVs, or full payment authorization payloads violates PCI-DSS regulations and GDPR privacy safeguards, exposing the enterprise to data exfiltration risks.
- **Reasoned Architectural Resolution:**
  Enforce **server-side scoped projections and field-level masking**. 
  Support agents are granted read-only access to customer order status, order line items, and courier tracking numbers via dedicated support endpoints (`/api/support/orders`). Sensitive payment card data (PAN, CVV) is NEVER stored in the database. Payment transaction records contain only gateway reference tokens, masked card types (e.g., `Visa ending in 4242`), and gateway transaction identifiers. Customer phone numbers and addresses are partially masked in all support UI payloads.
- **Acceptance Implication & Observable Criteria:**
  A direct API query by a support agent returns masked order metadata. Direct access to raw payment card credentials is architecturally impossible because the database schema explicitly excludes cardholder data. Furthermore, cross-customer queries (Customer A attempting to view Customer B's order) are strictly rejected with HTTP 403 Forbidden.

---

### Conflict 3: Instantaneous Payment Confirmation vs. Distributed Integration Availability
- **Competing Stakeholders:** Customer (expects immediate confirmation upon completing the payment redirect) vs. Integration Engineer / Finance Reviewer (demands cryptographically verified, duplicate-free financial records).
- **The Core Dilemma:** Commercial payment gateways typically redirect the user's browser back to an e-commerce "success" page before or concurrently with transmitting an asynchronous server-to-server webhook callback. If the platform marks the order `PAID` merely because the client browser returned to `/checkout/success`, malicious users can forge client-side redirects to obtain goods without paying. Conversely, waiting synchronously for the webhook callback before displaying any response can hang the customer browser if external network latency spikes.
- **Reasoned Architectural Resolution:**
  Establish an explicit **`PAYMENT_PENDING` intermediate state and a Transactional Outbox pattern**.
  Upon order placement, the order is persisted with state `PLACED`. When the customer completes external gateway interaction, the client displays a pending confirmation status. The order status is transitioned to `PAID` **strictly and exclusively** upon receipt of a cryptographically signed server-to-server webhook callback at `/api/payments/callback`. The callback handler verifies the HMAC-SHA256 signature, matches the authorized amount, and records a unique constraint on `(gateway_id, event_id)`. Within the same atomic transaction, a shipment intent is inserted into the outbox table.
- **Acceptance Implication & Observable Criteria:**
  A client-side browser success redirect does not alter the order state in the database. Delivery of duplicate or repeated payment callbacks returns the recorded idempotent outcome without creating duplicate payment entries, duplicate outbox intents, or multiple order confirmations.

---

### Conflict 4: Rapid Customer Refund Turnaround vs. Internal Financial Control & Segregation of Duties
- **Competing Stakeholders:** Customer / Support Agent (desires instantaneous one-click refunds to maximize customer satisfaction) vs. Finance Reviewer / Internal Auditor (demands strict four-eyes verification and fraud deterrence).
- **The Core Dilemma:** Allowing support agents or automated bots to issue instant cash refunds without supervision creates massive financial vulnerability (employee collusion, unauthorized chargebacks). However, requiring human executive approval for every minor \$5.00 return causes support backlogs and customer dissatisfaction.
- **Reasoned Architectural Resolution:**
  Implement a **threshold-governed, multi-state refund lifecycle with hard segregation of duties**.
  Refund requests are separated into distinct states: `REQUESTED` -> `APPROVED` / `REJECTED` -> `EXECUTING` -> `EXECUTED` (or `FAILED`).
  1. Support agents are granted permissions only to submit a return request (`REQUESTED`).
  2. A configurable policy threshold (default \$50.00) is enforced on the server. Low-risk returns below the threshold can proceed via automated policy checks, but any refund exceeding \$50.00 mandates explicit human review by an authenticated `FINANCE_REVIEWER`.
  3. No user can approve a refund they requested.
  4. If a gateway refund execution call fails, the state transitions to `FAILED` while **retaining the prior approval record**, allowing safe, controlled retry using a stable idempotency key without requiring re-approval.
- **Acceptance Implication & Observable Criteria:**
  Any attempt by a customer or support agent to invoke the `/api/refunds/{id}/approve` endpoint is denied with HTTP 403 Forbidden. A failed refund gateway execution leaves the approval record intact and retries safely under the same correlation key.
