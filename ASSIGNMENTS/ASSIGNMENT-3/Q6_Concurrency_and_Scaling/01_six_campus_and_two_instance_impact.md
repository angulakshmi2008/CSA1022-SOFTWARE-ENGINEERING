# Question 6: Architecture Adaptation for Six Campuses and Dual Backend Instances

## 1. Domain Scaling: Six-Campus Topology

The initial single-campus specification was expanded to support six geographically distributed university campuses:
1. **North Campus (Main Academic Hub)**: Houses high-capacity lecture halls (LH-101, LH-201) and engineering auditoriums.
2. **South Campus (Undergraduate Sciences)**: Houses standard seminar classrooms (SC-204) and teaching laboratories.
3. **East Campus (Biomedical & Life Sciences)**: Specialized medical laboratories and sterile research facilities.
4. **West Campus (Athletics & Performing Arts)**: Sports arenas, auditoriums, and creative studios.
5. **Innovation Campus (Incubation & Graduate Research)**: Advanced computing clusters, robotics labs, and maker spaces.
6. **Medical Campus (Clinical Skills & Simulation)**: High-fidelity clinical simulation wards and specialized medical equipment.

### 1.1 Data Model Adaptation
- **Campus Entity**: Added `Campus` model with unique `code`, `name`, `timezone`, `latitude`, and `longitude`.
- **Foreign Key Indexing**: Every `Facility` is partitioned by `campus_id` with composite indexes (`campus_id, code`) and (`campus_id, is_active`).
- **Campus-Scoped Filtering**: All calendar availability and maintenance queries are strictly filtered by campus ID to prevent full-table cross-campus scans.

---

## 2. Horizontal Scaling: Dual Stateless Backend Instances

To support planned peak concurrency and high availability, the backend architecture was scaled from a single monolith to **two identical, stateless backend instances** (`backend-1` and `backend-2`) deployed behind an Nginx reverse proxy load balancer (`deployment/compose/docker-compose.scaling.yml`).

```
                                [ Incoming Traffic ]
                                         │
                                         ▼ HTTP :80
                     ┌───────────────────────────────────────┐
                     │          nginx-load-balancer          │
                     │          (Round-Robin / Least-Conn)   │
                     └───────────────┬───────────────────────┘
                                     │
                   ┌─────────────────┴─────────────────┐
                   │                                   │
                   ▼ HTTP :8000                        ▼ HTTP :8000
        ┌─────────────────────┐             ┌─────────────────────┐
        │  backend-1 (Node A) │             │  backend-2 (Node B) │
        │  Stateless DRF      │             │  Stateless DRF      │
        └──────────┬──────────┘             └──────────┬──────────┘
                   │                                   │
                   └─────────────────┬─────────────────┘
                                     │ TCP :5432
                                     ▼
                     ┌───────────────────────────────────────┐
                     │          PostgreSQL 16 Database       │
                     │   - Row Locking (SELECT FOR UPDATE)   │
                     │   - GiST Range Exclusion Constraints  │
                     │   - Optimistic Version Verification   │
                     └───────────────────────────────────────┘
```

### 2.1 Enforcing Statelessness
1. **No In-Memory Session Storage**: Authentication uses stateless tokens, eliminating sticky-session affinity requirements. Any request can hit either backend instance interchangeably.
2. **Centralized Database Locking**: No local file or process memory locks are used for concurrency. All mutual exclusion is mediated exclusively by the shared PostgreSQL database.
3. **Zero Local File Dependencies**: All assets, attachments, and audit logs are recorded in the shared database or object storage, ensuring that if Node A creates a ticket, Node B can immediately inspect, triage, or resolve it without sync delay.

---

## 3. High Availability Resilience: Instance Crash Simulation

Under the dual-instance configuration:
- If `backend-1` crashes, reboots, or is terminated during peak load, the Nginx load balancer automatically detects upstream failure via health-check timeouts and routes 100% of incoming traffic to `backend-2`.
- Active transactions committed on `backend-1` prior to crash are fully persisted in PostgreSQL, preventing orphaned or half-committed reservation records.
