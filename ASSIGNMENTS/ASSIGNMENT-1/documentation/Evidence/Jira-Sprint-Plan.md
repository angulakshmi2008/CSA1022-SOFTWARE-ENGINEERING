# Jira & GitHub Projects Configuration Evidence

## 1. Project Profile and Configuration
- **Project Name:** Omnichannel Order Fulfilment Platform (OFP)
- **Project Key:** `OFP` (or `FIQP`)
- **Project Type:** Scrum Software Development (Team-Managed / Company-Managed)
- **Board Configuration:** Scrum Board with Custom Kanban WIP Columns

---

## 2. Board Status Workflow and Column Mapping

| Board Column | Mapped Workflow Status | Column WIP Constraint | Quality Gate Rule |
|---|---|---|---|
| **To Do / Ready** | `Ready` | None (Unlimited) | Card must satisfy Definition of Ready (DoR). |
| **In Progress** | `In Progress` | **Max 4 Items** | Developers actively coding; unblocked tasks only. |
| **Review** | `Review` | **Max 2 Items** | Pull request open; peer review actively conducted. |
| **Test** | `Test` | **Max 2 Items** (Tightest Control) | Single QA engineer verifying automated tests & acceptance criteria. |
| **Blocked** | `Blocked` | Counted against column WIP | Reason & owner required; triggers 24-hour escalation rule. |
| **Done** | `Done` | Terminal (Unlimited) | 100% adherence to Definition of Done (DoD). |

---

## 3. Sprint Iteration Containers

### Sprint 1: Secure Ordering Foundation (Weeks 1–2)
- **Sprint Goal:** Deliver authenticated login, atomic inventory reservation with 15m TTL, idempotent payment processing stub, warehouse pick list generation, and reproducible local builds.
- **Committed Issues:**
  - `OFP-S01`: Role-based login and scoped session management (3 pts) -> **Done**
  - `OFP-S02`: Atomic stock reservation with TTL expiry (5 pts) -> **Done**
  - `OFP-S03a`: Idempotent payment processing with local stub (2 pts) -> **In Progress (Carryover)**
  - `OFP-S04`: Warehouse digital pick list generation (3 pts) -> **Done**
  - `OFP-S09a`: Local build and smoke test automation (3 pts) -> **In Progress (Carryover)**
- **Sprint Metrics:** 11 / 16 Points Completed (68.8% Velocity).

### Sprint 2: Fulfillment Lifecycle, Milestone Tracking & Stock Alerts (Weeks 3–4)
- **Sprint Goal:** Enable warehouse dispatch state transitions, screen-reader accessible tracking, CI/CD pipeline enforcement, and low-stock safety triggers.
- **Committed Issues:**
  - `OFP-S03a`: Payment Stub (2 pts - Carryover) -> **Done**
  - `OFP-S09a`: Local Build Docs (3 pts - Carryover) -> **Done**
  - `OFP-S05a`: Dispatch Transition State Machine (3 pts) -> **Done**
  - `OFP-S06`: Screen-Reader Accessible Milestone Tracking (3 pts) -> **Done**
  - `OFP-S09b`: CI/CD Pipeline Enforcement (2 pts) -> **Done**
  - `OFP-S11`: Deterministic Low-Stock Alerts (3 pts) -> **Done**

### Sprint 3: Payment Gateway Sandbox, Barcode Scanning & Controlled Refunds (Weeks 5–6)
- **Sprint Goal:** Connect live payment sandbox, verify physical barcode picking, and enable customer returns with finance-controlled refund approvals.
- **Committed Issues:**
  - `OFP-S03b`: External Gateway Sandbox Integration (3 pts)
  - `OFP-S07`: Customer Return Request Initiation (3 pts)
  - `OFP-S08`: Role-Controlled Finance Refund Approval (5 pts)
  - `OFP-S12`: Barcode Scanner Verification (3 pts)

### Sprint 4: Support Console, Regression Hardening & Release Rehearsal (Weeks 7–8)
- **Sprint Goal:** Empower customer support order lookups, absorb carryover defects, execute full cross-browser regression, and complete release staging rehearsal.
- **Committed Issues:**
  - `OFP-S10`: Support Order Timeline Lookup Console (3 pts)
  - Buffer / Release Hardening / Rehearsal (Reserve Capacity)

---

## 4. Scaled Agile Coordination Board (Sprints 2–4 with Team A & Team B)
- **Team A (Core Engine):** Focuses on multi-warehouse reservation row-locks, order state transitions, and tracking.
- **Team B (Regional & UX):** Focuses on regional tax/shipping policy tables, customer support UI, and payment sandbox integration.
- **Cross-Team Integration Lane:** Shared board column with strict WIP limit = 2 items to prevent merge deadlocks.
