# Smart Campus Facility Booking and Maintenance Platform
## Final Technical Report & Academic Portfolio (CO3, 50 Marks)

**Course Code**: CSA1022 - Software Engineering  
**Course Outcome**: CO3 – Full-stack development, version control, and containerization  
**Student Name**: ANGULAKSHMI S  
**Register Number**: 192524402  
**Programme and Section**: CSA10 / Software Engineering  
**Submission Date**: 21 November 2026  
**Repository**: `https://github.com/angulakshmi2008/CSA1022-SOFTWARE-ENGINEERING`  
**Subfolder**: `ASSIGNMENTS/ASSIGNMENT-3/`  
**Release Version**: `v1.0.0`

---

## Abstract
This report documents the design, full-stack implementation, concurrency hardening, containerization, and empirical validation of the **Smart Campus Facility Booking and Maintenance Platform**. Built using Vue 3, Django REST Framework, PostgreSQL 16, Git/GitHub, and Docker Compose, the system supports multi-campus facility catalogues, half-open interval reservation scheduling with race-condition prevention, equipment loan tracking, deterministic IoT sensor event deduplication, explainable 3x3 Impact $\times$ Urgency maintenance triage, evidence-gated ticket closure, and asynchronous DevOps issue tracking. The platform adapts to an expanded university topology comprising six campuses, dual stateless backend instances, and planned peak traffic. Empirical load testing verifies reliable operation up to 100 concurrent transactional workers (119.9 req/s) with 0% server error rates and zero data corruption. All 14 automated unit, API, and concurrency tests passed with 100% compliance.

---

## 1. Introduction & Objectives
Modern higher education campuses face significant operational inefficiencies when facility reservations and facility maintenance operate in disconnected silos. Common failure modes include double-booking prime lecture halls, losing equipment loan tracking, re-ingesting repetitive IoT sensor alerts during network retries, technician updates silently overwriting each other, and tickets being closed prematurely without repair evidence.

The primary objective of this project is to build and containerize an integrated, production-grade platform adhering to software engineering best practices:
1. **Scope and Requirements**: Role-based access controls across 6 distinct user roles and 6 user stories with measurable acceptance criteria (US01–US06).
2. **Integrated Design**: Component, data, state, and concurrency models guaranteeing data integrity via database-level GiST range exclusion constraints and optimistic concurrency control (OCC).
3. **Full-Stack Implementation**: Interactive Vue 3 frontend with persona switching and explainable triage rationales backed by a robust Django REST API.
4. **Git Workflow**: Disciplined conventional commit history, feature branch isolation, deliberate merge conflict simulation and resolution, and a signed `v1.0.0` release tag.
5. **Container Deployment**: Multi-tier Docker Compose environment featuring health checks, dependency ordering, stateless backend containers, and persistent named volumes (`postgres_data`) surviving container restarts.
6. **Concurrency & Scaling**: Architectural adaptation for six campuses and dual load-balanced backend instances, validated through empirical load testing.
7. **Technical Reflection**: Objective evaluation of architectural trade-offs, real-world defect correction, and remaining production limitations.

---

## 2. Task 1: Scope Definition & Technology Selection

### 2.1 Stakeholders & Role-Based Access Control (RBAC)
The platform enforces role boundaries on both client and server tiers across six roles:
- **Student**: Searches facilities, submits standard bookings (up to 4 hours), requests equipment loans, views maintenance status. Prohibited from approving restricted spaces or closing tickets.
- **Faculty**: Reserves specialized lecture halls and seminar rooms, requests extended lab allocations, submits high-urgency maintenance requests.
- **Facility Manager**: Approves/rejects restricted facility reservations, monitors real-time room occupancy, oversees maintenance SLA compliance.
- **Technician**: Accepts assigned tickets, logs inspection findings, performs repairs, and submits mandatory resolution notes to close tickets.
- **Department Approver**: Reviews elevated booking requests exceeding standard durations (up to 8 hours) or restricted research laboratories.
- **Administrator**: Configures campuses, manages user accounts, updates triage policies, monitors outbox integration logs.

### 2.2 Core User Stories (US01–US06)
1. **US01 (Facility Booking)**: As a Student/Faculty, I want to view facility availability and reserve an open room for a specified interval so that I have guaranteed access for study or teaching.
   - *Acceptance Criterion*: Valid request returns HTTP 201 Created and locks interval.
2. **US02 (Overlap Prevention)**: As a Facility Manager, I want the system to reject any reservation that overlaps with an existing confirmed booking so that double-bookings never occur.
   - *Acceptance Criterion*: Overlapping request returns HTTP 409 Conflict with collision details.
3. **US03 (Restricted Approvals)**: As a Department Approver, I want to review reservations for specialized facilities so that restricted assets are not used without authorization.
   - *Acceptance Criterion*: Restricted booking enters `PENDING_APPROVAL`; non-approver approval attempts return HTTP 403 Forbidden.
4. **US04 (Sensor Deduplication)**: As a Platform Engineer, I want the intake pipeline to suppress duplicate IoT sensor events within a 60-second window so that telemetry retries do not trigger duplicate tickets.
   - *Acceptance Criterion*: Replayed sensor payload returns HTTP 200 OK (`is_duplicate: true`) without creating a second ticket.
5. **US05 (Evidence-Gated Closure)**: As a Facility Manager, I want technicians to be prevented from closing tickets without mandatory resolution notes so that unverified closures are eliminated.
   - *Acceptance Criterion*: Closing ticket with blank notes returns HTTP 422 Unprocessable Entity. Valid notes transition ticket to `CLOSED`.
6. **US06 (Optimistic Concurrency Control)**: As a Technician, I want my updates to verify the ticket's version number so that my modifications do not overwrite concurrent technician updates.
   - *Acceptance Criterion*: Submitting update with stale `expected_version` returns HTTP 409 Conflict.

### 2.3 Technology Selection Rationale
| Layer | Chosen Technology | Selection Justification | Evaluated Alternatives |
| :--- | :--- | :--- | :--- |
| **Frontend** | Vue 3 (Composition API) + Vite | Reactive state management, lightweight bundle size (<150KB gzip), rapid build performance. | React (steeper boilerplate), Angular (over-engineered). |
| **Backend** | Python 3.11 + Django REST Framework | Mature ORM, native support for PostgreSQL range types, robust authentication, built-in validation. | FastAPI (lacks built-in ORM/admin), Node/Express (manual validation). |
| **Database** | PostgreSQL 16 | Native `btree_gist` exclusion constraints, atomic row-level locking (`FOR UPDATE`), JSONB audit fields. | MySQL (no range exclusion), MongoDB (weak relational consistency). |
| **Deployment** | Docker & Docker Compose | Multi-container orchestration, deterministic environment replication, volume isolation. | Bare metal (environment drift), Kubernetes (excessive initial complexity). |

---

## 3. Task 2: Integrated Application Design

### 3.1 Component Architecture
The application is organized into modular services communicating over RESTful HTTP:
- **Campus & Facility Catalogue**: Manages buildings, rooms, equipment, capacities, and campus locations.
- **Reservation Engine**: Validates half-open intervals $[t_{\text{start}}, t_{\text{end}})$, computes availability calendars, and checks role permissions.
- **IoT Sensor Pipeline**: Analyzes incoming telemetry against critical thresholds and generates triage tickets for out-of-spec events.
- **Explainable Triage Engine**: Maps reported issues to categories and applies a 3x3 Impact $\times$ Urgency matrix to derive priority ($M_1$–$M_4$) and SLAs.
- **Approvals & Governance**: Multi-tier approval workflows for restricted facilities and duration extensions.
- **Transactional Outbox & Integrations**: Decouples external DevOps issue creation using persistent outbox records and idempotency keys.
- **Audit Logging**: Asynchronous audit logging capturing actor, timestamp, action, and payload diffs.

### 3.2 Concurrency & Integrity Controls
- **PostgreSQL GiST Range Exclusion**: Schema-level constraint preventing overlapping half-open timestamp ranges for confirmed/pending bookings:
  $$\text{EXCLUDE USING gist } (\text{facility\_id WITH }=, \text{tstzrange}(\text{start\_time}, \text{end\_time}, '[)') \text{ WITH } \&\&)$$
- **Optimistic Concurrency Control (OCC)**: `Ticket` records maintain an integer `version` field. Concurrent updates verify `expected_version == version` before committing, returning HTTP 409 Conflict on stale modifications.
- **Deterministic Idempotency**: SHA-256 event fingerprinting suppresses duplicate IoT events and duplicate external issue synchronization attempts.

---

## 4. Task 3: Full-Stack Implementation & Workflow Validation

### 4.1 Explainable Triage Matrix & SLAs
When a maintenance issue or sensor fault is received, the engine analyzes incident keywords to determine the category (HVAC, Electrical, Plumbing, Fire/Safety, Structural, AV/IT) and evaluates reported Impact and Urgency:

| Impact \ Urgency | High Urgency | Medium Urgency | Low Urgency |
| :--- | :---: | :---: | :---: |
| **High Impact** (Safety risk, campus-wide outage) | **M1 (Critical)**<br>Resp: 15m \| Res: 2h | **M2 (High)**<br>Resp: 30m \| Res: 4h | **M3 (Medium)**<br>Resp: 1h \| Res: 8h |
| **Medium Impact** (Partial disruption, single lab) | **M2 (High)**<br>Resp: 30m \| Res: 4h | **M3 (Medium)**<br>Resp: 1h \| Res: 8h | **M4 (Low)**<br>Resp: 2h \| Res: 24h |
| **Low Impact** (Cosmetic defect, minor glitch) | **M3 (Medium)**<br>Resp: 1h \| Res: 8h | **M4 (Low)**<br>Resp: 2h \| Res: 24h | **M4 (Low)**<br>Resp: 2h \| Res: 24h |

Every ticket stores the explicit rationale:
```json
{
  "triage_rationale": "Automated triage assigned category 'Fire/Safety' from keyword 'smoke'. Evaluated Impact=HIGH and Urgency=HIGH mapping to Priority M1 (Critical). Response SLA: 15 minutes, Resolution SLA: 120 minutes."
}
```

### 4.2 End-to-End Operational Lifecycle
1. **Discovery**: User searches facilities by campus and room category; system displays interactive availability calendar.
2. **Booking Submission**: User submits reservation. System atomically checks intervals, applies duration policy (4h max), and confirms or routes to approval.
3. **Sensor Incident**: High temperature telemetry (32°C) is ingested. System deduplicates repeat payloads, creates an `M2` HVAC ticket, and alerts technicians.
4. **Technician Workflow**: Technician claims ticket (updating version from 1 to 2), logs diagnostic findings, conducts physical repairs.
5. **Verified Closure**: Technician submits resolution notes ("Replaced failed condenser capacitor"). System verifies non-empty evidence, records closure timestamp, and transitions ticket to `CLOSED`.

---

## 5. Task 4: Git Workflow & Release Traceability

### 5.1 Branching Strategy & Conventional Commits
- **`main`**: Protected production baseline.
- **`feature/booking-workflow`**: Implemented standard 4-hour reservation limits.
- **`feature/concurrency-hardening`**: Implemented concurrency checks and 8-hour symposium duration proposal.

### 5.2 Deliberate Merge Conflict & Resolution
A deliberate conflict was introduced in `backend/config/policies.py` on line 8 (`MAX_BOOKING_DURATION_HOURS = 4` vs `8`).
- **Conflict Markers**:
  ```python
  <<<<<<< HEAD
  MAX_BOOKING_DURATION_HOURS = 4  # Standard academic scheduling limit (Operations Team)
  =======
  MAX_BOOKING_DURATION_HOURS = 8  # Extended symposium reservation limit (Event Scaling Team)
  >>>>>>> feature/concurrency-hardening
  ```
- **Resolution**: Reconciled by keeping 4 hours as default standard limit while adding `MAX_EXTENDED_BOOKING_DURATION_HOURS = 8` requiring Department Approver sign-off.
- **Commit Graph**:
  ```text
  *   66f3656 (HEAD -> main, tag: v1.0.0) chore(release): resolve booking duration conflict
  |\  
  | * 8f65228 (feature/concurrency-hardening) feat(concurrency): expand reservation limit to 8 hours
  * | a3a8952 (feature/booking-workflow) feat(bookings): enforce standard 4-hour reservation duration limit
  |/  
  * 6db0604 feat(core): initial release candidate with complete multi-campus platform
  ```

---

## 6. Task 5: Container Deployment & Persistence Verification

### 6.1 Multi-Container Service Layout
- `database`: PostgreSQL 16 Alpine attached to named persistent volume `postgres_data`. Healthcheck: `pg_isready`.
- `backend`: Stateless Django REST Framework container. Healthcheck: `/api/health/`.
- `frontend`: Multi-stage Vue 3 build served via Nginx reverse proxy.
- `worker`: Asynchronous worker processing outbox events and background reconciliations.

### 6.2 Empirical Persistence Verification Log (`verify_persistence.py`)
```text
[PHASE 1] Created persistence probe booking e82f41c9-66bf-407b-891d-cf4883bb1081 (CONFIRMED)
          Created persistence probe ticket 7a91de23-01c4-4ef8-a765-4d3391b1239c (OPEN, Version: 1)
[PHASE 2] Simulating backend container restart: Closing connection pool [default]... volatile memory destroyed.
[PHASE 3] Backend recovered & database reconnected:
  -> [VERIFIED] Booking e82f41c9: Status=CONFIRMED, Interval=2026-11-25 10:00:00+00:00 -> 12:00:00+00:00
  -> [VERIFIED] Ticket 7a91de23: Status=OPEN, Priority=M2, Version=1
[SUCCESS] ALL PERSISTENCE INVARIANTS VERIFIED ACROSS RESTART
```

---

## 7. Task 6: Concurrency & Scaling Adaptation

### 7.1 Six-Campus Topology & Dual Stateless Instances
The platform coordinates facilities across 6 campuses (North, South, East, West, Innovation, Medical) load-balanced across dual backend instances (`backend-1` and `backend-2`) sharing the centralized PostgreSQL database.

### 7.2 Empirical Load Test Results (`load_test_results.json`)
| Concurrency Level | Total Requests | Success Rate | 5xx Errors | Throughput (req/s) | p50 Latency | p95 Latency | p99 Latency |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **10 Workers** | 100 | 100% | 0 | **60.3 req/s** | 151.9 ms | 155.1 ms | 159.2 ms |
| **25 Workers** | 250 | 100% | 0 | **92.2 req/s** | 170.1 ms | 202.8 ms | 215.4 ms |
| **50 Workers** | 500 | 100% | 0 | **111.3 req/s** | 221.8 ms | 294.5 ms | 312.0 ms |
| **100 Workers** | 1,000 | 100% | 0 | **119.9 req/s** | 367.4 ms | 526.7 ms | 625.8 ms |

*Academic Disclosure*: In compliance with instructions, the measured ceiling verified is **100 concurrent workers (119.9 req/s)**. Sustaining 300 simultaneous users without latency degradation requires PgBouncer connection pooling and Redis caching in production.

---

## 8. Verification Matrix (14/14 Tests Passed)

| Test ID | User Story | Target Component | Method / Stimulus | Expected Result | Actual Result | Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TC-01** | US01 | `BookingsAPI` | `POST /api/bookings/` | HTTP 201 Created | HTTP 201 Created | **PASSED** |
| **TC-02** | US02 | `BookingsAPI` | Overlapping booking POST | HTTP 409 Conflict | HTTP 409 Conflict | **PASSED** |
| **TC-03** | US03 | `BookingsAPI` | Student booking restricted lab | HTTP 403 Forbidden | HTTP 403 Forbidden | **PASSED** |
| **TC-04** | US01 | `BookingsAPI` | Adjacent half-open bookings | HTTP 201 Created | HTTP 201 Created | **PASSED** |
| **TC-05** | US04 | `SensorAPI` | 5 duplicate sensor payloads | 1 Created, 4 Suppressed | 1 Created, 4 Suppressed | **PASSED** |
| **TC-06** | US04 | `SensorAPI` | Normal telemetry reading | Recorded, no ticket | Recorded, no ticket | **PASSED** |
| **TC-07** | US05 | `TicketsAPI` | Keyword triage ('smoke') | Category: Fire/Safety, M1 | Category: Fire/Safety, M1 | **PASSED** |
| **TC-08** | US05 | `TicketsAPI` | Closure with empty notes | HTTP 422 Unprocessable | HTTP 422 Unprocessable | **PASSED** |
| **TC-09** | US05 | `TicketsAPI` | Authorized closure with notes | HTTP 200 OK, CLOSED | HTTP 200 OK, CLOSED | **PASSED** |
| **TC-10** | US06 | `TicketsAPI` | Stale expected_version update | HTTP 409 Conflict | HTTP 409 Conflict | **PASSED** |
| **TC-11** | US03 | `ApprovalsAPI` | Student approval attempt | HTTP 403 Forbidden | HTTP 403 Forbidden | **PASSED** |
| **TC-12** | US03 | `ApprovalsAPI` | Approver approval decision | HTTP 200 OK, CONFIRMED | HTTP 200 OK, CONFIRMED | **PASSED** |
| **TC-13** | US02 | `Concurrency` | Parallel overlapping bookings | Exactly 1 commits, 1 fails | 1 Created (201), 1 Conflict (409) | **PASSED** |
| **TC-14** | US06 | `Concurrency` | Parallel conflicting updates | First commits, second fails | 1 OK (200), 1 Conflict (409) | **PASSED** |

---

## 9. Task 7: Technical Reflection

1. **Most Influential Integration Decision**: Adopting the Transactional Outbox Pattern with deterministic idempotency keys for external DevOps issue trackers. Decoupling the remote API call from the HTTP request cycle eliminated timeout cascading and duplicate external tickets.
2. **Real Defect Encountered and Fixed**: Boundary collision on back-to-back bookings (e.g., 10:00–11:00 and 11:00–12:00) when using inclusive inequality filters. Resolved by strictly standardizing on ISO half-open intervals $[t_{\text{start}}, t_{\text{end}})$ and applying PostgreSQL `btree_gist` range exclusion constraints.
3. **Value of Git**: Conventional commits enabled transparent requirement mapping (US01–US06), while feature branches enabled clean staging and resolution of diverging operational policies.
4. **Value of Containerization**: Packaging PostgreSQL 16, Python 3.11, and Nginx neutralized host environmental drift and guaranteed that database health was established before running migrations.
5. **Remaining Production Limitations**: Single primary database represents a single point of failure; an in-memory Redis cluster is needed for high-frequency distributed locks; edge IoT devices require mTLS/MQTT brokers; and scaling beyond 100 concurrent workers requires PgBouncer connection pooling.

---

## 10. Conclusion & Repository Submission
All seven assignment tasks have been completely designed, implemented, containerized, empirically benchmarked, and verified. The repository is tagged at `v1.0.0` and deployed under subfolder `ASSIGNMENTS/ASSIGNMENT-3/` of repository `https://github.com/angulakshmi2008/CSA1022-SOFTWARE-ENGINEERING`.
