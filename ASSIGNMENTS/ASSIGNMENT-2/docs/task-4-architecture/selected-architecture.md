# Task 4: Detailed Design of the Selected Architecture

## 1. Architectural Style: Modular Monolith with Transactional Outbox
The selected architecture balances high transactional consistency with decoupled asynchronous integration. It is composed of three primary runtime subsystems:
1. **Stateless Application Tier (`backend-api`):** Python FastAPI service handling authenticated HTTP/REST client requests, executing business logic, and enforcing role authorization.
2. **Relational Persistence Tier (`postgres-db`):** PostgreSQL database acting as the single transactional source of truth, enforcing ACID guarantees, relational foreign keys, unique constraint deduplication, and outbox tables.
3. **Asynchronous Integration Worker (`outbox-worker`):** Independent background daemon continuously polling the `outbox_intents` table, executing third-party API handshakes (Courier API, Payment Gateway refunds) with backoff and correlation key reconciliation.

---

## 2. Module Responsibilities and Data Ownership

| Module Name | Domain Responsibilities | Managed Data Entities | Dependencies / Inbound Calls |
| :--- | :--- | :--- | :--- |
| **Auth & Security** | JWT generation, password hashing, role resolution, permission guard verification. | `users`, `user_roles` | Invoked by API middleware on all protected routes. |
| **Products & Catalog** | SKU definitions, category listings, base unit pricing. | `products` | Read by Cart, Checkout, and Inventory modules. |
| **Inventory & Reservation** | Atomic stock reservation, conditional quantity decrements, 15-minute lease expiry. | `stock_items`, `reservations` | Invoked synchronously by Order Service during checkout. |
| **Order Management** | Order state machine, lifecycle transitions, customer ownership verification, UTC dispatch SLA timers. | `orders`, `order_lines` | Ingests checkout requests; triggers inventory reservations and outbox events. |
| **Payment Integration** | Webhook callback signature verification (HMAC), payment idempotency deduplication. | `payment_events` | External Payment Gateway webhooks; marks orders `PAID`. |
| **Warehouse & Picking** | Pick list generation, warehouse zone filtering, pick confirmation, packing verification. | `orders` (state `PACKED`) | Invoked by Warehouse Pickers; guards physical dispatch. |
| **Courier Outbox & Tracking** | Persists shipment intents, executes asynchronous courier registration, records tracking tokens. | `outbox_intents`, `courier_tracking` | Triggered by `PAID` transition; polled by background worker. |
| **Returns & Refunds** | Return request ingestion, \$50.00 threshold evaluation, finance review approval/rejection, refund execution. | `refund_requests` | Invoked by Support Agents and Finance Reviewers. |
| **Regional Policy Engine** | 12-region tax rates, regional shipping fees, refund approval thresholds, policy versioning. | `regional_policies` | Ingested by Order pricing and Refund evaluation. |
| **Scanner Edge Sync** | Ingests offline barcode scan batches, deduplicates by `(node_id, event_id)`, reconciles physical counts. | `scanner_event_logs` | Handheld warehouse edge scanners. |
| **Reporting & Analytics** | Aggregates revenue, tax collected, inventory turnover, and refund totals across regions. | Read models / materialized queries | Invoked by Store Managers and Regional Directors. |
| **Audit Logging** | Append-only audit logging recording actor, action, timestamp, entity version, and details. | `audit_events` | Invoked synchronously across all mutating domain operations. |

---

## 3. Concurrency, Deduplication, and Failure Recovery Protocols

### Stock Reservation Under High Concurrency
To eliminate overselling race conditions when multiple customers compete for the final stock unit:
- The checkout endpoint begins a local database transaction.
- An atomic SQL update is executed against `stock_items`:
  ```sql
  UPDATE stock_items 
  SET reserved = reserved + :qty, version = version + 1 
  WHERE sku = :sku AND (on_hand - reserved) >= :qty;
  ```
- If the rows affected is 0, the transaction immediately aborts, and the caller receives HTTP 409 Conflict (`Insufficient Stock`).
- If successful, a `reservations` record is created with `expires_at = NOW() + 15m`.

### Duplicate Payment Webhook Deduplication
Payment callbacks can arrive repeatedly or concurrently due to network retries.
- Webhooks arrive at `POST /api/payments/callback`.
- The handler attempts to insert into `payment_events`, which defines a composite unique constraint `UNIQUE(gateway_id, event_id)`.
- If a duplicate event arrives, the database throws a unique key violation. The transaction catches the exception, verifies the existing payment status, and returns HTTP 200 with the recorded outcome without updating the order state or inserting secondary outbox intents.

### Transactional Outbox Pattern for Third-Party Couriers
Directly invoking the external Courier API inside the payment callback transaction introduces a severe architectural vulnerability: if the courier API takes 8 seconds to respond or times out, the database connection is held open, exhausting backend thread pools. If the database commits but the network crashes before courier registration, the order is paid but never shipped.
- In the selected architecture, when payment is verified, the system writes a row to `outbox_intents` **in the exact same database transaction** as the order state change (`PAID`).
- The asynchronous worker polls `outbox_intents` where `status = 'PENDING'`.
- The worker invokes the external courier API with an idempotency key (`correlation_key`).
- If the courier API times out, the intent remains `PENDING` with an incremented attempt count and exponential backoff.
- On retry, the worker queries the courier API by correlation key to reconcile state before issuing a duplicate booking.
