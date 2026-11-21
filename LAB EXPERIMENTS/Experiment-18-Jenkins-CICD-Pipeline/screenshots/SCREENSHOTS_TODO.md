# Screenshots Required for Experiment 18: CI/CD Pipeline with Jenkins for a Containerized Application

**Student Name:** Angulakshmi S  
**Register Number:** 192524402  
**Course:** CSA10 - Software Engineering  

If running a live Jenkins server (`http://localhost:8080`) or Dockerized Jenkins instance, please capture the following screens and place them in this `screenshots/` directory:

| Figure No. | Step Reference | Description to Capture | Recommended File Name |
| :--- | :--- | :--- | :--- |
| **Figure 18.1** | Step 1 & 2: Jenkins Setup | Jenkins initial unlock screen and dashboard after installing Git and Pipeline plugins. | `figure_18_1_jenkins_dashboard.png` |
| **Figure 18.2** | Step 3: Application Repo | VS Code or GitHub showing `app.py`, `test_app.py`, `Dockerfile`, and `Jenkinsfile`. | `figure_18_2_repo_structure.png` |
| **Figure 18.3** | Step 4 & 5: Pipeline Job Config | Jenkins UI showing Pipeline job configuration (`Definition: Pipeline script from SCM`, Git repository URL, Script Path `Jenkinsfile`). | `figure_18_3_pipeline_config.png` |
| **Figure 18.4** | Step 6: Stage View | Jenkins Stage View showing all 4 stages (**Checkout**, **Build Image**, **Test**, **Deploy**) with green status ticks (**SUCCESS**). | `figure_18_4_stage_view_success.png` |
| **Figure 18.5** | Step 7: Application Browser | Browser visiting `http://localhost:5000` showing *"CI/CD with Jenkins - Build successful! Deployed by Angulakshmi S (192524402)"*. | `figure_18_5_deployed_app.png` |
| **Figure 18.6** | Step 8: Polling SCM Trigger | Jenkins build history showing automated build trigger (#102) from Git SCM polling. | `figure_18_6_scm_triggered_build.png` |

---
*Note: A complete real pipeline simulation log including automated `pytest` test runs is recorded in [`output/run_output.txt`](../output/run_output.txt).*
