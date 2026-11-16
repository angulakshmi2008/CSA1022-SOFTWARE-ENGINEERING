# Task 6: Scaled Agile Redesign Under Changed Conditions

## Directory Contents

- [Impact-Analysis.md](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-6-Scaled-Agile-Redesign/Impact-Analysis.md): Detailed diagnosis of the five organizational disruptions (two regional warehouses, second 7-member team, departing payments engineer, regional tax/shipping rules, fixed deadline), evaluating capacity drag, Brooks' Law, and architectural coupling.
- [Revised-Strategy.md](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-6-Scaled-Agile-Redesign/Revised-Strategy.md): Six measurable redesign objectives, mathematical capacity recalculation yielding 459 net focused hours (~1.37× scaling factor, not 2.0×), and a lightweight scaled coordination model (shared backlog, synchronized sprints, integration lane WIP: 2).
- [Team-Responsibilities.md](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-6-Scaled-Agile-Redesign/Team-Responsibilities.md): Architectural boundaries between Team A (core transactional engine) and Team B (regional policies & UX), emergency payment knowledge transfer protocol, and Cross-Team Integration Owner authority.
- [Additional-Simulation.csv](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-6-Scaled-Agile-Redesign/Additional-Simulation.csv): Six simulated cross-team disruption events (SC-01 to SC-06) evaluating regional policy injection, schema merge conflicts, payments handover, sandbox delays, security gate triggers, and midpoint scope governance. All entries labelled as **SIMULATED**.
- [Performance-Comparison.md](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-6-Scaled-Agile-Redesign/Performance-Comparison.md): Side-by-side comparative validation across four delivery indicators (throughput: 11 vs 18 pts; reliability: 68.8% vs 81.8%; blocked duration: 2.0 vs 1.0 story-days; rework: 67% vs 33%) and an evidence-based strategic defense of the fixed festival deadline.

---

## Key Redesign Takeaways
1. **Brooks' Law Proved:** Adding a 7-member team yields only a 37% net capacity increase due to onboarding drag and cross-team coordination overhead.
2. **Interface Decoupling:** Isolating regional tax and shipping rules into table-driven configuration prevented core order code contamination.
3. **Resilient Governance:** A single shared backlog, contract-first stubs, and an active Integration Owner role halved blocked waiting time and rework ratios.
