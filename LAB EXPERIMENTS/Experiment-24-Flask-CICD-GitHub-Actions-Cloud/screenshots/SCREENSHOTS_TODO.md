# Screenshots To-Do List - Experiment 24

**Student Name:** Angulakshmi S  
**Register Number:** 192524402  
**Experiment:** CI/CD Pipeline for a Flask Application using GitHub Actions with Cloud Deployment  
**Course:** CSA10 - Software Engineering Laboratory  

This file outlines the live screenshots to capture from GitHub and your cloud dashboard:

| Step # | Screenshot Description | Expected Window / View | File Destination |
|:---:|:---|:---|:---|
| **Step 4** | GitHub Actions Pipeline Run Graph showing all three jobs (`test`, `build-and-push`, `deploy`) completed with green checkmarks | GitHub repository -> **Actions** tab -> Latest Workflow Run | `screenshots/01_workflow_graph_all_success.png` |
| **Step 5** | Pytest execution step inside the `test` job logs showing `2 passed` | GitHub Actions -> `test` job log details | `screenshots/02_actions_pytest_log.png` |
| **Step 5** | Docker Hub repository showing the pushed image `<dockerhub-username>/flask-cicd:latest` | Web Browser (`hub.docker.com/repositories`) | `screenshots/03_dockerhub_pushed_image.png` |
| **Step 5** | Live Deployed Application in Web Browser showing JSON output `{"message":"Flask CI/CD with GitHub Actions","status":"running"}` | Web Browser visiting `https://<app-name>.onrender.com` or Heroku URL | `screenshots/04_cloud_deployed_app.png` |
| **Step 6** | Pipeline Quality Gate Failure demonstration (when a broken test is pushed, e.g. `a - b`) showing failed `test` job and skipped `build-and-push` / `deploy` jobs | GitHub Actions tab -> Failed workflow run | `screenshots/05_actions_failed_test_gate.png` |

> *Note on Safety Rule 9: GitHub Actions workflows are executed by GitHub when located in `.github/workflows/` at repository root. Per strict laboratory isolation rules, the workflow file is preserved in `workflows/ci-cd.yml` within this experiment folder to prevent affecting other assignments.*
