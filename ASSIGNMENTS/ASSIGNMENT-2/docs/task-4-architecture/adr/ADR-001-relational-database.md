# ADR-001: Selection of Relational Transactional Storage (PostgreSQL)

## Status
Accepted

## Context and Problem Statement
The Omnichannel Order Fulfilment Platform coordinates financial transactions, inventory counts, order status transitions, approval workflows, and audit histories. Under peak concurrent checkout conditions, competing customers attempt to reserve the final remaining unit of a SKU, and duplicate webhook callbacks arrive from payment gateways. The system must guarantee that:
1. Available inventory (`on_hand - reserved`) never becomes negative.
2. Duplicate payment events are rejected with absolute consistency.
3. Order creation and stock reservation commit atomically or abort completely.

What persistence technology should serve as the primary source of truth for the platform?

## Decision Drivers
- Need for ACID transactions to coordinate multi-table mutations (order placement + stock reservation).
- Strict uniqueness enforcement for deduplication of external event IDs `(gateway_id, event_id)` and `(node_id, event_id)`.
- Support for row-level locking (`SELECT ... FOR UPDATE`) or atomic conditional updates.
- Mature indexing (B-Tree, Partial, Composite) to satisfy read latency targets.
- Low operational complexity for a small engineering team.

## Considered Alternatives
1. **Relational Database Management System (PostgreSQL 16):** Fully ACID-compliant, mature constraint enforcement, row-level locking, rich JSONB support for payload snapshots.
2. **Document-Oriented NoSQL Store (MongoDB):** Flexible document schema, native JSON handling. Supports multi-document transactions since v4.0, but lacks declarative relational foreign key cascades and requires higher operational discipline to prevent orphaned records.
3. **Distributed Key-Value Store (Redis + Event Log):** In-memory speed, but lacks durable multi-entity relational transactions and requires complex custom synchronization to guarantee disk persistence.

## Decision Outcome
Chosen option: **PostgreSQL 16**, because it provides native ACID transactional semantics, declarative unique constraints, row-level locking, and proven operational reliability.

### Positive Consequences
- **Zero Inventory Invariant Violations:** Atomic transactions and conditional SQL updates guarantee that two buyers cannot oversell the final unit of stock.
- **Declarative Webhook Deduplication:** Enforcing a composite unique index on `payment_events(gateway_id, event_id)` delegates duplicate rejection directly to the database engine, eliminating race windows.
- **Relational Integrity:** Foreign keys guarantee that order lines, payments, audit events, and outbox intents cannot become orphaned.
- **Transactional Outbox Feasibility:** Business state changes and external integration intents can be written to disk in the exact same local transaction.

### Negative Consequences and Mitigations
- **Single Point of Bottleneck:** Central relational database capacity limits maximum vertical write throughput.
  - *Mitigation:* Heavy analytical queries (Store Manager reports) are decoupled from the transactional checkout path via read-only materialized summary tables, and connection pooling (PgBouncer/SQLAlchemy pool) is enforced.
- **Schema Migration Overhead:** Evolving table structures requires strict version-controlled database migrations (Alembic/Flyway).
