# Full-Stack Implementation Architecture

## 1. System Overview
The Smart Campus Facility Booking and Maintenance Platform delivers a cohesive, responsive web application connecting a Vue 3 frontend, Django REST Framework (DRF) backend, and PostgreSQL relational database.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   VUE 3 SINGLE PAGE APPLICATION                        │
│  - App.vue: Master layout, Persona Switcher, Tab Router                │
│  - Operations Dashboard: KPI metrics, SLA countdowns, Activity Feed    │
│  - Facilities Catalogue: Multi-campus spaces, Availability Calendar    │
│  - Maintenance Queue: Explainable triage popover, Priority badges      │
│  - Inspection & Closure Modal: FSM transitions, Evidence inputs        │
│  - Sensor Telemetry Simulator: Telemetry injection, Duplicate test     │
│  - Governance Centre: Restricted booking and loan approvals            │
│  - DevOps Hub: Outbox intent tracking, Retry reconciliation            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / REST / JSON
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   DJANGO REST FRAMEWORK BACKEND                        │
│  - accounts: Custom User model, 6 RBAC roles, Token authentication     │
│  - campuses: Multi-campus domain records (6 campuses)                  │
│  - facilities: Space inventory, capacity, restriction flags            │
│  - bookings: Reservation FSM, overlap validation, idempotency          │
│  - maintenance: Ticket FSM, explainable triage engine, comments        │
│  - sensor_events: Ingestion, threshold alerts, duplicate suppression   │
│  - approvals: Delegated governance for restricted actions              │
│  - integrations: Durable intent outbox with correlation keys           │
│  - audit: Transactional append-only event logging                      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ SQL (ACID Transactions)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   POSTGRESQL RELATIONAL PERSISTENCE                    │
│  - 14 Normalized Domain Tables                                         │
│  - GiST Range Exclusion Constraint: booking_no_active_overlap           │
│  - Unique Index: UNIQUE(source_id, event_id)                           │
│  - Optimistic Concurrency Control: version column                      │
│  - Named Persistent Storage Volume                                     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Server-Enforced Persona Profiles

| Username | Role | Campus | Delegated Authority Scope |
|---|---|---|---|
| `admin` | System Administrator | MAIN | System-wide configuration, facility management, SLA policies. |
| `approver.dr.kumar` | Department Approver | MAIN | Authorizes restricted research facilities (BSL-3, Cleanroom, Robotics). |
| `manager.priya` | Facility Manager | MAIN | Triage verification, technician assignment, SLA oversight. |
| `tech.rajesh` | Maintenance Technician | MAIN | Diagnostics, inspection notes, repair execution, resolution evidence. |
| `tech.vikram` | Maintenance Technician | ENG | Engineering campus mechanical & plumbing workorders. |
| `faculty.dr.anand` | Faculty Member | MAIN | Reserves teaching halls & laboratories; requests restricted spaces. |
| `student.arun` | Student | MAIN | Public study spaces and computer labs; equipment loans. |
| `student.meera` | Student | MED | Biomedical public library and standard study rooms. |

---

## 3. Key Design Invariants
1. **Server-Enforced RBAC:** The frontend provides intuitive role-based guidance, but every backend endpoint strictly validates permissions against the authenticated user's database role.
2. **Defensive Concurrency:** All entity updates check `expected_version` to prevent race conditions and silent overwriting.
3. **Atomic Audit Trails:** State transitions and audit logging execute within `transaction.atomic()`, ensuring zero unrecorded state mutations.
