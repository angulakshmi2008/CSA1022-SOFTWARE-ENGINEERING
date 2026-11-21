# Screenshots Required for Experiment 16: Static Website Containerized and Served with Docker and Nginx

**Student Name:** Angulakshmi S  
**Register Number:** 192524402  
**Course:** CSA10 - Software Engineering  

If running Docker Desktop on your personal system, please capture the following screens and place them in this `screenshots/` directory:

| Figure No. | Step Reference | Description to Capture | Recommended File Name |
| :--- | :--- | :--- | :--- |
| **Figure 16.1** | Step 1: Verify Docker | Terminal / PowerShell showing `docker --version` and `docker run hello-world` with *"Hello from Docker!"* output. | `figure_16_1_docker_verify.png` |
| **Figure 16.2** | Step 4: Dockerfile | Visual Studio Code editor displaying the completed `Dockerfile` with instructions (`FROM nginx:alpine`, `COPY`, `EXPOSE 80`, `CMD`). | `figure_16_2_dockerfile.png` |
| **Figure 16.3** | Step 5: Build Image | Terminal showing `docker build -t static-site:1.0 .` build steps and `docker images` listing `static-site:1.0`. | `figure_16_3_docker_build.png` |
| **Figure 16.4** | Step 6: Run Container | Terminal showing `docker run -d --name mysite -p 8080:80 static-site:1.0` and `docker ps` displaying container status and port mapping `0.0.0.0:8080->80/tcp`. | `figure_16_4_docker_run.png` |
| **Figure 16.5** | Step 7: Browser Verification | Web browser visiting `http://localhost:8080` displaying *"Welcome to My Static Website"* with student academic details (Angulakshmi S, 192524402). | `figure_16_5_browser_localhost.png` |
| **Figure 16.6** | Step 8: Docker Logs & Cleanup | Terminal showing `docker logs mysite`, `docker stop mysite`, and `docker rm mysite`. | `figure_16_6_logs_cleanup.png` |

---
*Note: A complete local HTTP verification and asset check transcript is recorded in [`output/run_output.txt`](../output/run_output.txt).*
