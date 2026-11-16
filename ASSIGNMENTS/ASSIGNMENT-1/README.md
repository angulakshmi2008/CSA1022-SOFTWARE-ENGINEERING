# Omnichannel Order Fulfilment Platform – Agile Delivery Strategy

## Course: CSA10 – Software Engineering | Assignment 1 (Set B)
**Institution:** SIMATS Engineering, Department of Computer Science and Engineering  
**Target Course Outcome:** CO1 (Apply agile methodologies and project management techniques such as scale and lean to effectively manage software projects using industry-standard tools like Jira)  
**Cognitive Levels:** Bloom's Taxonomy Level 5 (Evaluate) & Level 6 (Create)  
**Student Name:** ANGULAKSHMI SUBBURAJ (Reg. No: 192524402)  
**Submission Date:** November 14, 2026  

---

## 1. Executive Summary and Problem Scenario

A prominent multi-channel retailer operates an e-commerce website, a mobile shopping application, and 12 physical brick-and-mortar stores. The business has suffered from high customer churn, order cancellation spikes, and audit vulnerabilities caused by unsynchronized stock counts, untraceable parcels, and uncontrolled refund approvals.

This repository contains the complete, industry-standard solution for **Software Engineering Assignment 1**:
1. **Agile Delivery Strategy:** A disciplined delivery model combining **Scrum with Lean Flow Controls** (Work-in-Progress limits: Dev 4, Review 2, Test 2) tailored for an 8-week release window across four 2-week sprints.
2. **Prioritized Backlog & Release Plan:** 15 refined user stories across 4 functional epics with explicit positive/negative acceptance criteria, MoSCoW prioritization, and a capacity model of 420 nominal / 336 focused engineering hours per sprint.
3. **Sprint 1 Simulation:** A 16-step simulated event log validating a pre-simulation bottleneck hypothesis (single QA test queue & stock reservation race conditions), delivering 11 of 16 planned points (68.8% reliability) and driving empirical improvements for Sprint 2.
4. **Scaled Agile Redesign (Task 6):** A comprehensive architectural redesign under a 5-factor Day-4 organizational disruption (2 additional regional warehouses, a second 7-member team, departure of the lead payments engineer, regional tax/shipping rules, and a fixed festival deadline). Effective capacity is recalculated via **Brooks' Law** (459 net focused hours, ~1.37× scaling, debunking the naive 2.0× assumption), introducing decoupled policy tables, contract-first API stubs, an emergency payments pairing handover protocol, and an active Integration Owner role.
5. **Individual Technical Reflection (Task 7):** A rigorous first-person reflection analyzing key project decisions, empirical pivots, residual risks, ethical duties (privacy, accessibility, sustainable workload), and future empirical investigations.
6. **Functional Software Prototype (`Platform/`):** A demonstrable Python/SQLite backend prototype with 100% automated test coverage asserting all five Measurable Delivery Criteria (MSC-01 to MSC-05).

---

## 2. Professional Repository Structure

```text
Software-Engineering-Assignment-1/
│
├── README.md                                  # Master project overview and quickstart guide
├── convert_pdf.ps1                            # Automation script
│
├── documentation/                             # Formal academic documentation and reports
│   ├── Final-Assignment-Report.docx           # Publication-grade academic report (Times New Roman, 1.5 spacing, 14pt/12pt)
│   ├── Final-Assignment-Report.pdf            # Exported PDF report
│   ├── Requirements-Traceability.md           # Master RTM mapping requirements to tasks, rubrics, and code
│   ├── Project-Assumptions.md                 # Formal resource, capacity, stakeholder, and constraint baselines
│   ├── References.md                          # IEEE-formatted numbered reference citations
│   └── Evidence/                              # Empirical execution evidence and board artifacts
│       ├── Test-Execution-Report.txt          # Console log: 13/13 automated test suites passing 100%
│       ├── Demo-Execution-Log.txt             # Interactive end-to-end CLI demonstration log
│       ├── Jira-Backlog-Export.csv            # Import-ready issue catalogue for Atlassian Jira Software
│       ├── Jira-Sprint-Plan.md                # Board status workflow, sprint containers, and WIP policies
│       ├── Sprint-1-Simulation-Trace.csv      # 16-step simulated event log for Sprint 1
│       └── Sprint-2-Scaled-Simulation-Trace.csv # 6-step simulated event log for Scaled Sprint 2
│
├── Task-1-Problem-Investigation/              # Problem investigation, scope, and criteria (5 Marks)
│   ├── README.md                              # Task overview and key takeaways
│   ├── Investigation-Questions.md             # 5 targeted investigation questions probing system bottlenecks
│   ├── Stakeholder-Analysis.md                # Stakeholder matrix & simulated interview findings across 6 roles
│   └── Delivery-Outcomes.md                   # Product goal, scope boundaries, MSC-01 to MSC-05, feasibility
│
├── Task-2-Agile-Lean-Approach/                # Delivery framework & operating model design (6 Marks)
│   ├── README.md                              # Task overview and key takeaways
│   ├── Framework-Comparison.md                # Scrum + Lean vs Kanban comparative analysis across 7 axes
│   ├── Team-Operating-Model.md                # 7 cross-functional roles, RACI matrix, 90-min stakeholder model, WIP
│   └── Tool-Comparison.md                     # Jira Software vs GitHub Projects technical evaluation
│
├── Task-3-Product-Backlog/                    # Prioritized backlog in Jira (8 Marks)
│   ├── README.md                              # Backlog overview and metrics
│   ├── Epics.md                               # Epics E1 to E4 (In-Scope) and E5 (Deferred Roadmap)
│   ├── User-Stories.md                        # 15 refined user stories with MoSCoW, points, roles, dependencies
│   ├── Acceptance-Criteria.md                 # Positive and negative boundary test cases (Gherkin format)
│   ├── Definition-of-Ready.md                 # 6-point gating checklist governing sprint commitment
│   ├── Definition-of-Done.md                  # 8-point quality contract & analysis of 2 stakeholder conflicts
│   └── Backlog-Import.csv                     # Import-ready CSV formatted for Jira / GitHub Projects
│
├── Task-4-Release-Planning/                   # Capacity-based 4-sprint plan & workflow (7 Marks)
│   ├── README.md                              # Release planning summary
│   ├── Capacity-Planning.md                   # 420h nominal / 336h focused capacity formula & point decoupling
│   ├── Four-Sprint-Plan.md                    # 4-sprint roadmap, story slicing (S03/S09), Wk 4 & Wk 5 dependencies
│   └── Workflow-Configuration.md              # 6-state dev workflow vs 10-state order lifecycle, WIP, blockers
│
├── Task-5-Sprint-Simulation/                  # Delivery simulation & evidence-based adaptation (7 Marks)
│   ├── README.md                              # Simulation summary and metrics
│   ├── Sprint-1-Event-Log.csv                 # 16-step simulated event log (all entries labelled SIMULATED)
│   ├── Sprint-Metrics.md                      # Bottleneck analysis: 68.8% velocity, 2.0 story-days blocked, 67% rework
│   └── Improvement-Actions.md                 # 5 concrete Sprint 2 corrective actions (capping scope, daily pairing)
│
├── Task-6-Scaled-Agile-Redesign/              # Scaled redesign under changed conditions (12 Marks)
│   ├── README.md                              # Redesign summary and outcomes
│   ├── Impact-Analysis.md                     # Component A: Diagnosis of 5 organizational disruptions & Brooks' Law
│   ├── Revised-Strategy.md                    # Components B & C: Redesign objectives, 459h capacity, scaled model
│   ├── Team-Responsibilities.md               # Team A vs Team B boundaries & payments handover protocol
│   ├── Additional-Simulation.csv              # Component D: 6 simulated cross-team disruption events
│   └── Performance-Comparison.md              # Components D & E: Comparative metrics table & strategic defense
│
├── Task-7-Technical-Reflection/               # Individual technical reflection (5 Marks)
│   ├── README.md                              # Pedagogical summary
│   └── Individual-Reflection.md               # First-person reflection on decisions, evidence, vulnerabilities, ethics
│
└── Platform/                                  # Fully functional software prototype & test harness
    ├── src/                                   # Domain models, services, RBAC, state machine, policy engine
    ├── tests/                                 # Automated test suites for lifecycle, concurrency, idempotency, RBAC
    ├── test-data/                             # Synthetic product catalog and multi-region rule tables
    ├── scripts/                               # Interactive CLI demo and test runner scripts
    └── README.md                              # Prototype architecture and execution guide
```

---

## 3. Measurable Delivery Criteria (MSC-01 to MSC-05) Verification

The software prototype directly executes and validates the five acceptance criteria established in Task 1:

| Criterion ID | Target Acceptance Threshold | Automated Test Suite | Test Result |
|---|---|---|---|
| **MSC-01** | Full 10-state lifecycle (`CREATED` → `RESERVED` → `PAID` → `PICKING` → `PICKED` → `DISPATCHED` → `DELIVERED` → `RETURN_REQUESTED` → `REFUND_PENDING` → `REFUNDED`) with immutable audit logging. | `Platform/tests/test_order_lifecycle.py` | **PASS (100%)** |
| **MSC-02** | 100 concurrent checkout requests for a 10-unit SKU yield exactly 10 reservations, 90 clean out-of-stock rejections, and zero negative stock. | `Platform/tests/test_concurrency_stock.py` | **PASS (100%)** |
| **MSC-03** | 10 consecutive payment requests with identical idempotency keys return the same payment intent with zero duplicate charges. | `Platform/tests/test_payment_idempotency.py` | **PASS (100%)** |
| **MSC-04** | Role-based authorization rejects unauthorized refund approvals by Support Agents or Pickers with HTTP 403; only Finance Reviewer can approve. | `Platform/tests/test_security_roles.py` | **PASS (100%)** |
| **MSC-05** | Clean checkout builds and passes 100% of unit/integration tests using a single standard command. | `Platform/scripts/run_all_tests.py` | **PASS (100%)** |

---

## 4. How to Run the Platform Prototype

### 4.1 Prerequisites
- Python 3.10+ (Standard library only; zero external packages required).

### 4.2 Run the Automated Test Suite (13 Tests, 100% Pass)
```bash
python Platform/scripts/run_all_tests.py
```
*Expected Output:*
```text
===========================================================================
  TEST EXECUTION SUMMARY:
  Tests Run:     13
  Passed:        13
  Failures:      0
  Errors:        0
  Success Rate:  100.0%
===========================================================================
  >>> ALL ASSIGNMENT ACCEPTANCE TESTS PASSED (100% SUCCESS) <<<
```

### 4.3 Run the Interactive End-to-End Walkthrough
```bash
python Platform/scripts/run_demo.py
```
*Demonstrates:*
1. Database seeding with synthetic catalogue and regional rules.
2. User authentication for Customer, Picker, Support Agent, and Finance Reviewer.
3. Order creation and atomic stock reservation with 15-minute countdown TTL.
4. Idempotent payment processing and duplicate replay rejection.
5. Warehouse pick list generation filtered by paid orders.
6. Barcode scanning confirmation.
7. Order lifecycle transitions to `DELIVERED`.
8. Public milestone tracking (WCAG screen-reader accessible).
9. Customer return request submission within the 14-day policy window.
10. Security RBAC guard blocking unauthorized support agent refund attempts.
11. Finance Reviewer refund approval with monetary limits.
12. Inspection of the immutable audit journal.

---

## 5. Traceability and Assessment Verification Guide

For faculty evaluation and oral defense:
- **Requirements Traceability:** Refer to [documentation/Requirements-Traceability.md](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/documentation/Requirements-Traceability.md) for a comprehensive line-by-line mapping of the syllabus rubrics to project artifacts.
- **Project Assumptions:** Refer to [documentation/Project-Assumptions.md](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/documentation/Project-Assumptions.md) for detailed resource, capacity, and constraint specifications.
- **Formal Academic Report:** Access [documentation/Final-Assignment-Report.docx](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/documentation/Final-Assignment-Report.docx) formatted strictly in Times New Roman, 1.5 line spacing, 14pt headings, 12pt body text, justified alignment, complete with cover page, IEEE citations, and appendices.
