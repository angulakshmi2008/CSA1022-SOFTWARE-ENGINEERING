# Screenshots Required for Experiment 21: Containerizing a Python Flask To-Do Application using Docker

**Student Name:** Angulakshmi S  
**Register Number:** 192524402  
**Course:** CSA10 - Software Engineering  

If running Docker Desktop on your system, please capture the following screens and place them in this `screenshots/` directory:

| Figure No. | Step Reference | Description to Capture | Recommended File Name |
| :--- | :--- | :--- | :--- |
| **Figure 21.1** | Step 1: App & Template | VS Code showing `app/app.py` and `app/templates/index.html`. | `figure_21_1_code_structure.png` |
| **Figure 21.2** | Step 2: Dockerfile | VS Code showing `Dockerfile` and `.dockerignore`. | `figure_21_2_dockerfile.png` |
| **Figure 21.3** | Step 3: Docker Build | Terminal showing `docker build -t todo-app:1.0 .` and `docker images todo-app`. | `figure_21_3_docker_build.png` |
| **Figure 21.4** | Step 4: Run Container | Terminal showing `docker run -d --name todo -p 5000:5000 todo-app:1.0` and `docker ps`. | `figure_21_4_container_running.png` |
| **Figure 21.5** | Step 4 & 5: To-Do App Web UI | Browser visiting `http://localhost:5000` showing task input, added tasks, completed strike-throughs, and student credentials (Angulakshmi S, 192524402). | `figure_21_5_todo_web_ui.png` |
| **Figure 21.6** | Step 5: Container Exec & Logs | Terminal showing `curl http://localhost:5000/api/tasks`, `docker exec -it todo ...`, and `docker logs todo`. | `figure_21_6_exec_and_logs.png` |
| **Figure 21.7** | Step 6: Docker Hub Push | Browser on `hub.docker.com` showing repository `todo-app` with tag `1.0` published. | `figure_21_7_dockerhub_repo.png` |

---
*Note: A complete verified local application run log is saved in [`output/run_output.txt`](../output/run_output.txt).*
