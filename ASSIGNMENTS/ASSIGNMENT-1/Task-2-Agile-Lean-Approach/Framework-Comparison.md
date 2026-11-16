# Task 2: Project Management Delivery Framework Comparison

## 1. Context and Evaluation Objectives
The project scenario demands an initial release within a fixed 8-week timeframe prior to a commercial festival sale. The team consists of seven cross-functional engineers with no historical velocity data. Critical external dependencies—specifically the payment gateway sandbox (Week 4) and barcode scanners (Week 5)—impose sequential constraints. Furthermore, key operational stakeholders (Warehouse and Finance) are available for only 90 minutes per week.

To determine the optimal delivery mechanism, two established Agile methodologies were analyzed:
1. **Approach 1: Scrum with Lean Flow Controls (Time-Boxed Cadence + WIP Constraints)**
2. **Approach 2: Continuous Flow Kanban with Fixed Release Milestones**

---

## 2. Comprehensive Comparative Matrix

| Evaluation Dimension | Approach 1: Scrum with Lean Flow Controls | Approach 2: Kanban with Release Milestones | Comparative Analysis & Scenario Fit |
|---|---|---|---|
| **Work Selection & Planning** | Iterative sprint planning at the start of each two-week cycle; work is selected against a single, coherent Sprint Goal from a refined, prioritized backlog. | Continuous pull system; team members pull the next highest-priority ready item whenever active WIP limits permit. | Scrum's explicit Sprint Goal focuses cross-functional team members on completing shared vertical slices rather than optimizing individual task throughput. |
| **Operating Cadence & Coordination** | Structured 2-week time-boxes; 15-minute daily standups; mid-sprint backlog refinement; formal sprint reviews and retrospectives. | Event-driven cadence; daily standup at the flow board; weekly service delivery reviews; replenishment meetings when backlog buffers drop below threshold. | Scrum's fixed ceremony calendar provides predictability for warehouse and finance stakeholders whose availability is strictly capped at 90 minutes/week. |
| **Change Handling & Flexibility** | Scope is locked during the sprint; emergency requests require formal Product Owner evaluation and trading out equivalent planned story points to preserve the Sprint Goal. | Dynamic continuous reprioritization; new high-priority items can be placed at the top of the backlog queue or pulled immediately via an Expedite swimlane. | Kanban offers superior immediate reactivity, but in an 8-week hard-deadline scenario, unconstrained reprioritization risks scope thrashing and unfinished core journeys. |
| **Stakeholder Review Cadence** | Bi-weekly increment demonstrations where stakeholders interact directly with completed, deployable software slices. | Asynchronous or cadence-based reviews of completed features as they reach the final stage. | Scrum aligns perfectly with the 90-minute weekly stakeholder constraint: 45 minutes for review/demo and 45 minutes for backlog refinement. |
| **Suitability for Scenario** | **HIGH.** Ideal for fixed-date deliveries requiring phased integration of delayed external dependencies (payment gateway in Week 4, scanners in Week 5). | **MODERATE.** Highly effective for ongoing maintenance, bug fixing, or steady-state operations, but less protective against milestone slippage in a greenfield project. | Scrum's cadence forces early integration and testing before moving to subsequent architectural tiers. |
| **Operational Overhead** | Moderate ceremony overhead (Sprint Planning: 2h, Review: 1h, Retro: 1h, Refinement: 1.5h per 2-week cycle = ~5.5h / 80h per person, or ~6.8%). | Low administrative overhead; minimal ceremonies outside daily standups and ad-hoc replenishment. | Scrum's ceremony overhead is justified by the alignment, risk mitigation, and empirical inspection it provides to a newly formed team. |
| **Delivery Risks & Limitations** | Risk of overcommitment in early sprints due to lack of historical velocity data. Mitigated by setting an initial conservative velocity ceiling (16 points) and an explicit 20% buffer. | Risk of "milestone drift" where architectural foundations and complex integrations are continuously postponed in favor of easier, isolated tasks. | Pure Kanban lacks the forcing function of sprint boundaries needed to coordinate multi-role handoffs between API, UI, Database, and QA engineers. |

---

## 3. Justified Selection: Scrum Tailored with Lean Flow Controls

**Selected Approach:** **Scrum augmented with Lean Flow Controls.**

### Justification Rationale:
1. **Synchronization with Scarce Stakeholders:** The 90-minute weekly availability of warehouse and finance representatives makes an ad-hoc, pull-based review model unviable. A structured sprint review every two weeks provides predictable, non-negotiable review checkpoints.
2. **Mitigation of Unknown Velocity:** Because the team has never worked together on this codebase, pure Kanban provides no bounding box for capacity commitment. Scrum enforces an explicit planning ceiling (16 points in Sprint 1) combined with an empirical inspect-and-adapt retrospective cycle.
3. **Incorporation of Lean Principles:** Pure Scrum often allows excessive parallel development within a sprint, resulting in a chaotic "scramble" at sprint end where stories pile up in the testing column. By embedding strict **Work-in-Progress (WIP) limits** (Development = 4, Review = 2, Test = 2), the team prevents QA bottlenecks and ensures stories meet the Definition of Done incrementally throughout the sprint.
