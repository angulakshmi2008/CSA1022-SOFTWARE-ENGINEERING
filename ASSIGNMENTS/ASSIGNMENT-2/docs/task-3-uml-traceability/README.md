# Task 3: UML Models and Requirements Traceability

## 1. Task Overview and Assessment Mapping
- **Assessed Area:** UML Modeling and Requirements Traceability
- **Course Outcome:** CO2 – Analyze software requirements to design scalable and efficient system architectures using collaborative tools and structured modeling.
- **Marks Allocated:** 7 Marks
  - Four consistent UML models (Use Case, Class, Sequence, State Machine) (4 marks)
  - Requirements-to-model-to-validation traceability matrix (2 marks)
  - Two identified inconsistencies and documented corrections (1 mark)

## 2. Directory Structure and Deliverables
```text
docs/task-3-uml-traceability/
├── README.md                          # This document
├── diagrams/                          # Standard PlantUML source files
│   ├── use-case.puml                  # Complete Use Case model with distinct actor boundaries
│   ├── class.puml                     # Domain Class diagram with relationships and constraints
│   ├── payment-courier-sequence.puml  # Detailed Sequence diagram with outbox, retry & reconciliation
│   ├── order-state-machine.puml       # Guarded Order lifecycle state machine
│   └── refund-state-machine.puml      # Dual-control Refund state machine with failure retry retention
├── traceability-matrix.md             # End-to-end Requirements -> UML -> Component -> Test matrix
└── modelling-inconsistencies.md       # 4 documented modeling anomalies and rigorous engineering corrections
```

## 3. Modeling Principles Applied
1. **Strict Separation of Concerns:** In accordance with faculty evaluation guidelines, UI actions are cleanly isolated from transactional domain commands. Refund request, approval, and execution are modeled as distinct use cases and state transitions.
2. **Asynchronous Distributed Boundaries:** The payment callback and courier sequence explicitly traces both synchronous database commits and asynchronous outbox worker execution, demonstrating how the system tolerates upstream partner failures.
3. **End-to-End Traceability:** Every functional and non-functional requirement mapped in Task 2 is formally traced to its corresponding UML element, underlying code implementation module, and automated verification test.
