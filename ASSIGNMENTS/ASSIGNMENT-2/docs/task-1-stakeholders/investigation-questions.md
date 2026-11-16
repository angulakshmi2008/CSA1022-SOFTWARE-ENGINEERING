# Task 1: Stakeholder Investigation Questions

## 1. Investigation Methodology
To elicit non-obvious domain rules, edge cases, and architectural friction points, a structured process review was formulated. In accordance with the assignment instructions, because direct access to the commercial retailer's personnel was unavailable, all subsequent responses are **simulated findings** generated from retail fulfilment benchmarks.

The investigation focuses on five critical unresolved dilemmas:

---

### Question 1: Inventory Contention and Reservation Expiry Notification
> *"How should a warehouse picker be notified when a customer's reserved stock item expires or becomes unavailable while an active picking task is open on the warehouse floor?"*
- **Target Stakeholders:** Warehouse Picker, Warehouse Supervisor, Inventory Control Engineer.
- **Architectural Motivation:** Uncovers whether inventory reservation is purely soft (logical flag) or hard (transactional lease). Identifies whether real-time push notifications (e.g., WebSockets, push events) or pull-based polling is required on warehouse handheld devices, and defines what happens to physical items placed in a cart when a customer's payment window lapses.

---

### Question 2: Refund Governance and Segregation of Duties
> *"Which refund monetary thresholds require mandatory finance review, and under what conditions may a support agent or system process an immediate refund without secondary approval?"*
- **Target Stakeholders:** Support Agent, Finance Reviewer, Chief Financial Officer.
- **Architectural Motivation:** Determines the boundary between automated and human-governed workflows. Investigates whether support agents can execute refunds directly, preventing insider fraud, and clarifies whether the requester can simultaneously approve their own refund (strict four-eyes principle).

---

### Question 3: Customer Privacy versus Operational Support Visibility
> *"What specific customer order details must a frontline support agent inspect to resolve dispatch and tracking complaints, and which specific payment, address, or identity fields must remain strictly masked or redacted?"*
- **Target Stakeholders:** Customer, Support Agent, Compliance & Security Officer.
- **Architectural Motivation:** Explores the conflict between customer data privacy (GDPR, PCI-DSS) and support agent diagnostic velocity. Informs the API response schema to ensure sensitive payment credentials (e.g., card tokens, raw customer billing identifiers) are filtered at the server boundary rather than masked solely in the browser UI.

---

### Question 4: Distributed Integration Failure and Asynchronous Courier Handshake
> *"What operational protocol must be executed when a customer's order is successfully committed and marked 'Paid' locally, but the third-party courier dispatch API times out or returns a temporary 503 Service Unavailable?"*
- **Target Stakeholders:** Customer, Dispatch Manager, Integration Architect.
- **Architectural Motivation:** Defines the boundary between synchronous transactional persistence and asynchronous external communication. Tests whether an order can safely be accepted without blocking the customer checkout loop, necessitating a Transactional Outbox pattern with idempotent reconciliation.

---

### Question 5: Last-Unit Stock Race Conditions and Checkout Fairness
> *"How should the platform resolve a race condition where two simultaneous buyers attempt to checkout the single remaining unit of a high-demand SKU within the exact same millisecond window?"*
- **Target Stakeholders:** Customer, E-Commerce Store Manager, Backend Database Engineer.
- **Architectural Motivation:** Determines database locking semantics (optimistic concurrency with versioning vs. pessimistic row-level locking `SELECT ... FOR UPDATE`). Clarifies whether the second customer receives an immediate backorder, an out-of-stock notification, or a retry prompt.
