# ADR-002: Implementation of Transactional Outbox Pattern for External Integrations

## Status
Accepted

## Context and Problem Statement
When a customer's order is verified as paid, the platform must notify external partner systems—specifically, the third-party Courier Logistics API to register a shipment and generate a tracking number. Similarly, approved refunds must be transmitted to the Payment Gateway.

If the application makes a synchronous HTTP call to the external courier API within the payment callback request:
1. An external network timeout or 503 error leaves the system in an ambiguous state: did the courier register the parcel or not?
2. If the external call succeeds but the local database transaction fails or crashes before committing, the courier dispatches a parcel for an order marked unpaid.
3. If the local transaction commits first and the network call fails immediately after, the customer is billed but no courier booking exists (silent intent drop).
4. Synchronous third-party HTTP calls block backend worker threads, causing connection pool exhaustion during traffic surges.

How can the platform reliably synchronize with external partner APIs without sacrificing local transactional integrity or thread availability?

## Decision Drivers
- Guarantee that no courier dispatch or refund intent is dropped due to partner downtime (At-Least-Once Delivery).
- Prevent duplicate courier bookings or double refund disbursements (Idempotent Retry).
- Decouple external network latency from customer-facing checkout and webhook callback threads.
- Avoid introducing heavyweight message brokers (Kafka/RabbitMQ) for a modest engineering team.

## Considered Alternatives
1. **Synchronous Direct HTTP Calls in Request Thread:** Lowest code complexity, but suffers from thread starvation, failure coupling, and silent intent loss.
2. **Dedicated Message Broker Cluster (RabbitMQ / Apache Kafka):** Industry-standard distributed messaging, but introduces severe operational complexity (broker clustering, partition monitoring, schema registries) unsuitable for a modest team.
3. **Transactional Outbox Pattern with Relational Polling Worker:** Storing an `outbox_intents` row in the same PostgreSQL transaction as the business state change, processed asynchronously by a background daemon.

## Decision Outcome
Chosen option: **Transactional Outbox Pattern with PostgreSQL Table and Background Worker**.

### Positive Consequences
- **Atomicity:** The local business state (`Order.state = PAID`) and the external integration intent (`COURIER_DISPATCH`) commit in the exact same database transaction. An intent is physically impossible to drop if the order commits.
- **Immediate Response Times:** The payment callback handler commits and returns HTTP 200 to the payment gateway in under 20 ms without waiting for courier network calls.
- **Controlled Retry with Exponential Backoff:** The background worker daemon claims pending intents using `SELECT ... FOR UPDATE SKIP LOCKED`, executing retries with deterministic backoff.
- **Correlation Key Reconciliation:** Each outbox intent carries an immutable `correlation_key` (UUID). If a timeout occurs, the worker queries the courier API by correlation key before attempting a new booking, guaranteeing zero duplicate shipments.

### Negative Consequences and Mitigations
- **Delayed External Visibility:** Courier tracking numbers are not available instantaneously at the exact millisecond of checkout; customers initially see "Paid, Shipment Pending".
  - *Mitigation:* The customer frontend uses polling or short intervals to refresh tracking milestones as soon as the outbox worker completes the booking.
- **Worker Process Monitoring:** A hung or crashed worker process could cause an unnoticed outbox backlog.
  - *Mitigation:* The worker health status and queue backlog depth are exposed via `/api/health` and audited periodically.
