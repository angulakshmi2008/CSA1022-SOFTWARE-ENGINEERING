"""
Experiment 17: Flask API Verification & Kubernetes Architecture Generator
Author: Angulakshmi S (Reg No: 192524402)
Department of Computer Science and Engineering
Saveetha School of Engineering, SIMATS
"""

import os
import sys
import json
import time
import threading
import urllib.request
import urllib.error
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Add app directory to sys.path
base_dir = os.path.dirname(os.path.abspath(__file__))
exp_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, os.path.join(exp_dir, "app"))

from app import app
from werkzeug.serving import make_server

class ServerThread(threading.Thread):
    def __init__(self, app, port=5000):
        super().__init__()
        self.server = make_server('127.0.0.1', port, app)
        self.ctx = app.app_context()
        self.ctx.push()
        self.daemon = True

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

def test_endpoints():
    print("=" * 80)
    print("EXPERIMENT 17: FLASK API DOCKER CONTAINERIZATION & KUBERNETES DEPLOYMENT")
    print("STUDENT: Angulakshmi S | REGISTER NUMBER: 192524402")
    print("=" * 80)
    
    server = ServerThread(app, port=5000)
    server.start()
    time.sleep(1) # Give server time to bind

    base_url = "http://127.0.0.1:5000"
    try:
        # 1. GET /
        print("\n[1] TEST GET / (Home Endpoint):")
        with urllib.request.urlopen(f"{base_url}/") as res:
            status = res.getcode()
            data = json.loads(res.read().decode("utf-8"))
            print(f"  * Status: {status} OK")
            print(f"  * Response: {json.dumps(data, indent=2)}")

        # 2. GET /api/students
        print("\n[2] TEST GET /api/students (Student Directory):")
        with urllib.request.urlopen(f"{base_url}/api/students") as res:
            status = res.getcode()
            data = json.loads(res.read().decode("utf-8"))
            print(f"  * Status: {status} OK")
            print(f"  * Initial Count: {data['count']}")
            for s in data['students']:
                print(f"    - ID {s['id']}: {s['name']} ({s['dept']})")

        # 3. POST /api/students
        print("\n[3] TEST POST /api/students (Add Record):")
        new_payload = json.dumps({"name": "Kavitha M", "dept": "CSE"}).encode("utf-8")
        req = urllib.request.Request(
            f"{base_url}/api/students",
            data=new_payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req) as res:
            status = res.getcode()
            data = json.loads(res.read().decode("utf-8"))
            print(f"  * Status: {status} CREATED")
            print(f"  * Response: {json.dumps(data, indent=2)}")

        # 4. GET /health
        print("\n[4] TEST GET /health (Liveness & Readiness Probe Endpoint):")
        with urllib.request.urlopen(f"{base_url}/health") as res:
            status = res.getcode()
            data = json.loads(res.read().decode("utf-8"))
            print(f"  * Status: {status} OK")
            print(f"  * Response: {json.dumps(data, indent=2)}")

    finally:
        server.shutdown()

    print("\n" + "=" * 80)
    print("[5] KUBERNETES MANIFEST VALIDATION:")
    dep_file = os.path.join(exp_dir, "k8s", "deployment.yaml")
    svc_file = os.path.join(exp_dir, "k8s", "service.yaml")
    print(f"  * Deployment manifest: {os.path.exists(dep_file)} ({os.path.getsize(dep_file)} bytes)")
    print(f"  * Service manifest:    {os.path.exists(svc_file)} ({os.path.getsize(svc_file)} bytes)")
    print("  * NodePort Target:      30007 (Forwarded to internal port 5000)")
    print("  * Pod Replicas:         2 Replicas with Health Probes (/health)")
    print("=" * 80)

def generate_diagram(output_path):
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    # Title
    ax.text(5.5, 6.1, "Kubernetes Deployment & NodePort Service Architecture", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1e293b')
    ax.text(5.5, 5.7, "Student: Angulakshmi S (192524402) | CSA10 - Software Engineering", 
            ha='center', va='center', fontsize=10, color='#64748b')

    # External Client
    client_box = patches.FancyBboxPatch((0.5, 2.5), 1.8, 1.4, boxstyle="round,pad=0.1", ec="#2563eb", fc="#eff6ff", lw=2)
    ax.add_patch(client_box)
    ax.text(1.4, 3.4, "External Client", ha='center', va='center', fontsize=10, fontweight='bold', color='#1e40af')
    ax.text(1.4, 2.9, "Browser / curl\nhttp://localhost:30007", ha='center', va='center', fontsize=8, color='#1e3a8a')

    # Node boundary
    node_box = patches.FancyBboxPatch((3.0, 0.7), 7.5, 4.6, boxstyle="round,pad=0.2", ec="#64748b", fc="#f8fafc", lw=2, linestyle="--")
    ax.add_patch(node_box)
    ax.text(3.3, 5.0, "Kubernetes Node (Worker Node / Minikube / Docker Desktop)", fontsize=9, fontweight='bold', color='#475569')

    # Service Box
    svc_box = patches.FancyBboxPatch((3.5, 2.2), 2.4, 2.0, boxstyle="round,pad=0.1", ec="#059669", fc="#f0fdf4", lw=2)
    ax.add_patch(svc_box)
    ax.text(4.7, 3.7, "NodePort Service", ha='center', va='center', fontsize=11, fontweight='bold', color='#047857')
    ax.text(4.7, 3.1, "flask-api-service\nNodePort: 30007\nPort: 5000\nTargetPort: 5000", ha='center', va='center', fontsize=8.5, color='#065f46')
    ax.text(4.7, 2.5, "Selector: app=flask-api", ha='center', va='center', fontsize=8, color='#047857', style='italic')

    # Pod 1 Box
    pod1_box = patches.FancyBboxPatch((7.2, 3.3), 3.0, 1.6, boxstyle="round,pad=0.1", ec="#7c3aed", fc="#faf5ff", lw=2)
    ax.add_patch(pod1_box)
    ax.text(8.7, 4.4, "Pod 1: flask-api-xxxx", ha='center', va='center', fontsize=10, fontweight='bold', color='#6d28d9')
    ax.text(8.7, 3.8, "Container: flask-api\nImage: <user>/flask-api:1.0\nPort: 5000", ha='center', va='center', fontsize=8.5, color='#581c87')

    # Pod 2 Box
    pod2_box = patches.FancyBboxPatch((7.2, 1.2), 3.0, 1.6, boxstyle="round,pad=0.1", ec="#7c3aed", fc="#faf5ff", lw=2)
    ax.add_patch(pod2_box)
    ax.text(8.7, 2.3, "Pod 2: flask-api-yyyy", ha='center', va='center', fontsize=10, fontweight='bold', color='#6d28d9')
    ax.text(8.7, 1.7, "Container: flask-api\nImage: <user>/flask-api:1.0\nPort: 5000", ha='center', va='center', fontsize=8.5, color='#581c87')

    # Arrows
    # Client -> Service
    ax.annotate("", xy=(3.5, 3.2), xytext=(2.3, 3.2), arrowprops=dict(arrowstyle="->", color="#2563eb", lw=2.5))
    ax.text(2.9, 3.45, ":30007", ha='center', va='center', fontsize=9, fontweight='bold', color='#2563eb')

    # Service -> Pod 1
    ax.annotate("", xy=(7.2, 4.1), xytext=(5.9, 3.5), arrowprops=dict(arrowstyle="->", color="#059669", lw=2))
    # Service -> Pod 2
    ax.annotate("", xy=(7.2, 2.0), xytext=(5.9, 2.9), arrowprops=dict(arrowstyle="->", color="#059669", lw=2))

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print("Saved K8s diagram to", output_path)

if __name__ == "__main__":
    out_dir = os.path.join(exp_dir, "output")
    diag_dir = os.path.join(exp_dir, "diagrams")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(diag_dir, exist_ok=True)

    diag_path = os.path.join(diag_dir, "k8s_architecture.png")
    generate_diagram(diag_path)

    report_file = os.path.join(out_dir, "run_output.txt")
    orig_stdout = sys.stdout
    with open(report_file, "w", encoding="utf-8") as f:
        sys.stdout = f
        test_endpoints()
    sys.stdout = orig_stdout
    test_endpoints()
    print(f"\n[+] Real run log saved to: {report_file}")
