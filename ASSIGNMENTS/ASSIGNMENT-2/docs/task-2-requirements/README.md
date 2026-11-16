# Task 2: Prioritized and Testable Requirements Specification

## 1. Task Overview and Assessment Mapping
- **Assessed Area:** Prioritized and Testable Requirements Specification
- **Course Outcome:** CO2 – Analyze software requirements to design scalable and efficient system architectures using collaborative tools and structured modeling.
- **Marks Allocated:** 8 Marks
  - Twelve functional and six non-functional requirements (3 marks)
  - Identifiers, sources, priorities, and measurable acceptance criteria (2 marks)
  - Order rules, assumptions, and stakeholder conflict influence (2 marks)
  - Documentation and issue-tracker evaluation & traceability (1 mark)

## 2. Directory Structure and Deliverables
```text
docs/task-2-requirements/
├── README.md                          # This document
├── functional-requirements.md         # 14 uniquely identified Functional Requirements (FR01-FR14)
├── non-functional-requirements.md     # 8 quantified Non-Functional Requirements (NFR01-NFR08)
├── business-rules.md                  # Comprehensive order lifecycle and governance rules
├── assumptions-and-open-questions.md  # Explicit planning assumptions (A01-A07) & unresolved questions
├── prioritization-method.md           # Risk-adjusted MoSCoW rationale & conflict-driven requirements
└── tool-evaluation.md                 # Comparative analysis: Jira/Confluence vs. GitHub repository
```

## 3. Requirements Engineering Rigor
In compliance with the official assignment specification:
1. **Replacement of Vague Goals:** Colloquial descriptions such as "checkout should be fast" or "the system should be highly available" have been systematically eliminated. Each non-functional requirement specifies an operational condition, a quantitative measurement metric (e.g., p95 latency < 800 ms at 50 concurrent synthetic users), and an observable validation vector.
2. **Conflict Traceability:** Two major stakeholder conflicts directly shaped requirements:
   - Conflict 1 (Checkout Speed vs. Stock Accuracy) directly resulted in **FR03 (Atomic Reservation)** and **FR08 (Reservation Expiry with Reconciliation)**.
   - Conflict 4 (Fast Refunds vs. Financial Control) directly shaped **FR10 (Dual-Control Refund Workflow)**.
3. **Traceability IDs:** All requirements are assigned permanent identifiers (`FR01`–`FR14`, `NFR01`–`NFR08`) referenced in UML models (Task 3), Architectural Decision Records (Task 4), and automated validation tests (Task 5 & 6).
