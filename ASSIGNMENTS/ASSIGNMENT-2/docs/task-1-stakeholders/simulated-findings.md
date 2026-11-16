# Task 1: Simulated Stakeholder Findings

> **Methodological Disclaimer:** As required by Section 1 and Q1 of the official CSA10 specification, the following findings represent **simulated responses** based on an industry standard retail process review. No actual proprietary interviews were conducted.

---

### Finding 1: Customer Representative (Simulated Persona: "Retail Shopper")
- **Core Expectation:** Customers demand zero-friction ordering. When an item appears as "In Stock", checkout should complete under 1 second. Once paid, tracking should update in near real-time.
- **Pain Points:** 
  - Having an item vanish from cart during checkout without clear feedback.
  - Being billed twice if network glitches cause duplicate callback or page refresh.
  - Lengthy delays when requesting returns and uncertainty regarding refund approval.
- **Privacy Perspective:** Expects card numbers, CVVs, and complete addresses to remain confidential and inaccessible to floor staff or third-party couriers.

---

### Finding 2: Warehouse Picker (Simulated Persona: "Floor Lead Marcus")
- **Core Expectation:** Requires an authoritative, steady pick list on handheld terminals. When an order appears on the dashboard, the item MUST physically exist in the specified aisle and bin.
- **Pain Points:** 
  - Picking an item only to find the customer cancelled or the reservation expired while en route, resulting in wasted walking time and inventory restock overhead.
  - "Ghost stock" resulting from concurrent web checkout races that sell units not physically present.
- **Operational Need:** Only orders that are verified as `PAID` with confirmed reservations should enter the picking queue. Pick confirmation must precede physical dispatch.

---

### Finding 3: Support Agent (Simulated Persona: "Senior Agent Priya")
- **Core Expectation:** Needs instantaneous lookup of customer order history, shipment milestones, and courier tracking identifiers using order IDs or customer email.
- **Pain Points:** 
  - Having customers complain about delayed shipments without having visibility into courier tracking numbers.
  - Being unable to submit return requests on behalf of non-technical or distressed customers.
- **Permission Limitation:** Acknowledges that support staff should NOT have the ability to view credit card details, edit order prices, or directly approve cash refunds, as this presents an internal fraud risk.

---

### Finding 4: Finance Reviewer (Simulated Persona: "Financial Controller Elena")
- **Core Expectation:** Absolute accountability, audit trails, and segregation of duties. Every financial outflow (refund) must tie back to a verified original payment event, return authorization, and authenticated reviewer signature.
- **Pain Points:** 
  - Automated or support-initiated refunds being executed without oversight, leading to revenue leakage.
  - Gateway retry anomalies resulting in double refund disbursements.
- **Regulatory Rule:** Refunds equal to or below a baseline threshold (e.g., \$50.00) can proceed via automated policy checks, but any refund above \$50.00 requires explicit dual-control (human finance review). A support agent must never be able to approve or execute a refund.

---

### Finding 5: Store Manager (Simulated Persona: "Regional Director Chen")
- **Core Expectation:** Comprehensive aggregated metrics across all stores and fulfilment nodes: gross revenue, tax collected, stock turnover, pending dispatch backlogs, and refund loss rates.
- **Pain Points:** 
  - Operational databases grinding to a halt during end-of-day reporting queries because complex SQL `JOIN`s compete with high-volume customer checkout transactions.
  - Inconsistent regional tax and shipping calculations across multiple jurisdictions.
- **Analytical Need:** Read-only consolidated dashboards updated periodically without locking operational tables.

---

### Finding 6: Enterprise Administrator (Simulated Persona: "System Admin Alex")
- **Core Expectation:** Centralized, role-based access control (RBAC), immutable system audit logs, and configuration management for regional shipping rates, tax rules, and refund limits.
- **Pain Points:** 
  - Client-side privilege escalation (e.g., users spoofing roles via dropdowns or modified JWT payloads).
  - Lack of traceability when system parameters are altered.
- **Security Rule:** All authorization decisions must be strictly enforced on the server. Audit records must record the actor identity, action type, entity ID, previous version, and timestamp.
