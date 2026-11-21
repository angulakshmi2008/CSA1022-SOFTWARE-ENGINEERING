# Scope Boundaries, Inclusions, and Exclusions

## 1. System Context and Architectural Boundaries
The Smart Campus Facility Booking and Maintenance Platform addresses core day-to-day facility management and maintenance operations across modern campus infrastructure. In accordance with sound software engineering principles and the one-week delivery constraint, the project establishes unambiguous boundaries separating production core capabilities from speculative or out-of-scope enhancements.

---

## 2. Inclusions (First Release Target)

1. **Facility Management & Catalogue:**
   - Multi-campus inventory support (configured for 6 campuses).
   - Facility categorization (Lecture Halls, Computer Laboratories, Bio-Chem Research Labs, Seminar Rooms, Collaborative Spaces).
   - Capacity tracking and active/maintenance state management.
   - Restricted flag gating sensitive laboratories behind authorized approvals.

2. **Booking & Calendar Lifecycle:**
   - Visual calendar view displaying occupied slots.
   - Half-open time range reservation (`[start_at, end_at)`).
   - Strict database-enforced non-overlap constraint preventing double-booking under concurrency.
   - Full lifecycle states: `requested`, `approved`, `confirmed`, `in_use`, `completed`, `cancelled`.
   - Idempotent booking submission using client-generated request tokens.

3. **Sensor Intake & Telemetry Ingestion:**
   - RESTful ingestion of timestamped sensor readings (temperature, humidity, vibration, power draw).
   - Deterministic duplicate suppression via unique `(source_id, event_id)` constraints.
   - Threshold-breach detection triggering automatic maintenance work item creation.

4. **Maintenance Queue & Explainable Triage:**
   - Priority assessment via transparent $3 \times 3$ impact-urgency matrix ($M1$ Critical to $M4$ Low).
   - Deterministic keyword and threshold classification engine explaining the exact rule matched.
   - Technician assignment and workload tracking.
   - Inspection log append and evidence-gated resolution workflow (mandatory notes enforced with HTTP 422).

5. **Approvals & Governance:**
   - Dedicated approval queue for Department Approvers.
   - Rejection and approval recording with required justification.
   - Immutable audit trail logging actor, timestamp, entity ID, action, and before/after states within ACID transactions.

6. **DevOps & Integration Hub:**
   - Durable `IntegrationIntent` outbox tracking external developer issues (e.g., Jira / GitHub issue sync).
   - Idempotency key handling and timeout reconciliation pattern.

7. **Deployment & Version Control:**
   - Git repository with branching model, conventional commits, deliberate conflict resolution, and release tag `v1.0.0`.
   - Multi-container Docker Compose configuration with PostgreSQL named persistent volume.

---

## 3. Explicit Exclusions (Deferred to Future Iterations)

| Excluded Capability | Justification for Exclusion | Alternative Strategy in First Release |
|---|---|---|
| **Paid Facility Reservations & Financial Gateways** | Campus facilities operate on academic departmental allocations rather than direct payment processing. Financial settlement introduces PCI-DSS compliance overhead unnecessary for academic scheduling. | Facility bookings use role-based quotas and departmental approval instead of credit card/banking transactions. |
| **Predictive AI / Black-Box ML Occupancy Forecasting** | Machine learning models trained on non-existent campus historical data produce unverifiable hallucinations. Faculty evaluation requires transparent, auditable triage logic. | Rule-based deterministic classification engine mapping explicit keywords and sensor thresholds to categories and priorities with visible explanations. |
| **Autonomous Technician Dispatch Without Human Review** | Disregarding human-in-the-loop review can lead to false dispatches from malfunctioning sensor hardware, disrupting campus contractors. | Sensor breaches create tickets in `intake`/`triaged` status, requiring facility manager assignment and verification. |
| **Unauthenticated / Raw IoT Hardware Protocol Collectors** | Direct MQTT/CoAP broker connections to physical embedded microcontrollers require complex field hardware gateways outside the assignment scope. | Controlled RESTful telemetry ingestion endpoint (`POST /api/sensor-events/`) accepting standardized JSON payloads with strict idempotency identity. |
| **Multi-Region Active-Active Distributed Orchestration (Kubernetes)** | Unnecessary operational complexity, latency overhead, and resource consumption for a single-institution 6-campus deployment. | Reproducible Docker Compose multi-container setup with two stateless backend API instances sharing a single ACID-compliant PostgreSQL database. |
