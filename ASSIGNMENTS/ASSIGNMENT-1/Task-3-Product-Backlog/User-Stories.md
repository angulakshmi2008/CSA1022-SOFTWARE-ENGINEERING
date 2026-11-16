# Task 3: Refined Product Backlog User Stories

## 1. Prioritization Rationale: MoSCoW Methodology
Priorities are assigned using the **MoSCoW** framework based on customer harm, regulatory compliance, end-to-end dependency sequencing, and delivery feasibility:
- **Must Have (M):** Release-critical stories required to complete the core order-to-refund journey. Without these, the platform cannot launch.
- **Should Have (S):** Important features that enhance operational efficiency (e.g., support lookup, barcode verification, low-stock alerts) but can be temporarily worked around or deferred if capacity collapses.
- **Could Have (C):** Desirable features (e.g., sales analytics reconciliation) that are non-critical and will only be developed if surplus capacity is available.
- **Won't Have (W):** Explicitly deferred capabilities (e.g., ML forecasting, loyalty engines).

---

## 2. Comprehensive User Story Catalogue

| Story ID | Epic | User Story Statement (Role / Want / Benefit) | Priority | Estimate (Pts) | Dependencies | Assigned Role | Target Sprint |
|---|---|---|---|---|---|---|---|
| **S01** | E4 | **As an** authenticated system user (Customer, Picker, Support, Finance, Admin),<br>**I want** to log in securely and receive a scoped session token,<br>**so that** I can access only the features and data permitted by my assigned role. | **Must** | **3** | None | Payments & Security | Sprint 1 |
| **S02** | E1 | **As an** online customer,<br>**I want** the system to atomically reserve inventory for 15 minutes when I initiate checkout,<br>**so that** items cannot be oversold to other customers while I complete payment. | **Must** | **5** | S01 | Order API + Inventory | Sprint 1 |
| **S03a** | E2 | **As a** checkout customer,<br>**I want** my payment submission to generate a unique idempotency key and communicate with a local payment adapter,<br>**so that** network timeouts or repeated clicks never result in duplicate orders or charges. | **Must** | **2** | S02 | Payments & Security | Sprint 1 |
| **S03b** | E2 | **As a** backend order service,<br>**I want** the payment adapter to communicate with the external payment gateway sandbox API,<br>**so that** real-world authorization, decline, and timeout responses are properly handled. | **Must** | **3** | S03a, Gateway Sandbox (Wk 4) | Payments & Security | Sprint 3 |
| **S04** | E3 | **As a** warehouse picker,<br>**I want** to view a dedicated digital pick list displaying only paid and inventory-reserved items for my warehouse,<br>**so that** I never waste time searching for unpaid, cancelled, or missing stock. | **Must** | **3** | S02 | Inventory & Database | Sprint 1 |
| **S05** | E3 | **As a** warehouse supervisor,<br>**I want** to transition orders through valid fulfillment lifecycle states (`PICKING` → `PICKED` → `DISPATCHED` → `DELIVERED`),<br>**so that** order progression is strictly controlled and audited. | **Must** | **5** | S03a, S04 | Order API | Sprint 2 |
| **S06** | E3 | **As an** online customer,<br>**I want** to view a milestone-based tracking timeline (`Paid`, `Picked`, `Dispatched`, `Delivered`) via a screen-reader accessible page,<br>**so that** I know exactly when my package will arrive without calling support. | **Must** | **3** | S05 | Frontend Engineer | Sprint 2 |
| **S07** | E2 | **As an** authenticated customer,<br>**I want** to submit a return request for an eligible delivered order within 14 days of delivery,<br>**so that** I can initiate a return when goods are damaged or unsuitable. | **Must** | **3** | S05 | Order API | Sprint 3 |
| **S08** | E2 | **As a** finance reviewer,<br>**I want** to review pending return refunds and approve or reject them based on strict monetary authority thresholds,<br>**so that** financial disbursements are auditable and unauthorized staff cannot issue refunds. | **Must** | **5** | S03a, S07 | Payments & Security + Finance | Sprint 3 |
| **S09a** | E4 | **As a** software engineer,<br>**I want** the local repository to build and execute core automated smoke checks via a single shell command,<br>**so that** codebase integrity is easily verified from a fresh clone. | **Must** | **3** | None | DevOps Engineer | Sprint 1 |
| **S09b** | E4 | **As a** development team,<br>**I want** continuous integration checks to run automated unit, integration, and security tests on pull requests,<br>**so that** regressions are caught before merging into the main branch. | **Should** | **2** | S09a | DevOps Engineer | Sprint 2 |
| **S10** | E4 | **As a** customer support agent,<br>**I want** to search customer orders by Order ID or email to view tracking timelines, payment status, and return history,<br>**so that** I can resolve customer inquiries within 60 seconds without write privileges. | **Should** | **3** | S05, S07, S08 | Frontend + Order API | Sprint 4 |
| **S11** | E1 | **As a** store manager,<br>**I want** the system to flag a low-stock alert whenever available inventory for any SKU dips below a deterministic safety threshold,<br>**so that** store replenishment can be triggered before stock runs out. | **Should** | **3** | S04 | Inventory & Database | Sprint 2 |
| **S12** | E3 | **As a** warehouse picker,<br>**I want** to scan item barcodes using the test scanner device to verify that the picked item matches the order specification,<br>**so that** picking errors and incorrect parcel dispatches are eliminated. | **Should** | **3** | S04, Scanner Hardware (Wk 5) | Inventory & Database | Sprint 3 |
| **S13** | E4 | **As an** operations executive,<br>**I want** a sales analytics summary that reconciles daily transaction totals against completed order records,<br>**so that** financial revenue and dispatch quantities can be verified. | **Could** | **3** | S05 | Frontend + Data | Deferred / Roadmap |

---

## 3. Backlog Statistics Summary
- **Total Backlog Items:** 15 Refined Stories (13 primary requirements with S03 and S09 split for technical decoupling).
- **Total Backlog Story Points:** 46 Story Points.
- **Must-Have Points:** 32 Points (Core Release Baseline).
- **Should-Have Points:** 11 Points (Enhancements & Operational Efficiency).
- **Could-Have Points:** 3 Points (Deferred Analytics).
