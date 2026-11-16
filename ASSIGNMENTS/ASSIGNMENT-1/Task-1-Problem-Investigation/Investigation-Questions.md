# Task 1: Stakeholder Investigation Questions

## 1. Overview
To establish an evidence-based Agile delivery strategy, the development team formulated targeted investigation questions addressing key operational vulnerabilities identified in the omnichannel retail scenario. In the absence of live corporate access, all findings represent structured, simulated stakeholder responses.

---

## 2. Investigation Questions and Analytical Objectives

### Question 1: Inventory Synchronization & Overselling Vulnerability
> *"Where and why do discrepancies occur between online inventory availability and physical store/warehouse shelves, and at what exact lifecycle event must inventory be locked?"*
- **Target Stakeholders:** Warehouse Pickers, Store Managers, Inventory Database Engineer.
- **Underlying Risk:** If stock is decremented only upon payment or physical dispatch, concurrent orders can claim the same stock, leading to out-of-stock cancellations, negative inventory, and customer dissatisfaction.
- **Investigation Objective:** Determine whether an atomic stock reservation mechanism with an auto-releasing expiry timer (e.g., 15 minutes) is necessary during checkout.

### Question 2: Milestone Visibility vs Internal Operational Confidentiality
> *"Which order milestones are essential for customers and support agents to track order progress without exposing internal warehouse picking notes or sensitive routing logic?"*
- **Target Stakeholders:** Customers, Support Agents, Frontend Engineer.
- **Underlying Risk:** Displaying a vague "Processing" status for multiple days causes high call volumes to customer support. Conversely, leaking internal warehouse notes can compromise internal operational security and confuse customers.
- **Investigation Objective:** Define a standardized public order state model with explicit customer-facing milestones (`Paid`, `Picked`, `Dispatched`, `Delivered`).

### Question 3: Payment Gateway Resilience & Idempotency Rules
> *"What should happen when a payment transaction times out or the external gateway sandbox is unreachable, and how do we ensure retried requests never result in duplicate financial charges?"*
- **Target Stakeholders:** Payments & Security Engineer, Finance Reviewer, Customer.
- **Underlying Risk:** Network partitions or gateway downtime could cause duplicate card charges upon retry, or cause orders to be abandoned without a local audit trail.
- **Investigation Objective:** Establish a unique client-side idempotency key contract and local fallback stub to allow safe transaction retries without double charging.

### Question 4: Refund Authorization Governance & Internal Audit Trails
> *"What specific governance rules and role-based permissions must dictate refund issuance, and what audit information is mandatory for corporate accounting reconciliation?"*
- **Target Stakeholders:** Finance Reviewer, Store Managers, Support Agents.
- **Underlying Risk:** If customer support agents possess unconstrained refund approval authority, or if approvals occur via informal channels (e.g., Slack or chat), the retailer faces fraudulent payouts, revenue leakages, and audit failure.
- **Investigation Objective:** Design a role-based authorization check enforcing monetary thresholds (e.g., support can initiate return, but refunds require dual or finance approval) and an append-only audit trail.

### Question 5: Regional Tax & Warehouse Policy Variations
> *"Which regional discrepancies in tax calculation, courier shipping rates, and return windows must be supported across the physical warehouse network?"*
- **Target Stakeholders:** Store Managers, Regional Warehouse Supervisors, Product Owner.
- **Underlying Risk:** Hardcoding regional business logic into the core checkout pipeline leads to monolithic fragility and high regression risks when expanding across territories.
- **Investigation Objective:** Formulate a decoupled, table-driven regional policy engine that isolates regional rules from core order workflows.
