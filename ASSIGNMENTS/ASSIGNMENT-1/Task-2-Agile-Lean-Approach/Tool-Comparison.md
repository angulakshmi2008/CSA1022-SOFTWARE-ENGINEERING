# Task 2: Project Management Tool Comparison and Justification

## 1. Tool Evaluation Objectives
Selecting an appropriate project management tool is essential to enforce the tailored Scrum-with-Lean delivery model. The platform must support epic hierarchies, user story backlog refinement, custom workflow state transitions, WIP limits, burndown/burnup velocity tracking, and exportability.

Two leading industry tools were evaluated:
1. **Atlassian Jira Software (Cloud)**
2. **GitHub Projects (Issues & Projects v2)**

---

## 2. In-Depth Comparative Evaluation

| Evaluation Criteria | Atlassian Jira Software | GitHub Projects (v2) | Comparative Synthesis & Fit |
|---|---|---|---|
| **Backlog & Epic Planning** | Native multi-tier hierarchy (Epic → Story/Task → Sub-task). Built-in backlog view supporting drag-and-drop prioritization, estimation in Story Points, and multi-sprint planning containers. | Flat issue structure; epics are represented via issue tracking lists, markdown task lists, or custom project fields. Sprint iterations can be created via Iteration fields. | **Jira is superior** for formal Agile sprint planning and backlog grooming, providing dedicated views for backlog refinement vs active sprint execution. |
| **Workflow & Status Customization** | Advanced workflow designer supporting custom states (`Ready`, `In Progress`, `Review`, `Test`, `Blocked`, `Done`), strict transition conditions, validators, post-functions, and column-based WIP limits. | Project board columns support custom statuses, but lacks native transition validation guards (e.g., preventing a move to `Done` without passing test run evidence). | **Jira provides stronger governance** by enforcing required fields and transition rules, directly aligning with our Definition of Done. |
| **Lean Flow & WIP Limits** | Built-in column WIP constraints with visual alerts when limits are exceeded. Dedicated Kanban and Scrum board modes. | WIP limits can be configured on column headers in table/board views, with visual indicator flags. | Both tools support column WIP limits; Jira integrates limits into cumulative flow reporting. |
| **Traceability & Engineering Linkage** | Integrates with git repositories via smart commits (e.g., `FIQP-102 #close`). Links issues to commits, branches, and pull requests. Requires plugin configuration. | Deep, native repository integration. Issues, pull requests, commit hashes, code reviews, and CI/CD GitHub Actions workflows share a single interface. | **GitHub Projects is superior** for direct developer-centric code traceability, while Jira is superior for cross-functional business traceability. |
| **Reporting & Flow Metrics** | Out-of-the-box Agile reporting: Sprint Burndown, Velocity Charts, Cumulative Flow Diagrams (CFD), Cycle Time / Control Charts. | Basic project insights and charts. Advanced flow metrics (cycle time, CFD) require custom GraphQL queries or external third-party actions. | **Jira is significantly stronger** for academic and management reporting, providing standard burndown and lead-time analytics. |
| **Accessibility & Cost Model** | Free tier covers up to 10 users with standard Agile features (sufficient for our 7-member team). Paid tiers required for advanced cross-project roadmaps and SLA rules. | Free for public and private repositories under standard GitHub accounts, offering unlimited collaborators on basic projects. | Both tools offer viable free tiers for a 7-member team. Jira carries zero monetary cost for small teams under 10 members. |

---

## 3. Justified Tool Selection: Jira Software

**Selected Tool:** **Atlassian Jira Software (with GitHub Projects as an interoperable technical backup).**

### Justification Rationale:
1. **Academic and Faculty Alignment:** The CSA10 assignment specification explicitly highlights Jira as the primary industry-standard benchmark for CO1 evaluation.
2. **Rigid Workflow & WIP Enforcement:** Jira allows configuring the exact 6-state development workflow (`Ready` → `In Progress` → `Review` → `Test` → `Blocked` → `Done`) and setting distinct column WIP limits (4 on Dev, 2 on Review, 2 on Test).
3. **Sprint & Velocity Analytics:** Jira provides native sprint management, burndown charts, and velocity tracking necessary to evaluate Sprint 1 commitments against actual completions.

---

## 4. Identified Limitations and Mitigation Strategies

| Potential Tool Limitation | Practical Operational Impact | Proactive Mitigation Strategy |
|---|---|---|
| **Account Tier & Permissions Restrictions** | Standard free tiers may restrict advanced custom field validators, automated transition scripts, or enterprise audit logs. | Provide a fully standardized, import-ready CSV export ([Backlog-Import.csv](file:///c:/Users/ANGULAKSHMI%20SUBBURAJ/Downloads/ASSIGNMENT-1/Task-3-Product-Backlog/Backlog-Import.csv)) that can be imported into any Jira Cloud instance, Server instance, or spreadsheet without data loss. |
| **Separation of Operational vs Development States** | Risk of confusion between software development states (e.g., `Test`) and business order states (e.g., `Dispatched`). | Enforce strict naming conventions: Issue tickets describe software tasks; acceptance criteria and domain models strictly encapsulate order lifecycle states (`CREATED`, `RESERVED`, `PAID`, `PICKING`, `DISPATCHED`, `DELIVERED`, `REFUNDED`). |
| **Offline or Sandboxed Execution Constraints** | External cloud access may be restricted during sandbox examination or local grading sessions. | All backlog items, sprint plans, workflow configurations, and simulation event logs are mirrored as markdown tables and CSV artifacts directly within the version-controlled repository. |
