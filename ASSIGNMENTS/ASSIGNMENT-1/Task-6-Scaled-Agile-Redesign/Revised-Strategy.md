# Task 6: Scaled Agile Redesign Strategy and Capacity Recalculation

## 1. Redesign Objectives (Component B)

To navigate the organizational shock while safeguarding the fixed 8-week festival-sale launch date, the Product Owner and lead architects established six measurable redesign objectives:

1. **Objective 1 (Contract Integrity):** Maintain a **single immutable OpenAPI and database schema contract** for orders and payments; neither team is permitted to alter shared data contracts unilaterally.
2. **Objective 2 (Modular Policy Decoupling):** Implement region-specific tax, shipping, and refund rules via **isolated, table-driven configuration policies**, preventing code duplication across regional warehouse deployments.
3. **Objective 3 (Regional Multi-Tenancy Validation):** Demonstrate a fully verified, end-to-end order-to-refund journey across the primary region and at least one secondary regional warehouse in Sprint 2, with the third region verified in Sprint 3.
4. **Objective 4 (Zero Security & Authorization Defects):** Enforce strict server-side RBAC guaranteeing that **zero authorization defects** exist in the refund path (e.g., support agents approving refunds) at release sign-off.
5. **Objective 5 (WIP Constraint on Dependencies):** Limit active cross-team dependencies to a **maximum of two items in flight simultaneously**, preventing integration deadlocks.
6. **Objective 6 (Uncompromising Deadline Preservation):** Protect the Week 8 festival-sale release deadline by strictly deferring non-essential scope (analytics, promotional features, demand forecasting) rather than extending the schedule.

---

## 2. Capacity Recalculation: Brooks' Law in Practice (Component C)

### 2.1 The Realistic Capacity Model
Rather than assuming that two teams double throughput, the capacity model mathematically accounts for onboarding friction, knowledge transfer, and cross-team communication overhead:

- **Team A Available Capacity (6 Engineers):**
  $$\text{Nominal Hours (Team A)} = 6 \text{ engineers} \times 10 \text{ days} \times 6 \text{ hours} = 360 \text{ nominal hours}$$
- **Team B Available Capacity (7 Engineers with 40% Onboarding Drag):**
  $$\text{Nominal Hours (Team B)} = 7 \text{ engineers} \times 10 \text{ days} \times 6 \text{ hours} \times 0.60 = 252 \text{ nominal hours}$$
- **Combined Gross Capacity:**
  $$360 + 252 = 612 \text{ nominal engineering hours}$$

### 2.2 The Scaled Coordination Reserve (25%)
In a multi-team environment, cross-team syncs, merge conflict resolution, interface alignments, and joint reviews demand a higher operational buffer. The operational reserve is expanded from 20% to **25%** (153 hours):

$$\text{Net Focused Engineering Capacity} = 612 \times (1 - 0.25) = \mathbf{459 \text{ focused hours}}$$

### 2.3 The Capacity Reality Check
Comparing the scaled capacity to the original Sprint 1 capacity:
$$\text{Scaling Ratio} = \frac{459 \text{ hours}}{336 \text{ hours}} \approx \mathbf{1.37\times}$$
Adding a second team increases effective delivery capacity by **only 37%**, entirely debunking management's naive assumption of a 100% (2.0×) increase. Consequently, the combined planned commitment for Sprint 2 is capped at **22 Story Points across both teams** (Team A: 12 points, Team B: 10 points).

---

## 3. Lightweight Scaled Agile and Lean Coordination Architecture

To coordinate 13 engineers without saddling them with heavy enterprise ceremony frameworks (such as full SAFe Portfolio or Large-Scale Scrum), the team deploys a **pragmatic, lightweight scaled delivery framework**:

```
                              ┌─────────────────────────────────────────┐
                              │       ONE SHARED PRODUCT BACKLOG        │
                              │    (Single Product Owner Governance)    │
                              └────────────────────┬────────────────────┘
                                                   │
                  ┌────────────────────────────────┴────────────────────────────────┐
                  ▼                                                                 ▼
      ┌───────────────────────┐                                         ┌───────────────────────┐
      │   TEAM A: CORE ENGINE │                                         │ TEAM B: REGIONAL & UX │
      │  (Order, Stock, Track)│                                         │ (Policy, Refund, UI)  │
      └───────────┬───────────┘                                         └───────────┬───────────┘
                  │                                                                 │
                  └───────────────────────────────┬─────────────────────────────────┘
                                                  │
                                                  ▼
                               ┌─────────────────────────────────────┐
                               │     SHARED INTEGRATION LANE (WIP: 2)│
                               │  Contract Tests, Daily Cross-Sync   │
                               │  Lead Integration Owner Sign-Off    │
                               └─────────────────────────────────────┘
```

### Core Coordination Pillars:
1. **Single Shared Backlog:** Both teams pull work from a unified backlog prioritized by one Product Owner, eliminating conflicting departmental goals.
2. **Synchronized Sprints:** Both teams run on identical 2-week iteration cycles with unified planning, demo, and retrospective meetings.
3. **Dedicated Integration Owner:** A designated senior engineer acts as Integration Owner, holding veto authority over PR merges into the shared trunk and enforcing contract compatibility.
4. **Shared Integration Lane (WIP Limit = 2):** A dedicated board swimlane monitors cross-team pull requests. At most 2 cross-team integration items can be active simultaneously.
5. **Twice-Weekly Dependency Standup (Scrum of Scrums):** A 15-minute sync on Tuesdays and Thursdays between Team A and Team B leads to resolve interface blockers.
6. **Joint Sprint Review & Demonstration:** Both teams present an integrated increment in a single 45-minute live demo to warehouse and finance stakeholders.
