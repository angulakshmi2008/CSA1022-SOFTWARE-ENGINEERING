# Task 5: Evidence-Based Improvements for Sprint 2 and Beyond

## 1. Limitations Identified from Sprint 1 Simulation

The empirical simulation of Sprint 1 exposed four specific operational vulnerabilities in the original plan:

1. **Velocity Over-Optimism:** Assuming the team could achieve a 16-point velocity in greenfield development without historical baselines led to a 31.25% completion shortfall (11 of 16 points delivered).
2. **Coupled Dependency Bottlenecks:** Tightly coupling S03a (Payments) directly to live S02 (Stock Reservation) code caused two full story-days of developer idle waiting when S02 experienced a concurrency defect.
3. **Defective Definition of Ready (DoR):** The DoR allowed stories to enter development without explicit negative boundary tests and concurrency criteria, leading to a high rework ratio (67%).
4. **Single QA Starvation Risk:** Although the Test WIP limit of 2 prevented QA queue runaway, the single QA engineer struggled to simultaneously build automated integration fixtures and execute manual edge-case testing.

---

## 2. Evidence-Based Corrective Actions for Sprint 2

To address these empirical findings, the Product Owner and Scrum Master implemented the following concrete adjustments:

```
[Sprint 1 Observation] ────────────────► [Sprint 2 Corrective Action]
• 11 points delivered (68.8%)          ──► Cap new commitment at 10 new points + 5 carried over.
• 2 story-days blocked on S03a         ──► Mandate contract-first API stubs before dependent coding starts.
• 2 stories reopened for rework        ──► Mandate negative & concurrency cases in the Definition of Ready.
• QA testing bottleneck                ──► Institute mandatory 30-minute daily Developer-QA pairing slots.
• Large 5-point story risk (S05)       ──► Split S05 into S05a (Core API: 3 pts) and S05b (Events: 2 pts).
```

### Action 1: Recalibrated Capacity Commitment
- Instead of planning 16 new story points for Sprint 2, the team recognizes the **5 points of unfinished carryover** (`S03a` [2 pts] and `S09a` [3 pts]).
- The new scope commitment is capped at **exactly 10 new story points**:
  - `S03a (2 pts - Carryover)` + `S09a (3 pts - Carryover)` = **5 Carryover Points**.
  - `S05a (3 pts - Core Dispatch API)` + `S06 (3 pts - Milestone Tracking)` + `S09b (2 pts - CI/CD Pipeline)` + `S11 (3 pts - Low-Stock Alert)` = **11 New Points**.
  - *Contingency Rule:* If mid-sprint velocity flags, `S11 (3 pts)` will be resequenced to Sprint 3 to protect the core dispatch and tracking pipeline.

### Action 2: Architectural Story Slicing (S05)
- Story `S05` (Fulfillment State Machine Transitions, 5 points) is identified as a high-risk multi-role story similar to `S02`.
- It is sliced into:
  - **S05a (3 points):** Core backend status transition API with ACID validation and audit ledger. *Scheduled in Sprint 2.*
  - **S05b (2 points):** Asynchronous carrier webhook notifications and event streaming. *Resequenced to Sprint 3.*

### Action 3: Contract-First Development Protocol
- Developers are forbidden from waiting for backend implementation before starting dependent stories.
- The team must agree upon a OpenAPI / JSON schema contract and deploy a local mock server on Day 1 of the sprint, enabling UI and dependent service engineers to develop against stubs immediately.

### Action 4: Mandatory Daily Developer-QA Pairing Slot
- A recurring 30-minute pairing window (11:00 AM – 11:30 AM daily) is instituted where the Order API and Payments engineers pair with the QA engineer to co-author automated test fixtures, reducing QA test dwell time by an estimated 50%.

### Action 5: Definition of Ready Hardening
- The DoR checklist is formally updated to mandate:
  > *"Every transactional user story must include at least two documented negative/boundary scenarios and one concurrent race condition test specification before entering the sprint."*
