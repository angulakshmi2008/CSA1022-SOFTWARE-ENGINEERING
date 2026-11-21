# Screenshots To-Do List - Experiment 22

**Student Name:** Angulakshmi S  
**Register Number:** 192524402  
**Experiment:** Push and Pull Docker Images using Docker Hub  
**Course:** CSA10 - Software Engineering Laboratory  

This file outlines the exact live screenshots to capture when executing the Docker Hub push and pull lifecycle on your workstation or Play with Docker environment:

| Step # | Screenshot Description | Expected Window / View | File Destination |
|:---:|:---|:---|:---|
| **Step 2** | `docker build` command execution and `docker images` list showing local `static-web` image | Terminal / PowerShell / Bash | `screenshots/01_docker_build_and_images.png` |
| **Step 3** | Docker Hub repository creation page showing public repository `static-web` | Web Browser (`hub.docker.com/repositories`) | `screenshots/02_dockerhub_repo_created.png` |
| **Step 4** | `docker login` terminal showing `Login Succeeded` | Terminal / PowerShell / Bash | `screenshots/03_docker_login_succeeded.png` |
| **Step 5** | `docker tag` execution and `docker images` showing both `:1.0` and `:latest` tags sharing the same Image ID | Terminal / PowerShell / Bash | `screenshots/04_docker_tags_verified.png` |
| **Step 6** | `docker push` progress bars and Docker Hub Tags tab showing both `1.0` and `latest` pushed | Terminal & Browser (`hub.docker.com`) | `screenshots/05_docker_push_tags_web.png` |
| **Step 7** | `docker pull` execution on second machine / Play with Docker terminal | Terminal / Play with Docker instance | `screenshots/06_docker_pull_second_machine.png` |
| **Step 8** | `docker run -d -p 8080:80` and browser displaying the HTML website at `http://localhost:8080` | Web Browser showing "Hello from Docker Hub!" | `screenshots/07_website_running_pulled_image.png` |

> *Note: For verification in local academic environments without Docker Hub credentials or a second computer, Docker Desktop local daemon or [Play with Docker](https://labs.play-with-docker.com) provides instant virtual terminal instances.*
