# Project Assumptions and Operational Constraints

## Course: CSA10 – Software Engineering
**Assignment:** Omnichannel Order Fulfilment Platform Delivery Strategy  

---

## 1. Context and Organizational Background
A retail enterprise operates an e-commerce website, a mobile shopping application, and 12 physical brick-and-mortar stores. The organization has suffered from high customer churn caused by order cancellations, inventory overselling, untraceable deliveries, and slow refund issuance.

The management has commissioned an integrated Omnichannel Order Fulfilment Platform with an 8-week delivery deadline scheduled ahead of a major festival-sale event.

---

## 2. Resource and Availability Assumptions

1. **Initial Team Composition (Tasks 1–5):**
   - Exactly seven cross-functional engineers:
     1. Product Owner / Business Analysis Lead
     2. Frontend Engineer (Web & Mobile UI)
     3. Order API & Core Backend Engineer
     4. Inventory & Database Engineer
     5. Payments, Security & Compliance Engineer
     6. Quality Assurance (QA) & Test Automation Engineer
     7. DevOps & Infrastructure Engineer
   - No historical team velocity is established prior to Sprint 1.

2. **Nominal and Focused Working Capacity:**
   - 7 team members × 10 working days per 2-week sprint × 6 focused working hours per day = 420 nominal hours.
   - An explicit 20% operational reserve (84 hours) is set aside for sprint ceremonies, stakeholder clarification, unplanned defects, code reviews, and environment setup.
   - Net focused delivery capacity per sprint = **336 focused engineering hours**.
   - Story points are treated strictly as relative estimates of complexity, uncertainty, and effort, and are **never** treated as fixed conversion hours.

3. **Stakeholder Time Constraints:**
   - Warehouse operations and finance accounting stakeholders are available for exactly **90 minutes per week** for combined backlog refinement, requirement clarification, and increment review.
   - All clarification activities must be strictly prioritized and time-boxed within this window.

4. **Integration and Hardware Milestones:**
   - **Payment Gateway Sandbox:** External sandbox access is unavailable during weeks 1–3 and is scheduled to become accessible in **Week 4** (Sprint 2 / Sprint 3 boundary). Therefore, local mock adapters, test doubles, and idempotency contracts must be developed in Sprint 1.
   - **Barcode Scanner Hardware:** Physical test barcode scanners arrive in **Week 5** (Sprint 3). Warehouse scanning stories must rely on software-simulated string inputs prior to device arrival.

---

## 3. Reference Data and Privacy Assumptions

1. **Synthetic Data Mandate:**
   - In strict compliance with academic and professional privacy standards (and GDPR / DPDP guidelines), zero real customer data, live credit card credentials, or actual banking endpoints are used.
   - All catalogues, customer profiles, order numbers, payment tokens, and inventory movements are synthetic.
2. **Deterministic Rules vs Machine Learning:**
   - Low-stock alerts and threshold notifications are implemented via deterministic business rules (e.g., stock ≤ threshold).
   - Machine learning forecasting, automated demand predictions, and promotional AI are strictly excluded from the initial release and deferred to future roadmap phases.

---

## 4. Scaled Re-engineering Assumptions (Task 6)

1. **Changed Operating Context:**
   - The platform scope expands from 1 region to **3 regional warehouses** (North, South, and West), introducing regional tax jurisdictions, distinct shipping rate tables, and tiered refund approval thresholds.
   - A second 7-member cross-functional engineering team (Team B) joins the initiative.
   - The senior Payments and Security Engineer from Team A becomes abruptly unavailable for the remaining project duration.
   - The festival-sale delivery deadline (end of Week 8) is **fixed and non-negotiable**.

2. **Scaled Capacity Recalculation:**
   - Team A (6 remaining members): 6 × 10 × 6 = 360 nominal hours.
   - Team B (7 onboarding members): 7 × 10 × 6 × 0.60 (40% onboarding drag) = 252 focused-equivalent hours.
   - Total nominal capacity: 612 hours.
   - A 25% cross-team coordination, integration testing, and dependency reserve reduces effective focused capacity to **approximately 459 focused hours** (~1.37× original capacity, explicitly contradicting the naive Brooks' Law assumption of 2.0× throughput).

---

## 5. Simulation Transparency Notice
All stakeholder interview responses in Task 1, sprint event logs in Task 5, and scaled cross-team interaction logs in Task 6 represent structured, simulated planning data generated to validate delivery hypotheses. They are explicitly labelled as **SIMULATED** and are not presented as empirical corporate measurements.
