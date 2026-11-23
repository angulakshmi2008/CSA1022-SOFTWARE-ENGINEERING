# SIMATS Engineering
## Department of Computer Science and Engineering
### Course: CSA1022 / CSA10 – Software Engineering
### Assessment: Model Practical Examination – Set 2

---

## 📌 Model Practical Overview

This directory contains the complete, verified, and production-grade deliverables for all **four experiments** of the **Software Engineering Model Practical (Set 2)**.

All code implementations, test suites, Docker container configurations, YAML files, UML models, mathematical proofs, and analytical examination answers are fully completed and verified.

---

## 📋 Experiments Summary Table

| Experiment No. | Experiment Title | Course Outcomes | Marks | Key Deliverables | Status |
| :---: | :--- | :---: | :---: | :--- | :---: |
| **Experiment 01** | [Feature Branch & Pull Request for Signup](./Experiment-01-Feature-Branch-Signup) | CO3, CO1 | 25M (15M + 10M) | `signup.py`, `test_signup.py`, Git branches (`main`, `feature-signup`), PR merge simulation, merge conflict resolution guide & simulator | **VERIFIED** (13/13 Tests Passed) |
| **Experiment 02** | [Cyclomatic Complexity of Flow Graph](./Experiment-02-Cyclomatic-Complexity) | CO4, CO1 | 25M (15M + 10M) | Formula 1 & 2 derivations, verified CFG ($E=22, N=17, P=6, V(G)=7$), `flow_graph.png`, `flow_graph.drawio`, `flow_graph.mmd` | **VERIFIED** (Math & CFG Verified) |
| **Experiment 03** | [E-Learning Platform Use Case Diagram](./Experiment-03-Elearning-Use-Case) | CO2, CO1 | 25M (15M + 10M) | UML 2.5 Use Case Diagram, 4 Actors, System Boundary, `<<include>>` and `<<extend>>` relations, `use_case_diagram.png`, `.drawio`, `.mmd` | **VERIFIED** (UML 2.5 Standard) |
| **Experiment 04** | [Containerize Node.js Express Notes App](./Experiment-04-Docker-Notes-Application) | CO5, CO1 | 25M (15M + 10M) | Express REST API (`GET /`, `GET /notes`, `POST /notes`), `Dockerfile`, `.dockerignore`, `docker-compose.yml`, test suite, Docker Hub preparation | **VERIFIED** (16/16 Tests Passed) |

---

## 📂 Directory Structure

```text
MODEL LAB/
│
├── README.md                                    # Master Model Lab Index (this file)
│
├── Experiment-01-Feature-Branch-Signup/         # Experiment 1
│   ├── signup.py                                # Signup credential validation function & CLI
│   ├── test_signup.py                           # Automated unit test suite (13 test cases)
│   ├── git-workflow.md                          # Git feature branch & GitHub PR guide
│   ├── merge-conflict-demo.md                   # Merge conflict detection & resolution guide
│   ├── demo_conflict.py                         # Standalone executable conflict simulator
│   ├── git_workflow_graph.png                   # Visual diagram of PR & branch workflow
│   ├── test_results.png                         # Visual card of unit test results
│   ├── analysis.md                              # Part B typed exam answer (10 marks)
│   └── README.md                                # Experiment documentation & viva guide
│
├── Experiment-02-Cyclomatic-Complexity/         # Experiment 2
│   ├── calculations.md                          # Derivations: E-N+2P=7, Pred+1=7, Basis paths
│   ├── verify_graph.py                          # Python graph validator & diagram generator
│   ├── flow_graph.png                           # Rendered Control Flow Graph (17 nodes, 22 edges)
│   ├── flow_graph.drawio                        # Editable XML Draw.io source diagram
│   ├── flow_graph.mmd                           # Mermaid control flow graph source
│   ├── analysis.md                              # Part B typed exam answer (10 marks)
│   └── README.md                                # Experiment documentation & viva guide
│
├── Experiment-03-Elearning-Use-Case/            # Experiment 3
│   ├── actors_and_use_cases.md                  # Actor profiles, use case specs & relationships
│   ├── generate_diagram.py                      # Diagram renderer script
│   ├── use_case_diagram.png                     # Exported UML Use Case Diagram (300 DPI)
│   ├── use_case_diagram.drawio                  # Editable XML Draw.io diagram
│   ├── use_case_diagram.mmd                     # Mermaid diagram source
│   ├── analysis.md                              # Part B typed exam answer (10 marks)
│   └── README.md                                # Experiment documentation & viva guide
│
└── Experiment-04-Docker-Notes-Application/      # Experiment 4
    ├── package.json                             # Node.js project manifest & dependencies
    ├── package-lock.json                        # Dependency lockfile
    ├── server.js                                # Express REST API with input validation
    ├── test_api.js                              # Automated API test suite (16 assertions)
    ├── Dockerfile                               # Alpine Linux production containerfile
    ├── .dockerignore                            # Build context exclusions (node_modules, logs)
    ├── docker-compose.yml                       # Compose file for local multi-container launch
    ├── docker-commands.md                       # Build, run, exec, test & Docker Hub guide
    ├── docker_architecture.png                  # Architectural container diagram
    ├── api_test_results.png                     # Visual card of API test results
    ├── analysis.md                              # Part B typed exam answer (10 marks)
    └── README.md                                # Experiment documentation & viva guide
```

---

## 🚀 Quick Execution Guide

### Experiment 01: Signup Feature & Git PR
```bash
cd "MODEL LAB/Experiment-01-Feature-Branch-Signup"
python signup.py                        # Interactive test runner
python -m unittest test_signup.py -v    # Run unit tests (13/13 PASS)
python demo_conflict.py                 # Run safe conflict detection & resolution demo
```

### Experiment 02: Flow Graph & Cyclomatic Complexity
```bash
cd "MODEL LAB/Experiment-02-Cyclomatic-Complexity"
python verify_graph.py                  # Verify E=22, N=17, P=6, V(G)=7 and regenerate flow_graph.png
```

### Experiment 03: E-Learning UML Use Case Modeling
```bash
cd "MODEL LAB/Experiment-03-Elearning-Use-Case"
python generate_diagram.py              # Render high-resolution use_case_diagram.png
```

### Experiment 04: Docker Notes Application
```bash
cd "MODEL LAB/Experiment-04-Docker-Notes-Application"
npm install                             # Install dependencies
node test_api.js                        # Run automated API test suite (16/16 PASS)
node server.js                          # Start Express server on port 3000
```

---

## 📊 Course Outcomes Mapping

- **CO1 (Agile & Software Management):** Demonstrated across all 4 experiments through modular design, git branching, test-driven validation, and clear documentation.
- **CO2 (Requirements Analysis & UML Modeling):** Demonstrated in **Experiment 3** through actor classification, system boundary modeling, and `<<include>>`/`<<extend>>` relationships.
- **CO3 (Version Control Systems):** Demonstrated in **Experiment 1** through Git feature branching, pull request code review simulation, and three-way merge conflict resolution.
- **CO4 (Software Testing Strategies & Metrics):** Demonstrated in **Experiment 2** through McCabe's Cyclomatic Complexity, basis path testing, and risk level assessment.
- **CO5 (Modern Cloud Technologies & Containers):** Demonstrated in **Experiment 4** through Node.js Express REST API containerization, Alpine Linux multi-stage Dockerfiles, and storage lifecycle management.
