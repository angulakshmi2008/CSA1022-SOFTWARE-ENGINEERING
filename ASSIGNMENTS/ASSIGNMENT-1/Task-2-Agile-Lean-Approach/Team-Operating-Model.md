# Task 2: Team Operating Model and Lean Flow Controls

## 1. Cross-Functional Team Architecture and Roles

The delivery organization consists of a seven-member cross-functional engineering team designed to eliminate inter-departmental silos.

| Role Title | Primary Responsibilities | Core Deliverables & Artifacts | Primary Skill Domain |
|---|---|---|---|
| **Product Owner / Business Analysis Lead** | Owns product vision, maintains prioritized backlog, negotiates scope trade-offs, coordinates stakeholder validation sessions. | Product Backlog, Sprint Goals, Release Roadmap, User Stories with Acceptance Criteria. | Requirements engineering, Agile governance, domain analysis. |
| **Frontend Engineer** | Develops responsive web storefront, mobile checkout views, customer tracking dashboard, and support lookup screens. | Accessible UI components, client-side input validation, screen-reader markup. | Modern TypeScript/JavaScript, CSS, WCAG accessibility standards. |
| **Order API Engineer** | Implements core order lifecycle state machine, order creation/cancellation APIs, state transition validations, and persistence. | Order microservice endpoints, REST API schemas, transactional state transition logic. | Backend Python/Node.js, RESTful contracts, relational database design. |
| **Inventory & Database Engineer** | Architects inventory schema, implements atomic reservation locks with TTL timers, low-stock triggers, and warehouse pick list queries. | Reservation service, concurrency locking logic, database migrations, store sync scripts. | Relational databases (SQLite/PostgreSQL), transactional isolation, concurrency control. |
| **Payments & Security Engineer** | Engineers payment gateway adapter, idempotency key verification, role-based authorization guards, and cryptographic security. | Idempotency engine, payment stub, RBAC middleware, audit journal logging. | Application security, cryptography, payment gateway protocols, OWASP guidelines. |
| **Quality Assurance (QA) Engineer** | Authors automated test suites (unit, integration, regression, concurrency stress tests), validates acceptance criteria, enforces DoD. | Automated test scripts, test execution reports, defect logs, test data fixtures. | PyTest/Unittest, concurrency test harnesses, test automation frameworks. |
| **DevOps & Infrastructure Engineer** | Configures build automation, continuous integration pipelines, containerized environments, and health-check monitoring. | CI/CD pipeline scripts, environment configuration runbooks, reproducible build scripts. | CI/CD tooling, Docker, shell automation, system reliability engineering. |

---

## 2. RACI Governance Matrix

| Lifecycle Activity | Product Owner | Frontend | Order API | Inventory | Payments | QA | DevOps |
|---|---|---|---|---|---|---|---|
| Backlog Prioritization & Sprint Scope | **A / R** | C | C | C | C | C | I |
| User Story Definition of Ready | **A** | C | C | C | C | **R** | C |
| Core Order State Machine Development | I | C | **A / R** | C | C | C | I |
| Stock Concurrency & Reservation Locks | I | I | C | **A / R** | I | C | I |
| Payment Idempotency & Gateway Adapter | I | C | C | I | **A / R** | C | I |
| Automated Test Suite & Concurrency Tests | I | C | C | C | C | **A / R** | C |
| CI/CD Pipeline & Build Automation | I | I | I | I | I | C | **A / R** |
| Release Sign-Off (Definition of Done) | **A** | C | C | C | C | **R** | C |

*Legend: **A** = Accountable; **R** = Responsible; **C** = Consulted; **I** = Informed.*

---

## 3. Operating Cadence and Stakeholder Participation

To maximize velocity while honoring the 90-minute weekly stakeholder constraint, the team operates on the following recurring schedule:

```
Week 1 (Sprint Start & Development)
├── Mon 09:00 - 11:00 : Sprint Planning (Team only, PO presents refined backlog)
├── Mon - Fri 09:15  : Daily Standup (15-min timebox: Progress, Blockers, Flow)
└── Thu 15:00 - 15:45 : Stakeholder Refinement (Part 1: 45 min with Warehouse & Finance)

Week 2 (Completion & Review)
├── Mon - Fri 09:15  : Daily Standup (15-min timebox: Focus on WIP limits & testing)
├── Thu 15:00 - 15:45 : Stakeholder Refinement (Part 2: 45 min confirmation of next sprint AC)
├── Fri 14:00 - 15:00 : Sprint Review & Live Working Demo (Stakeholders attend 45 min)
└── Fri 15:30 - 16:30 : Sprint Retrospective (Team only: Inspect, adapt, refine metrics)
```

### 3.1 Strict Stakeholder Budgeting (90 Minutes / Week)
- **Session 1 (Refinement - 45 min):** Dedicated to clarifying acceptance criteria, negative test cases, business thresholds (e.g., return windows, refund approval limits), and warehouse pick list rules.
- **Session 2 (Sprint Review/Demo - 45 min):** Dedicated to demonstrating working, demonstrable software increments to warehouse supervisors and finance managers. Feedback is captured directly into the product backlog as new or revised stories.

---

## 4. Blocker Escalation Protocol (The One-Working-Day Rule)

To prevent idle waiting and silent bottlenecks:
1. **Trigger:** When an active work item is halted due to an external dependency, ambiguity in requirements, technical defect, or third-party unavailability, the developer immediately transitions the card to `Blocked` on the board.
2. **Identification:** The blocker card must be annotated with: (a) Blocker description, (b) Blocked dependency ID, (c) Date/time blocked, and (d) Designated owner.
3. **Internal Swarming (Day 0):** The team swarms within the daily standup to resolve the blocker internally (e.g., pairing or introducing a mock/stub).
4. **Formal Escalation (Day 1 / 24 Hours):** If the item remains blocked after 24 hours (1 working day), ownership automatically escalates to the **Product Owner**.
5. **Resolution Action:** The Product Owner has the sole authority to:
   - Schedule an emergency clarification with the relevant stakeholder;
   - Swap the blocked story with an equivalent-sized, ready backlog item; or
   - Authorize an architectural test double / stub to decouple progress.

---

## 5. Explicit Lean Flow Practices

The team applies foundational Lean principles (derived from Toyota Production System and Poppendieck's Lean Software Development) to eliminate the seven classic wastes of software engineering:

```
[Muda / Waste] ──────────► [Applied Lean Control in This Operating Model]
1. Partially Done Work ──► Strict WIP limits (Dev: 4, Review: 2, Test: 2); no story is Done without passing tests.
2. Extra Features      ──► Strict MoSCoW prioritization; ML forecasting, loyalty, and analytics are deferred.
3. Relearning          ──► Architecture Decision Records (ADRs) and executable automated test specifications.
4. Handoffs            ──► Cross-functional team with daily API and QA pairing sessions; no separate siloed teams.
5. Delays / Waiting    ──► Payment gateway mock stub and simulated scanner string input built in Sprint 1.
6. Task Switching      ──► Individual developers own at most 1 active item; expedite items require trading work.
7. Defects             ──► Test-First development; negative acceptance criteria defined before coding begins.
```

### 5.1 Work-in-Progress (WIP) Controls
- **In Progress (Development):** Limit = **4 items**. Prevents five developers from starting five separate backend threads that overwhelm the single QA engineer.
- **Review (Peer Review):** Limit = **2 items**. Forces developers to review colleagues' pull requests before starting new implementation tasks.
- **Test (QA & Acceptance):** Limit = **2 items**. Protects the single QA engineer from an unmanageable queue and makes testing delays visible immediately.
- **Expedite Swimlane Rule:** At most **1** critical production or security defect can enter the expedite swimlane. To preserve sustainable pace and the Sprint Goal, entering an expedite item requires the Product Owner to remove an equivalent number of planned story points from the active sprint.
