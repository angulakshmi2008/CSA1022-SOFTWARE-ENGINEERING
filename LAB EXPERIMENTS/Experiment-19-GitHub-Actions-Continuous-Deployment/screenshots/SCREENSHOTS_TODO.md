# Screenshots Required for Experiment 19: Continuous Deployment of a Dockerized Application using GitHub Actions

**Student Name:** Angulakshmi S  
**Register Number:** 192524402  
**Course:** CSA10 - Software Engineering  

If running a live GitHub Actions repository with Docker Hub and Cloud deployment, please capture the following screens and place them in this `screenshots/` directory:

| Figure No. | Step Reference | Description to Capture | Recommended File Name |
| :--- | :--- | :--- | :--- |
| **Figure 19.1** | Step 1: Application Repo | GitHub repository code view showing `app.py`, `Dockerfile`, and workflow file. | `figure_19_1_repo_files.png` |
| **Figure 19.2** | Step 2 & 3: Repository Secrets | GitHub **Settings $\rightarrow$ Secrets and variables $\rightarrow$ Actions** showing `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, and cloud deployment secrets. | `figure_19_2_actions_secrets.png` |
| **Figure 19.3** | Step 5: Workflow YAML | GitHub editor or VS Code displaying the `.github/workflows/cd.yml` specification. | `figure_19_3_cd_workflow_yaml.png` |
| **Figure 19.4** | Step 6: Successful Actions Run | GitHub **Actions** tab showing the run *"CD - Build, Push and Deploy"* with all job steps marked with green checkmarks (**SUCCESS**). | `figure_19_4_actions_run_success.png` |
| **Figure 19.5** | Step 7: Docker Hub Tags | Docker Hub repository `gha-docker-cd` showing tags `latest` and commit SHA pushed by GitHub Actions. | `figure_19_5_dockerhub_tags.png` |
| **Figure 19.6** | Step 7: Deployed App in Browser | Browser visiting the cloud deployment public URL displaying *"Version 1.0 - Deployed automatically with GitHub Actions"*. | `figure_19_6_deployed_app_v1.png` |
| **Figure 19.7** | Step 8: Triggered Re-run (Version 2) | Actions tab showing automated triggering and deployment of *"Version 2"* upon code push. | `figure_19_7_redeploy_v2.png` |

---
*Note: A complete local application verification and workflow schema validation log is available in [`output/run_output.txt`](../output/run_output.txt).*
