"""
Experiment 19: GitHub Actions CD Verification & Architecture Generator
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
import matplotlib.pyplot as plt
import matplotlib.patches as patches

base_dir = os.path.dirname(os.path.abspath(__file__))
exp_dir = os.path.abspath(os.path.join(base_dir, ".."))
app_dir = os.path.join(exp_dir, "app")
out_dir = os.path.join(exp_dir, "output")
diag_dir = os.path.join(exp_dir, "diagrams")
os.makedirs(out_dir, exist_ok=True)
os.makedirs(diag_dir, exist_ok=True)

sys.path.insert(0, app_dir)
from app import app
from werkzeug.serving import make_server

class ServerThread(threading.Thread):
    def __init__(self, app, port=5002):
        super().__init__()
        self.server = make_server('127.0.0.1', port, app)
        self.ctx = app.app_context()
        self.ctx.push()
        self.daemon = True

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

def run_verification():
    print("=" * 80)
    print("EXPERIMENT 19: CONTINUOUS DEPLOYMENT USING GITHUB ACTIONS & DOCKER")
    print("STUDENT: Angulakshmi S | REGISTER NUMBER: 192524402")
    print("=" * 80)

    # 1. Inspect Workflow YAML
    wf_file = os.path.join(exp_dir, "workflows", "cd.yml")
    print(f"\n[1] VALIDATING GITHUB ACTIONS WORKFLOW SPECIFICATION:")
    print(f"  * Path: {wf_file}")
    print(f"  * Exists: {os.path.exists(wf_file)} ({os.path.getsize(wf_file)} bytes)")
    with open(wf_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print(f"  * Total Lines: {len(lines)}")
    key_steps = [line.strip() for line in lines if "name:" in line or "uses:" in line]
    for s in key_steps[:8]:
        print(f"    - {s}")

    # 2. Local App Server Testing
    print(f"\n[2] TESTING APPLICATION RUNTIME ENDPOINTS:")
    port = 5002
    server = ServerThread(app, port=port)
    server.start()
    time.sleep(1)

    try:
        url = f"http://127.0.0.1:{port}/"
        with urllib.request.urlopen(url) as res:
            data = json.loads(res.read().decode("utf-8"))
            print(f"  * GET / Response Status: {res.getcode()} OK")
            print(f"  * Deployed Version:      {data['version']}")
            print(f"  * Author Verified:       {data['author']} ({data['reg_no']})")
            print(f"  * CI/CD Engine:          {data['ci_cd_platform']}")
            print(f"  * Container Registry:    {data['registry']}")

        health_url = f"http://127.0.0.1:{port}/health"
        with urllib.request.urlopen(health_url) as res:
            h_data = json.loads(res.read().decode("utf-8"))
            print(f"  * GET /health Status:    {res.getcode()} OK -> {h_data['status']}")

    finally:
        server.shutdown()

    print("\n" + "=" * 80)
    print("[3] CONTINUOUS DEPLOYMENT PIPELINE STAGES:")
    print("  1. git push origin main        -> Triggers GitHub Actions Runner (ubuntu-latest)")
    print("  2. actions/checkout@v4         -> Pulls latest application source code")
    print("  3. docker/login-action@v3      -> Authenticates using DOCKERHUB_USERNAME / TOKEN secrets")
    print("  4. docker/build-push-action@v6 -> Builds image and pushes tags 'latest' and '${{ github.sha }}'")
    print("  5. Cloud Deployment            -> Updates AWS ECS service / Cloud webhook for zero-downtime rollout")
    print("=" * 80)

def generate_diagram(output_path):
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    ax.text(5.5, 5.0, "GitHub Actions Continuous Deployment (CD) Architecture", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1e293b')
    ax.text(5.5, 4.6, "Student: Angulakshmi S (192524402) | CSA10 - Software Engineering", 
            ha='center', va='center', fontsize=9.5, color='#64748b')

    components = [
        ("Git Push", 0.6, 2.0, 1.8, 1.8, "#2563eb", "#eff6ff", "Developer\nCommit & Push\nto main branch"),
        ("GitHub Actions", 3.0, 1.7, 2.4, 2.4, "#7c3aed", "#faf5ff", "Runner: ubuntu-latest\n- Checkout Code\n- Docker Build\n- Tag (SHA, latest)\n- Docker Hub Login"),
        ("Docker Hub", 6.0, 2.0, 2.0, 1.8, "#0284c7", "#f0f9ff", "Container Registry\nImage: gha-docker-cd\nTags: :latest, :sha"),
        ("Cloud Platform", 8.6, 2.0, 2.0, 1.8, "#059669", "#ecfdf5", "AWS ECS / Render\nZero-Downtime Rollout\nhttp://<cloud-url>:5000")
    ]

    for title, x, y, w, h, col, bg, desc in components:
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", ec=col, fc=bg, lw=2)
        ax.add_patch(box)
        header = patches.FancyBboxPatch((x, y + h - 0.5), w, 0.5, boxstyle="round,pad=0.04", ec=col, fc=col)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 0.25, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color='white')
        ax.text(x + w/2, y + (h - 0.5)/2, desc, ha='center', va='center', fontsize=8, color='#1e293b')

    # Arrows between components
    ax.annotate("", xy=(3.0, 2.9), xytext=(2.4, 2.9), arrowprops=dict(arrowstyle="->", color="#2563eb", lw=2.5))
    ax.annotate("", xy=(6.0, 2.9), xytext=(5.4, 2.9), arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=2.5))
    ax.annotate("", xy=(8.6, 2.9), xytext=(8.0, 2.9), arrowprops=dict(arrowstyle="->", color="#0284c7", lw=2.5))

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print("Saved CD diagram to", output_path)

if __name__ == "__main__":
    diag_path = os.path.join(diag_dir, "gha_cd_pipeline.png")
    generate_diagram(diag_path)

    report_file = os.path.join(out_dir, "run_output.txt")
    orig_stdout = sys.stdout
    with open(report_file, "w", encoding="utf-8") as f:
        sys.stdout = f
        run_verification()
    sys.stdout = orig_stdout
    run_verification()
    print(f"\n[+] Real run log saved to: {report_file}")
