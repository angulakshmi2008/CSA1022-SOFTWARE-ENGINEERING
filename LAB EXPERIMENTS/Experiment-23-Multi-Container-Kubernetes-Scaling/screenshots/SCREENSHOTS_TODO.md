# Screenshots To-Do List - Experiment 23

**Student Name:** Angulakshmi S  
**Register Number:** 192524402  
**Experiment:** Multi-Container Application (Frontend, Backend, Database) on Kubernetes with Scaling  
**Course:** CSA10 - Software Engineering Laboratory  

This document details the live screenshots required from a running Kubernetes cluster (Minikube or Docker Desktop Kubernetes):

| Step # | Screenshot Description | Expected Command / Window | File Destination |
|:---:|:---|:---|:---|
| **Step 1** | Cluster startup and namespace creation | `minikube start`, `kubectl create namespace multiapp` | `screenshots/01_cluster_start_namespace.png` |
| **Step 6** | Applying all manifests and viewing active resources | `kubectl apply -f k8s/` and `kubectl get all` showing Pods, Deployments, and Services in `Running` status | `screenshots/02_kubectl_get_all_running.png` |
| **Step 7** | Detailed Pod and Service status | `kubectl get pods -o wide` and `kubectl get svc` displaying ClusterIPs and NodePort 30080 | `screenshots/03_kubectl_get_pods_svc.png` |
| **Step 7** | Live Frontend Application in Web Browser | Web browser visiting `http://<minikube-ip>:30080` displaying the Student Portal table | `screenshots/04_frontend_portal_browser.png` |
| **Step 7** | Kubernetes Dashboard Overview | Browser viewing `minikube dashboard` showing Deployments, Pods, and Services in namespace `multiapp` | `screenshots/05_kubernetes_dashboard.png` |
| **Step 8** | Manual scaling to 4 frontend replicas | `kubectl scale deployment frontend --replicas=4` and `kubectl get pods -l app=frontend` showing 4 active pods | `screenshots/06_kubectl_scale_4_pods.png` |
| **Step 8** | Horizontal Pod Autoscaler (HPA) status | `kubectl get hpa` showing CPU utilization targets and replica thresholds | `screenshots/07_hpa_status.png` |

> *Note: If Minikube or Docker Desktop is not currently running locally, execute `minikube start` followed by `kubectl apply -f k8s/` inside Minikube or cloud playground (e.g. Killercoda Kubernetes playground).*
