# Task 6: Day-4 Design Challenge – Architecture Redesign for Expansion and Partial Failure

## 1. Task Overview and Assessment Mapping
- **Assessed Area:** Expansion and Partial-Failure Redesign (Day-4 Challenge)
- **Course Outcome:** CO2 – Analyze software requirements to design scalable and efficient system architectures using collaborative tools and structured modeling.
- **Marks Allocated:** 10 Marks (Major Assessment Priority)
  - Part A: Diagnose the impact on requirements, assumptions, and quality attributes (2 marks)
  - Part B: Create the revised architecture, component responsibilities, buffering, and deduplication (4 marks)
  - Part C: Validate the redesign with at least three additional scenarios (T8, T9, T11) and evidence (2 marks)
  - Part D: Defend the design against costs, consistency vs. availability trade-offs, and limitations (2 marks)

## 2. Directory Structure and Deliverables
```text
docs/task-6-expansion/
├── README.md                          # This document
├── impact-analysis.md                 # Part A: Impact diagnosis across 12 regions and expanded workload
├── revised-architecture.md            # Part B: Architectural redesign and component responsibilities
├── synchronization-and-deduplication.md# Edge scanner synchronization protocol and deduplication rules
├── expansion-validation.md            # Part C: Validation of Scenarios T8, T9, T10, and T11 with evidence
├── cost-and-tradeoff-defence.md       # Part D: Budget defense, CAP theorem trade-offs, and limitations
└── diagrams/
    └── revised-deployment.puml        # Expanded multi-replica container deployment diagram
```

## 3. Changed Scenario Summary
The enterprise expands operations:
- **Geographic Scale:** Increased from 3 initial regions to **12 operating regions** worldwide.
- **Target Workload:** Increased from 50 to **500 simultaneous users** and from 100 to **1,000 operational events per minute** (~16.7 events/sec average, ~83.3 events/sec peak factor).
- **Regional Autonomy:** Each region defines independent, versioned sales tax rates, shipping fee structures, and refund approval monetary thresholds.
- **Intermittent Edge Connectivity:** Handheld warehouse scanners operate in warehouse dead zones, buffering scan events locally and syncing bursts upon reconnection.
- **Fraud Deterrence:** Locally queued refund approvals must remain `PENDING` until validated and committed by the central server.
- **Financial Constraint:** The operational infrastructure budget permits only a modest, justifiable expenditure increase.
