# Task 2: Explicit Planning Assumptions and Open Questions

In software engineering, explicit identification of planning assumptions and unresolved domain questions separates disciplined analysis from speculative development.

---

## 1. Explicit Planning Assumptions

| ID | Planning Assumption | Engineering Justification | Operational & Validation Impact |
| :--- | :--- | :--- | :--- |
| **A01** | Bounded Initial Release Scope | The representative system release operates across an initial bounded environment (3 baseline regions, expandable to 12) managed by a small technical team. | Avoids excessive microservice operational overhead; justifies a modular monolith architecture. |
| **A02** | 15-Minute Reservation Expiry | An unpaid stock reservation expires exactly 15 minutes after order placement if no payment confirmation is received. | Standard retail benchmark balancing cart completion time against blocking inventory from competing buyers. |
| **A03** | 24-Hour Dispatch SLA Window | Dispatch SLA is targeted at 24 hours post-payment confirmation, calculated strictly in Coordinated Universal Time (UTC). | Prevents timezone ambiguity across multi-regional warehouse operations. |
| **A04** | Dual-Control Refund Limit (\$50.00) | Refunds with monetary value exceeding \$50.00 require human Finance Reviewer approval; amounts equal or below can be policy-approved. | Establishes a concrete parameter for automated unit and integration tests. |
| **A05** | Strict Synthetic Data Usage | All customer profiles, payment references, SKUs, and addresses are purely synthetic. No real cardholder PANs or PII exist in the system. | Eliminates regulatory PCI-DSS and GDPR exposure during academic evaluation. |
| **A06** | Deterministic Integration Adapters | External Payment Gateway and Courier APIs are integrated via deterministic mock adapters when live partner credentials are unavailable. | Allows reproducible testing of network timeouts, 503 errors, duplicate callbacks, and retries in automated CI pipelines. |
| **A07** | Expansion Planning Target Metrics | The Day-4 expanded workload of 500 simultaneous users and 1,000 events/min (~16.7 events/sec avg, ~83.3 events/sec peak) across 12 regions is a **design planning target**, not demonstrated system capacity. | Distinguishes theoretical architectural capacity from empirically validated load benchmark results. |

---

## 2. Unresolved Domain Questions and Stakeholder Follow-Ups

The following open questions were identified during requirements elicitation and require executive confirmation prior to enterprise production deployment:

1. **Configurable Refund Approval Threshold:**
   - *Question:* Should the \$50.00 approval threshold be uniform across all 12 global regions, or should it vary dynamically based on local currency purchasing power parity (PPP) and regional fraud rates?
   - *Action Required:* Convene formal review with Chief Financial Officer and Regional Controllers.

2. **Reservation Expiry Optimization for High-Velocity Flash Sales:**
   - *Question:* During limited-time promotional events (e.g., Black Friday), is a 15-minute reservation hold too long, and should high-demand SKUs enforce a dynamic 5-minute checkout countdown?
   - *Action Required:* Coordinate with Marketing and Merchandising Directors.

3. **Regional Return Windows and Restocking Fee Policies:**
   - *Question:* Do statutory consumer protection regulations in European regions (EU-CENTRAL) mandate a 14-day unconditional return window, whereas North American regions enforce 30 days with a 10% restocking fee?
   - *Action Required:* Obtain legal compliance review by regional jurisdiction.

4. **Customer Data Retention and Right-to-be-Forgotten:**
   - *Question:* What is the statutory retention duration for completed order transaction records and shipping addresses before anonymization or hard deletion under GDPR Article 17?
   - *Action Required:* Coordinate with Data Protection Officer (DPO) and Legal Counsel.

5. **Edge Scanner Queue Storage Limits:**
   - *Question:* What is the maximum physical memory allocation and time limit for disconnected warehouse scanner offline event buffering before an audible alert sounds to prevent device RAM exhaustion?
   - *Action Required:* Consult with Warehouse Logistics Operations Lead and Hardware Vendor.
