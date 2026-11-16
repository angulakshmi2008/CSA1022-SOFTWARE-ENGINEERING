# Task 5: Delivery Simulation Metrics and Bottleneck Analysis

> **Transparency Notice:** All data, event sequences, and metrics presented herein are **SIMULATED** for the purpose of validating the Agile operating model and do not represent empirical measurements from a commercial production team.

---

## 1. Bottleneck Prediction (Pre-Simulation Hypothesis)

Prior to initiating the Sprint 1 simulation, the team formulated an explicit architectural and workflow hypothesis regarding where the primary delivery bottleneck would manifest:

### 1.1 Predicted Bottleneck Location
- **Hypothesis:** The primary system bottleneck will emerge at the **QA Testing stage and the handoff between Inventory Reservation (S02) and Payment Idempotency (S03a)**.
- **Root Cause Drivers:**
  1. *Resource Asymmetry:* The team possesses four backend/full-stack developers producing code simultaneously, but only **one dedicated QA Engineer** responsible for authoring automated integration and concurrency tests.
  2. *Architectural Coupling:* Payment processing cannot proceed to valid integration testing without a stable, transaction-safe inventory reservation mechanism. If stock reservation exhibits subtle concurrency defects, downstream payment development is immediately stalled.

### 1.2 Control Rule and Evidence Metric
- **Enforced Control Rule:** Enforce a strict **Test column WIP limit of 2 items**, and activate the Lean principle: *"Stop starting, start finishing"*. When the Test queue reaches 2 items, developers are barred from pulling new stories into `In Progress` and must instead pair with QA to write test fixtures and verify acceptance criteria.
- **Validation Evidence:** A successful control rule will be demonstrated by: (a) Test column WIP never exceeding 2 items, (b) average dwell time in testing remaining under 24 hours, and (c) all concurrency defects being trapped *before* reaching the `Done` column.

---

## 2. Quantitative Delivery Indicators (Simulated)

| Delivery Indicator | Mathematical Formula | Target Planning Ceiling | Simulated Observed Value | Variance & Qualitative Assessment |
|---|---|---|---|---|
| **1. Planned vs Completed Work (Commitment Reliability)** | $\frac{\text{Completed Points}}{\text{Planned Points}} \times 100$ | 100% (16 Points) | **11 of 16 Points (68.75% / ~68.8%)** | **-31.25% Shortfall:** Three stories reached Done (S01: 3 pts, S04: 3 pts, S02: 5 pts). S03a (2 pts) and S09a (3 pts) were carried over to Sprint 2. |
| **2. Blocked Duration & Waiting Waste** | $\sum \text{Dwell time in Blocked status}$ | 0 Days | **2.0 Story-Days (S03a)** | **Unplanned Waiting:** S03a spent 2 days in `Blocked` waiting for the multi-threaded race condition in S02 to be debugged and re-tested. |
| **3. Test Queue Depth & Dwell Time** | $\text{Max concurrent cards in Test column}$ | $\le 2 \text{ Items}$ | **Peak: 2 Items (Average: 1.2)** | **Controlled Flow:** The Test WIP limit strictly prevented queue runaway. Average dwell time reduced from 2.0 days on Day 6 to 1.0 day on Day 9. |
| **4. Rework & Reopened Story Ratio** | $\frac{\text{Reopened Stories}}{\text{Completed Stories}}$ | 0.00 | **2 / 3 = 0.67 (67%)** | **High Initial Rework:** S01 was rejected at peer review for missing session expiry tests; S02 failed QA testing due to a concurrent reservation race condition. |

---

## 3. Detailed Metric Interpretation and Architectural Insights

### 3.1 Analysis of Commitment Reliability (68.8%)
The delivery of 11 out of 16 points is typical for a newly assembled team in Sprint 1. The shortfall was not caused by developer slacking, but rather by **underestimating the hidden complexity of concurrency control** in Story S02. Had the team not negotiated down from 21 points to 16 points in Task 4, completion reliability would have collapsed below 50%.

### 3.2 Analysis of the Dependency Trap (S02 → S03a)
The simulation demonstrated the danger of tight sequential dependencies. Because the payment stub (S03a) required a functioning order reservation ID from S02, when S02 was returned to `In Progress` on Day 8 to fix the database row lock, the payments engineer was stranded for 48 hours. This empirical finding proves that future sprints must utilize mock interface contracts to decouple dependent stories earlier.

### 3.3 Effectiveness of the WIP Circuit Breaker
The Test WIP limit of 2 items successfully prevented the single QA engineer from being inundated. When S02 and S01 were both undergoing verification, the limit prevented other developers from pushing S04 into testing prematurely. Furthermore, when S02 failed concurrency checks, the Order API engineer immediately swarm-paired on fixing the database transaction lock rather than starting unrelated work.

### 3.4 Root Cause of the 67% Rework Ratio
Both rework instances (S01 and S02) stemmed from an identical flaw: **incomplete negative acceptance criteria during Sprint Planning**. In S01, the team only specified happy-path login; in S02, the team only tested single-user checkout. This highlights the necessity of tightening the Definition of Ready to mandate multi-threaded and failure scenarios before coding begins.
