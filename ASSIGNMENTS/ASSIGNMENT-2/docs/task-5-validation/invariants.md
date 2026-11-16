# Task 5: System Invariants

The Omnichannel Order Fulfilment Platform enforces the following seven fundamental business and safety invariants. These invariants must hold true across all operational states, concurrency levels, and external partner failure modes:

---

### Invariant 1: Uniqueness of Payment Events (Zero Duplicate Billing)
$$\forall (g, e) \in \text{PaymentEvents}, \quad \text{COUNT}(g, e) \le 1$$
*Specification:* A specific external payment gateway event identity pair `(gateway_id, event_id)` can result in at most one recorded payment entry, at most one order status transition to `PAID`, and at most one downstream dispatch intent. Repeated delivery of an identical event identity must return the previously cached outcome without executing any secondary business effects.
*Enforcement:* Database-level composite unique constraint `UNIQUE(gateway_id, event_id)` within the callback transaction.

---

### Invariant 2: Non-Negative Available Inventory (Zero Physical Oversell)
$$\forall s \in \text{StockItems}, \quad \text{AvailableStock}(s) = \text{OnHand}(s) - \text{Reserved}(s) \ge 0$$
*Specification:* Available inventory can never drop below zero under any concurrency level or race condition. When two or more buyers concurrently compete for the final unit, at most one buyer can successfully commit the reservation.
*Enforcement:* Database check constraint `CHECK((on_hand - reserved) >= 0)` combined with atomic conditional updates:
```sql
UPDATE stock_items 
SET reserved = reserved + :qty 
WHERE sku = :sku AND (on_hand - reserved) >= :qty;
```

---

### Invariant 3: Dual-Control Refund Authorization Gate (No Unapproved Outflows)
$$\forall r \in \text{RefundRequests}, \quad (\text{state} = \text{'EXECUTED'}) \implies (\text{state} = \text{'APPROVED'} \land \text{approved\_by} \ne \text{NULL})$$
*Specification:* An unapproved refund request can never be transmitted to the payment gateway or marked `EXECUTED`. Any refund exceeding the regional threshold (default \$50.00) strictly requires an independent, authenticated `FINANCE_REVIEWER` approval. Furthermore, the actor who requested the refund cannot be the approver (strict segregation of duties).
*Enforcement:* Server-side state guard in `refund_service.py` rejecting execution requests if `state != APPROVED`.

---

### Invariant 4: Customer Resource Ownership Isolation (Confidentiality)
$$\forall o \in \text{Orders}, \quad \text{Caller} \ne o.\text{owner\_id} \land \text{Caller}.\text{role} = \text{'CUSTOMER'} \implies \text{Access Denied (HTTP 403)}$$
*Specification:* A retail customer cannot view, alter, or cancel an order belonging to any other customer. Support agents can view order details only through redacted/masked projections that exclude credit card numbers and full contact details.
*Enforcement:* Server-side principal verification in API route dependencies evaluating `order.owner_id == authenticated_user_id`.

---

### Invariant 5: Guarded Dispatch Prerequisites (Pick & Payment Integrity)
$$\forall o \in \text{Orders}, \quad (o.\text{state} = \text{'DISPATCHED'}) \implies (o.\text{state}_{\text{prev}} = \text{'PACKED'} \land \text{PickConfirmed} = \text{TRUE})$$
*Specification:* An order cannot be dispatched unless it has been verified as paid and physically retrieved and confirmed by an authorized warehouse picker. Orders cannot transition directly from `PLACED` to `DISPATCHED`.
*Enforcement:* State transition validator in `warehouse_service.py` enforcing sequential lifecycle checks.

---

### Invariant 6: Resilient Outbox Persistence (Zero Dropped Handshakes)
$$\forall o \in \text{Orders}, \quad (o.\text{state} = \text{'PAID'}) \implies \exists i \in \text{OutboxIntents} \text{ s.t. } i.\text{aggregate\_id} = o.\text{order\_id}$$
*Specification:* When an order transitions to `PAID`, a corresponding external shipment integration intent is guaranteed to be persisted in the `outbox_intents` table in the exact same database transaction, ensuring no courier booking intent is lost during server crashes or network outages.
*Enforcement:* Local transactional atomicity in PostgreSQL/SQLite.

---

### Invariant 7: Idempotent External Retries (Zero Duplicate Carrier/Gateway Calls)
$$\forall i \in \text{OutboxIntents}, \quad \text{Retries}(i) \text{ share immutable } i.\text{correlation\_key}$$
*Specification:* Across all network retries and worker restarts, external API requests to third-party couriers and payment gateways reuse an immutable, pre-allocated correlation key (UUID). Third-party systems use this key to prevent duplicate parcel shipments or double refund payouts.
*Enforcement:* Pre-allocated UUID correlation keys stored in outbox intents and verified by reconciliation queries before re-transmission.
