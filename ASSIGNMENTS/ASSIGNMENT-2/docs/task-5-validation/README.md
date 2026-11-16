# Task 5: Critical Behaviour Validation and Design Revision

## 1. Task Overview and Assessment Mapping
- **Assessed Area:** Critical Behaviour Validation and Design Revision
- **Course Outcome:** CO2 – Analyze software requirements to design scalable and efficient system architectures using collaborative tools and structured modeling.
- **Marks Allocated:** 7 Marks
  - Invariants and two operation contracts (2 marks)
  - Six validation scenarios, predictions, and appropriate validation evidence (3 marks)
  - Identified weakness and documented design revision (2 marks)

## 2. Directory Structure and Deliverables
```text
docs/task-5-validation/
├── README.md                          # This document
├── invariants.md                      # 7 fundamental system invariants enforced throughout operation
├── operation-contracts.md             # Formal operation contracts for PlaceOrder, ConfirmPayment, and ExecuteRefund
├── validation-scenarios.md            # Detailed specification of Scenarios T1 through T7
├── design-revisions.md                # 2 critical design weaknesses identified and architectural revisions
└── evidence/
    └── test-execution-evidence.md     # Genuine automated test execution results (T1-T11)
```

## 3. Empirical Verification Integrity
In strict compliance with the faculty evaluation guide:
- All results marked as **demonstrated** were produced by running the automated verification suite (`scripts/run_all_tests.py`) against the actual backend application and SQLite/PostgreSQL transactional engine.
- Predicted specifications were documented prior to test execution.
- Two specific weaknesses discovered during structural walkthroughs and test development were corrected in code and validated through dedicated test cases (`T3` and `T7`).
