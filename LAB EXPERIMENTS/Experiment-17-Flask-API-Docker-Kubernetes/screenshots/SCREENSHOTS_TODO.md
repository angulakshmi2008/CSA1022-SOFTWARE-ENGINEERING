# Screenshots Required for Experiment 17: Flask API Containerized with Docker, Pushed to Docker Hub and Deployed on Kubernetes

**Student Name:** Angulakshmi S  
**Register Number:** 192524402  
**Course:** CSA10 - Software Engineering  

If running Docker Desktop, Docker Hub, and Kubernetes / Minikube, please capture the following screens and place them in this `screenshots/` directory:

| Figure No. | Step Reference | Description to Capture | Recommended File Name |
| :--- | :--- | :--- | :--- |
| **Figure 17.1** | Step 1 & 2: Flask API & Dockerfile | VS Code showing `app/app.py` and `Dockerfile` side-by-side. | `figure_17_1_code_dockerfile.png` |
| **Figure 17.2** | Step 3: Build & Local Run | Terminal showing `docker build -t <user>/flask-api:1.0 .`, `docker run -d -p 5000:5000 --name api <user>/flask-api:1.0`, and `curl http://localhost:5000/api/students`. | `figure_17_2_docker_build_curl.png` |
| **Figure 17.3** | Step 4: Docker Hub Push | Browser visiting `hub.docker.com` showing repository `flask-api` with tag `1.0` successfully pushed. | `figure_17_3_dockerhub_repo.png` |
| **Figure 17.4** | Step 5: Kubernetes Node Status | Terminal running `kubectl get nodes` showing status `Ready`. | `figure_17_4_k8s_nodes.png` |
| **Figure 17.5** | Step 6 & 7: K8s Manifests | VS Code showing `k8s/deployment.yaml` and `k8s/service.yaml`. | `figure_17_5_k8s_manifests.png` |
| **Figure 17.6** | Step 8: Apply Manifests | Terminal showing `kubectl apply -f deployment.yaml`, `kubectl apply -f service.yaml`, `kubectl get pods -o wide` (2/2 running), and `kubectl get svc` showing NodePort `5000:30007/TCP`. | `figure_17_6_kubectl_resources.png` |
| **Figure 17.7** | Step 9: NodePort API Access | Browser visiting `http://localhost:30007/` and `http://localhost:30007/api/students` displaying JSON responses. | `figure_17_7_browser_nodeport.png` |

---
*Note: A complete local Flask runtime verification log is provided in [`output/run_output.txt`](../output/run_output.txt).*
