# Task 2: Comparative Evaluation of Tool Arrangements for Requirements, Documentation, and UML Modeling

In compliance with the official CSA10 specification, this section formally evaluates two comprehensive tool arrangements across six software engineering dimensions: **Traceability**, **Collaboration**, **Version History**, **Diagram Support**, **Accessibility**, and **Cost / Operational Overhead**.

---

## 1. Tool Arrangement Comparison Matrix

| Evaluation Dimension | Arrangement A: Jira + Confluence + Dedicated UML Plugin (Atlassian Suite) | Arrangement B: GitHub Repository + GitHub Issues/Projects + Markdown + PlantUML (Chosen Architecture) |
| :--- | :--- | :--- |
| **Traceability** | **High:** Native bidirectional linking between Jira issues (`FR-01`), Confluence requirements pages, and Git commits via Jira Git integrations. However, requires multiple API webhooks and integration maintenance. | **Very High:** Native, single-repository traceability. Requirement IDs (`FR01`, `NFR01`) are directly embedded in Markdown specs, commit messages (`feat(FR03): ...`), pull requests, and automated test names (`test_t1_stock_contention_fr03`). Zero synchronization drift. |
| **Collaboration** | **Very High:** Real-time multi-user concurrent editing in Confluence; rich commenting, inline mentions, role-based workflows, and customizable Kanban boards in Jira. Highly familiar to enterprise project managers. | **High:** GitHub Pull Requests support structured code review, threaded discussions, code owner reviews, and GitHub Projects Kanban boards. Requires team comfort with Git branching workflows. |
| **Version History** | **Moderate:** Confluence maintains page revision history, but page versions are decoupled from the code release cycle. Rolling back an application version does not automatically roll back requirements documentation. | **Absolute (Git-Backed):** Every change to requirements, architecture, diagrams, and code is committed atomically in the same Git tree. Documentation history is cryptographically versioned and branched alongside the application code. |
| **Diagram Support** | **Good:** Visual GUI editors (Draw.io, Lucidchart, Gliffy) provide rich drag-and-drop modeling. However, diagrams are stored as proprietary binary/XML blobs that cannot be diffed cleanly in code reviews. | **Excellent (Code-as-Diagram):** Plaintext PlantUML and Mermaid source files (`.puml`, `.mmd`) reside alongside code. Architectural changes produce clean visual line-by-line diffs during Pull Requests and render in CI pipelines. |
| **Accessibility** | **High:** Standard web-browser accessibility; comprehensive enterprise Single Sign-On (SSO) integration, WCAG compliance, and mobile responsive portals. | **High:** Web-accessible interface via GitHub.com. Markdown rendered natively in any browser or local IDE (VS Code) with screen-reader friendly structured headings and tables. |
| **Cost & Overhead** | **High:** Tiered per-user monthly SaaS licensing (Jira + Confluence + diagram plugins). Substantial administrative overhead configuring user directories, issue types, workflows, and permissions. | **Low / Minimal:** Included in standard GitHub repository tiers (free for public/academic repositories, low flat rate for private organizations). Zero external infrastructure or synchronization servers required. |

---

## 2. Selection Rationale and Justification

### Selected Arrangement: Arrangement B (GitHub-First Repository Architecture)
For this omnichannel order fulfilment platform, **Arrangement B (GitHub Repository + GitHub Issues + Markdown + PlantUML)** is selected as the primary engineering environment for the following reasoned justifications:
1. **Zero Documentation-Code Drift:** In complex distributed architectures, decoupling requirements documentation (e.g., in Confluence) from source code repositories results in "documentation drift," where code evolves while wiki specifications become obsolete. By maintaining requirements (`docs/task-2-requirements/`), UML source (`docs/task-3-uml-traceability/diagrams/`), ADRs (`docs/task-4-architecture/adr/`), and test code (`tests/`) in the exact same version-controlled repository, any requirement change is committed atomically with its corresponding code update and test vector.
2. **Reviewable Diagram Diffs:** Using PlantUML/Mermaid (`.puml`) allows software architects to review modifications to state machines, sequence diagrams, and class models using standard Git diffs. Graphical GUI tools (Visio, Draw.io) generate binary files that cannot be meaningfully peer-reviewed in pull requests.
3. **Reproducibility and Academic Independence:** Arrangement B eliminates external SaaS subscription barriers, ensuring that any faculty evaluator or peer reviewer can clone the repository and inspect the complete lifecycle (investigation, specification, models, ADRs, test results) locally without requiring Jira/Confluence credentials.

---

## 3. Acknowledged Limitations of the Chosen Arrangement and Mitigation Strategies

While Arrangement B offers unmatched technical consistency, it exhibits the following real-world limitations, which are addressed through deliberate mitigations:

| Identified Limitation | Real-World Impact | Engineering Mitigation Applied |
| :--- | :--- | :--- |
| **Non-Technical Accessibility Barrier** | Business stakeholders (executives, finance reviewers, warehouse leads) may not be comfortable using Git, Markdown syntax, or terminal commands. | Export clean, professionally formatted Microsoft Word (`.docx`) and standalone HTML reports from the authoritative Markdown source for non-technical review. |
| **Lack of Automated Jira Workflow Enforcement** | Standard GitHub issues lack complex state-transition constraints (e.g., prohibiting an issue from moving to 'Done' without a formal QA sign-off). | Enforce quality gates via GitHub Actions CI: Pull requests cannot be merged to `main` unless 100% of automated pytest verification suites pass. |
| **Diagram Rendering Dependency** | Raw PlantUML (`.puml`) files require a Java/Graphviz runtime or remote PlantUML server to render into graphical PNG/SVG images. | Provide both raw `.puml` source files for versioning and pre-rendered vector SVG / high-resolution PNG images embedded directly in the documentation artifacts. |
| **Cross-System Synchronization Overhead** | In an enterprise already invested in Atlassian, maintaining GitHub Markdown alongside Jira tickets requires manual synchronization. | Generate import-ready JSON/CSV issue records formatted for Jira, allowing instantaneous one-click import into enterprise Jira boards if enterprise scaling demands it. |
