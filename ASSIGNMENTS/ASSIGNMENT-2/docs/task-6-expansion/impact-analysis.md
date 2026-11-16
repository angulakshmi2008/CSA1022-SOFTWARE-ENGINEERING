# Task 6: Part A – Impact Diagnosis of the Expanded Operational Scenario

The transition from a bounded initial deployment to an enterprise multi-regional architecture profoundly affects existing functional requirements, non-functional quality attributes, planning assumptions, and component responsibilities.

---

## 1. Impact on Functional Requirements

| Requirement ID | Affected Domain | Initial Behavior (3 Regions) | Expanded Impact & Architectural Adaptation (12 Regions) |
| :--- | :--- | :--- | :--- |
| **FR04** | Pricing & Tax Engine | Computed tax using a static table for 3 domestic hubs. | Must support 12 distinct international jurisdictions (e.g., VAT in UK-SOUTH and EU-CENTRAL, GST in AUS-EAST, state sales tax in US-EAST). Requires versioned policies so historical orders preserve their tax total regardless of statutory tax changes (`FR13`). |
| **FR07** | Warehouse Pick Lists | All pickers queried a single operational order queue. | Warehouse pick lists must be strictly partitioned by `region_id`. Pickers in Frankfurt (`EU-CENTRAL`) must not be assigned or see orders awaiting dispatch in Sydney (`AUS-EAST`). |
| **FR10** | Refund Governance | Uniform $50.00 approval threshold across all orders. | Refund limits vary by region to reflect currency conversions and local legal frameworks. Disconnected edge scanners or regional portals queuing approvals locally must be marked `PENDING` until validated by the central server. |
| **FR11** | External Outbox | Single worker polling synchronous intents. | Multi-carrier routing: Outbox worker must route dispatch intents to regional logistics APIs based on order `region_id`, managing separate rate limits and failure domains. |
| **FR12** | Consolidated Reporting | Single-query SQL aggregations directly on `orders` table. | Running cross-regional analytical queries across 12 hubs directly on operational tables will lock rows and degrade checkout latency. Requires decoupled read models and summary tables. |
| **FR14 (New)**| Edge Scanner Ingestion | Assumed live, continuous WiFi connectivity. | Requires edge buffering, batch synchronization endpoints (`POST /api/scanner/sync-batch`), and deduplication by `(node_id, event_id)` to handle warehouse dead zones. |

---

## 2. Impact on Non-Functional Requirements (Quality Attributes)

1. **Performance & Latency (NFR01):**
   - *Initial Target:* 50 concurrent users, p95 < 800 ms.
   - *Expanded Target:* **500 concurrent users** and **1,000 events/minute**.
   - *Diagnosis:* At ~83.3 events/second peak, a single Python FastAPI process can become CPU-bound on JSON serialization and cryptographic JWT decoding. Database connection pools will saturate if threads block on external network I/O.
   - *Mitigation:* Deploy multiple stateless FastAPI container replicas behind an Nginx load balancer; enforce database connection pooling with short transaction windows and targeted B-Tree indexes.

2. **Transactional Consistency (NFR02):**
   - *Diagnosis:* High write velocity increases lock contention on popular SKUs. If 50 buyers contend for the same promotion in multiple regions, unindexed queries cause table-wide lock escalation.
   - *Mitigation:* Maintain regional partitioning of inventory rows (`PRIMARY KEY (sku, region_id)`). Row-level locking is isolated to the specific regional warehouse bin.

3. **Recoverability & Resilience (NFR03):**
   - *Diagnosis:* 1,000 events/min implies that a 10-minute carrier API outage creates a backlog of ~10,000 pending outbox intents.
   - *Mitigation:* The outbox worker must implement batch claiming (`SELECT ... FOR UPDATE SKIP LOCKED LIMIT 50`) and exponential backoff to prevent thundering herd recovery.

---

## 3. Revised Planning Assumptions

| ID | Initial Assumption | Revised Operational Assumption | Rationale |
| :--- | :--- | :--- | :--- |
| **A01** | Single logical region, modest deployment. | **12 discrete geographic operating regions** with local tax, shipping, and currency rules. | Accommodates enterprise expansion while maintaining centralized database control. |
| **A07** | 50 concurrent users, 100 events/min. | **500 simultaneous users, 1,000 events/min** (~16.7 events/sec avg, ~83.3 events/sec peak). | Explicitly treated as a **planning target** rather than proven system throughput. |
| **A08 (New)**| Continuous warehouse network coverage. | **Intermittently disconnected edge scanners** with local FIFO buffering capacity up to 5,000 events. | Acknowledges concrete physical reality of industrial warehouse dead zones. |
| **A09 (New)**| Uniform infrastructure budget. | **Limited infrastructure expenditure increase**; horizontal scaling must be justified by measured profiling. | Precludes costly multi-region distributed databases or managed Kafka clusters. |
