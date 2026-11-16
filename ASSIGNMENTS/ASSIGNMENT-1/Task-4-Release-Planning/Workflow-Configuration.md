# Task 4: Development Workflow Configuration and WIP Policies

## 1. Development Issue Workflow vs Operational Order Lifecycle

A common failure mode in Agile engineering projects is confusing the **software development task workflow** with the **business domain order lifecycle**. The team establishes an explicit architectural separation between these two state machines:

```
[Development Issue Workflow (Jira / Board State Machine)]
Ready ──► In Progress ──► Review ──► Test ──► Done
             ▲              │          │
             └── (Rework) ──┴──────────┘
             │
             └──► Blocked ──► In Progress

-----------------------------------------------------------------------------------------

[Operational Order Lifecycle (E-Commerce Domain State Machine)]
CREATED ──► RESERVED ──► PAID ──► PICKING ──► PICKED ──► DISPATCHED ──► DELIVERED
                                                                           │
                                                                           ▼
REFUNDED ◄── REFUND_PENDING ◄── RETURN_REQUESTED ◄─────────────────────────┘
```

---

## 2. Development Workflow State Transitions and Quality Gates

| Status Name | Entry Criteria (Quality Gate In) | Transition & Work Rules | Exit Criteria (Quality Gate Out) |
|---|---|---|---|
| **Ready** | Story satisfies the Definition of Ready (DoR); estimates, dependencies, acceptance criteria, and owner assigned. | Backlog container. Items are pulled into development strictly based on priority when WIP permits. | Team member pulls card into `In Progress`. |
| **In Progress** | Developer capacity available; active column WIP < 4. | Active coding, unit test implementation, and local test double verification. | Code complete, local smoke tests pass, pull request created. |
| **Review** | Pull request submitted; active column WIP < 2. | Peer engineer inspects code quality, architecture compliance, test coverage, and security patterns. | At least one peer approval; clean CI build. |
| **Test** | Code merged to integration branch; active column WIP < 2. | Dedicated QA verification. Execution of automated integration tests, negative edge-case tests, and accessibility audits. | All acceptance criteria validated; QA signs off against Definition of Done (DoD). |
| **Blocked** | An active item is impeded by an external blocker, third-party dependency, or unclarified requirement. | Card is visually flagged with red blocker indicator. Reason, blocked dependency, owner, and escalation timer recorded. Item **remains counted against active column WIP**. | Blocker resolved or Product Owner substitutes scope; card returns to its active development status. |
| **Done** | All eight conditions of the Definition of Done (DoD) are 100% satisfied. | Terminal state. Working software deployed to staging environment; issue closed with linked test evidence. | Story closed; completed points credited to sprint velocity. |

---

## 3. Work-in-Progress (WIP) Policy Justification

The team enforces explicit column WIP limits on the active board:

```
┌──────────────┬──────────────────┬──────────────────┬──────────────────┬──────────────┐
│    Ready     │   In Progress    │      Review      │       Test       │     Done     │
│  (Unlimited) │    [ WIP: 4 ]    │    [ WIP: 2 ]    │    [ WIP: 2 ]    │  (Terminal)  │
└──────────────┴──────────────────┴──────────────────┴──────────────────┴──────────────┘
```

### Justification Rationale:
1. **Development Limit (4 Items):** With seven engineers (1 PO, 1 QA, 1 DevOps, and 4 active developers), a limit of 4 ensures that each developer focuses on finishing a single story rather than opening multiple half-finished tasks.
2. **Review Limit (2 Items):** Prevents completed code from languishing in review queues. When the review limit is reached, developers are forbidden from pulling new work into `In Progress`; they must review pending pull requests.
3. **Test Limit (2 Items - The Tightest Control):** The team has only **one dedicated QA engineer**. If more than two items enter testing simultaneously, the QA engineer becomes overwhelmed, leading to rushed testing and leaked regressions. The test limit acts as a circuit breaker for the entire delivery system.

---

## 4. Handling Blockers, Expedited Requests, and Unfinished Work

### 4.1 Blocked Work Protocol
- When an item is blocked, it transitions to `Blocked` but **continues to occupy WIP capacity** in its originating column. This deliberate friction prevents developers from simply abandoning blocked tasks to start new work, which would inflate overall system WIP.
- If an item remains blocked for more than 24 hours (1 working day), it triggers the **One-Working-Day Escalation Rule**, compelling the Product Owner to intervene.

### 4.2 Expedite Swimlane Policy
- An emergency production defect or critical compliance mandate may bypass standard sprint prioritization via an **Expedite Swimlane**.
- **The Trade-Out Rule:** To prevent scope creep and maintain sustainable pace, admitting 1 expedite item into the sprint strictly requires the Product Owner to negotiate and remove an equivalent number of planned story points from the active sprint backlog.
- At most **one** expedite item is permitted in active flight at any time.

### 4.3 Management of Unfinished Work (Carryover)
- If a user story fails to meet all Definition of Done criteria by the conclusion of Sprint Review, it is classified as **Unfinished Work**.
- **Zero Partial Credit:** In strict accordance with Agile principles, zero partial story points are awarded (e.g., a 5-point story that is 90% coded receives 0 points for that sprint).
- **Backlog Return:** The story returns to the Product Backlog, where the Product Owner re-evaluates its priority. If selected for the subsequent sprint, it is clearly tagged as **Carryover**.
- **Velocity Anti-Double-Counting:** In the subsequent sprint, only the remaining uncompleted effort is planned, and velocity credit is recorded only upon full completion to prevent artificially inflating team velocity across multiple sprints.
