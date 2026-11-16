# Task 6: Part B – Revised Architecture and Redesigned Responsibilities

In response to the 12-region expansion, 500 simultaneous users, 1,000 events/minute, and intermittently disconnected warehouse scanners, the baseline modular architecture was redesigned to enhance horizontal scalability, data isolation, and edge resilience without violating financial budget constraints.

---

## 1. Architectural Evolution: Horizontally Replicated Modular Monolith with Read Models
Rather than introducing a chaotic mesh of 10+ distributed microservices (which would violate the limited infrastructure budget and create eventual consistency nightmares), the revised architecture preserves the **Modular Monolith core** while scaling stateless and read components:

1. **Horizontally Replicated Stateless Application Tier:** The FastAPI backend is scaled horizontally across multiple stateless container replicas (`fastapi-backend-1`, `fastapi-backend-2`, ..., `fastapi-backend-N`) placed behind an Nginx reverse proxy employing round-robin HTTP load balancing. Any replica can handle any user request because session state is encapsulated in signed JWTs.
2. **Regional Policy Registry with Versioning:** Regional rules (tax rates, shipping charges, refund limits) are modeled as versioned immutable records. Orders snapshot `policy_version`, ensuring that modifying a European VAT rate does not retroactively rewrite historical transaction records or invalidate existing financial audits.
3. **Dedicated Reporting Read Models & Summary Tables:** Analytical queries from Store Managers are decoupled from operational checkout transactions. Summary tables (`regional_sales_summary`, `inventory_turnover_summary`) are updated asynchronously, eliminating table contention on `orders` and `stock_items`.
4. **Edge Scanner Synchronization Gateway:** A specialized ingestion endpoint (`/api/scanner/sync-batch`) ingests replayed scan bursts from handheld terminals, performing atomic batch deduplication and staleness evaluation before touching inventory balances.
5. **Server-Validated Refund Authority:** Regional client dashboards and warehouse terminals can record and queue refund requests, but the global state strictly remains **`REQUESTED` (Pending)**. The central server validates the reviewer's authenticated role, geographic assignment, monetary threshold, and four-eyes rule before transitioning to `APPROVED`.

---

## 2. Redesigned Component Responsibilities and Data Ownership

| Component | Redesigned Architectural Responsibility | Data Ownership & State Enforcement |
| :--- | :--- | :--- |
| **Nginx Reverse Proxy** | Load balances inbound HTTPS traffic across API replicas; terminates TLS; enforces rate limiting per IP; routes static React assets. | Stateless configuration; manages upstream container health checks. |
| **Stateless FastAPI Replicas** | Process authenticated REST requests; evaluate JWT RBAC; compute order pricing; execute atomic stock reservations; validate webhook signatures. | Stateless. Zero in-memory session caches; all transactional state is committed to PostgreSQL. |
| **Policy Registry Module** | Maintains versioned policy configurations across 12 regions (`US-EAST` to `MEA-UAE`). Exposes active policy lookup and audited administrative updates. | Authoritative owner of `regional_policies`. Guarantees policy immutability via incremental versioning. |
| **Scanner Ingestion Gateway** | Ingests offline barcode batches from edge scanners; filters stale observations (> 24 hours); deduplicates by `(node_id, event_id)`. | Authoritative owner of `scanner_event_logs`. Updates `stock_items` atomically. |
| **Central PostgreSQL 16 DB** | Primary transactional authority. Coordinates serializable transactions, row-level locks, foreign keys, and outbox tables. | Authoritative owner of all relational entities. Connection pooling managed via PgBouncer. |
| **Outbox Integration Worker** | Polls `outbox_intents` using `FOR UPDATE SKIP LOCKED`; routes dispatch requests to regional carrier APIs; executes exponential backoff. | Reads and updates `outbox_intents`. Reconciles by `correlation_key` before retries. |
| **Reporting Aggregator** | Computes consolidated cross-regional summaries; aggregates revenue, tax, and returns by region; serves read-only manager views. | Maintains read-only summary projections without locking transactional tables. |
