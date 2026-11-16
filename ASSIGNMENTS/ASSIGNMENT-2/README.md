# FulfillIQ – Omnichannel Order Fulfilment Platform
## CSA10 Software Engineering – Assignment 2: Requirements, Architecture, and Empirical Validation

[![System Tests](https://img.shields.io/badge/Validation%20Tests-11%2F11%20PASSED-success)](tests/)
[![Architecture](https://img.shields.io/badge/Architecture-Modular%20Monolith-blue)](docs/task-4-architecture/)
[![Outbox Pattern](https://img.shields.io/badge/Pattern-Transactional%20Outbox-orange)](backend/app/workers/)
[![Course Outcome](https://img.shields.io/badge/SIMATS%20CO-CO2%20(BTL--5%2F6)-purple)](docs/report/)

---

## Executive Overview
**FulfillIQ** is an enterprise-grade Omnichannel Order Fulfilment Platform designed, modeled, implemented, and empirically validated for **CSA10 Software Engineering (Assignment 2)**. 

The platform bridges digital e-commerce storefronts, physical retail fulfillment centers, and third-party logistics carriers. It enforces strict transactional integrity across order lifecycle states, eliminates ghost inventory overselling through atomic row-level reservations with a 15-minute lease expiry, prevents duplicate payments via cryptographic HMAC-SHA256 webhook deduplication, isolates warehouse picking by regional facility, and guarantees dual-control financial governance for customer refunds.

---

## Repository Structure & Task Mapping

All deliverables are organized into dedicated task folders with complete documentation, PlantUML source models, architectural decision records, and empirical test evidence:

| Task / Question | Assignment Requirement | Repository Location | Key Deliverables & Artifacts |
| :--- | :--- | :--- | :--- |
| **Q1** | Stakeholder Needs & Conflict Resolution | [`docs/task-1-stakeholders/`](docs/task-1-stakeholders/) | Investigation questions, simulated findings across 6 personas, 4 resolved conflicts, system boundary. |
| **Q2** | Requirements Specification & Tooling | [`docs/task-2-requirements/`](docs/task-2-requirements/) | FR01–FR14, NFR01–NFR08, business rules, MoSCoW prioritization, Jira vs. GitHub evaluation. |
| **Q3** | UML Modeling & Traceability | [`docs/task-3-uml-traceability/`](docs/task-3-uml-traceability/) | PlantUML source files (`.puml`), End-to-End Traceability Matrix, 4 discovered modeling corrections. |
| **Q4** | Architecture Design & Justification | [`docs/task-4-architecture/`](docs/task-4-architecture/) | Monolith vs. Microservices 10-dimension comparison, component & deployment diagrams, ADR-001/002/003. |
| **Q5** | Critical Behavior Validation & Revision | [`docs/task-5-validation/`](docs/task-5-validation/) | Invariants, operation contracts, test execution evidence (T1–T7), 2 documented design revisions. |
| **Q6** | Day-4 Expansion & Edge Scanner Redesign| [`docs/task-6-expansion/`](docs/task-6-expansion/) | 12-region impact analysis, edge scanner sync/dedup (T8), policy versioning (T9), CAP theorem defense. |
| **Q7** | Technical Reflection & Assessment Defense | [`docs/task-7-reflection/`](docs/task-7-reflection/) | Academic reflection on architectural drivers, stakeholder friction, modeling bugs, and defense prompts. |
| **Master Report**| Academic Assignment Report | [`docs/report/`](docs/report/) | [`assignment-report.docx`](docs/report/assignment-report.docx) (Times New Roman 12pt, 1.5 spacing) & [`assignment-report.md`](docs/report/assignment-report.md). |

---

## Technology Baseline

| Subsystem | Technology Selection | Architectural Rationale |
| :--- | :--- | :--- |
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS | Modular role-based dashboard views with type safety and responsive navigation. |
| **Backend API** | Python 3.11+, FastAPI, Pydantic | High-performance asynchronous REST API with dependency-injected JWT RBAC validation. |
| **Database** | PostgreSQL 16 (Production) / SQLite WAL (Dev/Test) | Strict ACID transactional consistency, row-level concurrency locks, and composite unique constraints. |
| **Asynchronous Engine**| Transactional Outbox Worker | Decouples external partner latency (courier/gateway) from synchronous customer request threads. |
| **Containerization** | Docker, Docker Compose, Nginx | Single-command portable deployment with reverse proxy load balancing and static asset serving. |
| **UML Modeling** | PlantUML (`.puml`) Plaintext Specs | Version-controlled, diffable visual models eliminating documentation drift. |

---

## Role-Based Access Control (RBAC) & Synthetic Accounts

The platform includes seven pre-seeded synthetic user accounts covering all six operational roles. **No real customer PII or payment card data is utilized.**

| Role | Username | Password | Operational Capabilities & Scope |
| :--- | :--- | :--- | :--- |
| **Customer** | `customer1` | `password123` | Browse catalog, submit checkout, view own order tracking, initiate refund requests. |
| **Warehouse Picker** | `picker_north` | `password123` | Inspect regional pick queues (Region 1 - North), transition orders: `PAID` $\to$ `PACKED`. |
| **Warehouse Picker** | `picker_south` | `password123` | Inspect regional pick queues (Region 2 - South), transition orders: `PAID` $\to$ `PACKED`. |
| **Support Agent** | `support1` | `password123` | Look up customer orders, inspect carrier tracking milestones, submit refund requests. |
| **Finance Reviewer**| `finance1` | `password123` | Review and sign off on high-value refunds (> \$50.00), inspect audit logs, approve retry. |
| **Store Manager** | `manager1` | `password123` | Monitor regional turnover, inspect aggregate fulfillment KPIs, review stock levels. |
| **Administrator** | `admin1` | `password123` | Configure versioned regional policies (tax/shipping/refund limits), view system audit trails. |

---

## Quickstart & Execution Guide

### Option 1: Run the Automated Validation Suite (In-Process Test Runner)
To execute the complete 11-scenario automated verification suite verifying all invariants:

```bash
# From repository root
python scripts/run_all_tests.py
```

**Empirical Test Results (0.79s Total Runtime):**
```text
================================================================================
                    FULFILLIQ AUTOMATED VALIDATION SUITE                        
================================================================================
  [T1] Stock Contention (Concurrency & Overselling)   ... [PASSED] (63.8 ms)
  [T2] Idempotent Payment Callback Deduplication      ... [PASSED] (91.2 ms)
  [T3] Refund Failure Approval Retention & Retry      ... [PASSED] (91.2 ms)
  [T4] Sequential Order Lifecycle & Dispatch Guards   ... [PASSED] (95.8 ms)
  [T5] Transactional Outbox Courier Retry & Sync      ... [PASSED] (50.8 ms)
  [T6] Security Boundaries & Server-Side RBAC         ... [PASSED] (110.5 ms)
  [T7] Late Payment Callback Lease Expiry & Resale    ... [PASSED] (82.2 ms)
  [T8] Edge Scanner Synchronization & Deduplication   ... [PASSED] (32.7 ms)
  [T9] Versioned Regional Policy Immutability         ... [PASSED] (74.5 ms)
  [T10] Multi-Regional Cluster Health & Resilience    ... [PASSED] (<1.0 ms)
  [T11] Offline Queued Refund Approval Governance     ... [PASSED] (94.8 ms)
--------------------------------------------------------------------------------
OVERALL STATUS: ALL 11 TESTS PASSED [Execution Time: 0.79s]
================================================================================
```

### Option 2: Run with Docker Compose (Full-Stack Deployment)
To start the entire multi-container environment (FastAPI API, PostgreSQL database, React frontend, Nginx reverse proxy, and Background Workers):

```bash
docker compose up --build
```
- **Web Application Portal:** `http://localhost`
- **FastAPI OpenAPI Swagger Documentation:** `http://localhost/api/docs`
- **Backend Health Check:** `http://localhost/api/health`

### Option 3: Run Locally for Development

**1. Initialize Database & Seed Synthetic Data:**
```bash
python -m database.seed_data
```

**2. Start Backend API Server:**
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

**3. Start Frontend Development Server:**
```bash
cd frontend
pnpm install
pnpm run dev
```

---

## Day-4 Design Challenge: Multi-Regional Expansion Summary

The platform addresses operational expansion from 3 to 12 international regions, supporting 500 simultaneous users, 1,000 events/minute, and intermittently disconnected warehouse scanners:
1. **Versioned Regional Policies:** Independent, versioned tax rates, shipping tiers, and refund approval thresholds across 12 regions (`US-NORTH`, `US-SOUTH`, `EU-WEST`, `APAC-EAST`, etc.). Orders snapshot the policy version at checkout.
2. **Edge Scanner Deduplication:** Handheld warehouse scanners buffer up to 5,000 scan events in dead zones, assigning composite identities `(node_id, event_id)`. The server enforces idempotent batch synchronization via `UNIQUE(node_id, event_id)` (verified in `T8`).
3. **Dual-Control Offline Governance:** Handheld scanners cannot locally approve financial refunds. Approvals are strictly validated against central RBAC upon reconnection (verified in `T11`).
4. **Cost & CAP Theorem Defense:** Order placement operates as a **Consistent/Partition-Tolerant (CP)** relational domain, while disconnected edge scanners operate as an **Available/Partition-Tolerant (AP)** domain buffering scans locally, maintaining infrastructure costs within \$300–\$600/month.

---

## Academic Documentation & Compliance

- **Final Academic Word Report:** [`docs/report/assignment-report.docx`](docs/report/assignment-report.docx)
  - Typography: Times New Roman, 14 pt Title/Headings, 12 pt Body, 1.5 Line Spacing, Justified Alignment.
  - Complete explanations of all 7 tasks, structured tables, ADRs, formal contracts, and 10 IEEE-style references [1]–[10].
- **Markdown Master Report:** [`docs/report/assignment-report.md`](docs/report/assignment-report.md)

---

## Git Version Control & Branch History

The project strictly followed isolated Git feature branching for every task deliverable:
- `task-1-stakeholders` $\to$ Elicitation, conflict resolutions, scope boundaries.
- `task-2-requirements` $\to$ FRs, NFRs, business rules, tool evaluation.
- `task-3-uml-traceability` $\to$ PlantUML diagrams, traceability matrix, modeling fixes.
- `task-4-architecture` $\to$ Architecture evaluation, component/deployment diagrams, ADRs.
- `task-5-validation` $\to$ Automated test suite (T1–T7), design revisions, empirical evidence.
- `task-6-expansion` $\to$ Multi-region scaling, edge scanner dedup (T8–T11), CAP theorem defense.
- `task-7-reflection` $\to$ Academic reflection, assessment defense prompts.
- `main` $\to$ Integrated production codebase, master reports, and container configs.

---

## License & Academic Integrity Notice
This project was developed for **SIMATS Engineering (CSA10 Software Engineering Assignment 2)**. All data, customer accounts, order transactions, and inventory levels are purely synthetic and intended solely for academic evaluation.
