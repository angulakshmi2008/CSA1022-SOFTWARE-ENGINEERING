# Task 5: Delivery Simulation and Design Validation

## Directory Contents

- [Sprint-1-Event-Log.csv](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-5-Sprint-Simulation/Sprint-1-Event-Log.csv): Detailed, 16-step simulated event log tracing stories S01, S02, S03a, S04, and S09a through planning, peer review, QA concurrency testing, rework, blocker states, and sprint closure. All entries are explicitly labelled as **SIMULATED**.
- [Sprint-Metrics.md](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-5-Sprint-Simulation/Sprint-Metrics.md): Empirical bottleneck analysis comparing pre-simulation predictions against four quantitative indicators: Commitment Reliability (68.8%), Blocked Effort (2.0 story-days), Test Queue Depth (peak: 2 items), and Rework Ratio (67%).
- [Improvement-Actions.md](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-5-Sprint-Simulation/Improvement-Actions.md): Five concrete corrective actions for Sprint 2, including commitment recalibration (10 new points + 5 carryover), architectural slicing of S05, contract-first development, daily QA pairing slots, and DoR hardening.

---

## Key Simulation Outcomes
1. **Delivered Velocity:** 11 of 16 planned Story Points completed (68.75%).
2. **Bottleneck Validated:** The single QA engineer and tightly coupled backend dependencies (S02 → S03a) created two story-days of waiting waste when concurrency defects surfaced.
3. **WIP Rule Efficacy:** The Test column WIP limit of 2 items successfully prevented queue runaway and compelled developers to assist with defect swarming.
