# Task 4: Architectural Design and Justified Selection

## 1. Task Overview and Assessment Mapping
- **Assessed Area:** Alternative Architectures and Justified Design
- **Course Outcome:** CO2 – Analyze software requirements to design scalable and efficient system architectures using collaborative tools and structured modeling.
- **Marks Allocated:** 8 Marks
  - Two meaningful alternatives and comparative analysis (3 marks)
  - Selected architecture component, deployment, and consistency design (3 marks)
  - Three complete Architectural Decision Records (ADRs) (2 marks)

## 2. Directory Structure and Deliverables
```text
docs/task-4-architecture/
├── README.md                          # This document
├── architectural-alternatives.md      # In-depth comparison across 10 engineering dimensions
├── selected-architecture.md           # Formal defense of Modular Monolith + Durable Worker
├── diagrams/                          # PlantUML source for architecture views
│   ├── component-diagram.puml         # Component diagram with clean module boundaries
│   └── deployment-diagram.puml        # Physical containerized deployment diagram
└── adr/                               # Architectural Decision Records (MADR format)
    ├── ADR-001-relational-database.md # Decision on PostgreSQL relational transactional storage
    ├── ADR-002-transactional-outbox.md# Decision on Transactional Outbox vs. synchronous HTTP
    └── ADR-003-server-authorization-idempotency.md # Decision on server-side RBAC & idempotency
```

## 3. Key Architectural Decisions Summary
1. **Selection:** **Alternative A (Modular Monolith with Transactional Outbox Worker)** is selected over a distributed microservice architecture. While microservices offer theoretical decoupled scaling, they introduce distributed transactions (2PC/Sagas), eventual consistency edge cases, complex distributed tracing, and massive operational overhead that is unjustifiable for an initial release managed by a small engineering team.
2. **Consistency Guarantee:** Atomic ACID transactions in PostgreSQL guarantee that order placement, inventory reservation, and payment event recording execute with serializable integrity.
3. **Resilient Outbox Integration:** Third-party partner calls (courier APIs, payment gateway webhooks) are completely decoupled from synchronous web request threads using the Transactional Outbox pattern.
