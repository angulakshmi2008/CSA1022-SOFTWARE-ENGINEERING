"""
Verification and Test Script for Experiment 23:
Multi-Container Application on Kubernetes with Scaling

Author: Angulakshmi S (192524402)
Department: CSE / AI & Data Science, Saveetha School of Engineering, SIMATS
"""

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Add backend directory to sys.path to test Flask API
backend_dir = os.path.join(os.path.dirname(__file__), "..", "backend")
sys.path.insert(0, backend_dir)
from app import app

def test_flask_backend():
    client = app.test_client()
    res_home = client.get("/")
    assert res_home.status_code == 200
    home_json = res_home.get_json()
    assert home_json["status"] == "healthy"
    assert home_json["register_number"] == "192524402"
    print("[PASS] Flask Backend Root endpoint verified (200 OK).")

    res_students = client.get("/api/students")
    assert res_students.status_code == 200
    stu_json = res_students.get_json()
    students_list = stu_json.get("data") if isinstance(stu_json, dict) else stu_json
    assert len(students_list) >= 4
    assert any("Angulakshmi S" in s.get("name", "") for s in students_list)
    print(f"[PASS] Flask /api/students endpoint verified ({len(students_list)} student records returned).")

def test_k8s_manifests():
    k8s_dir = os.path.join(os.path.dirname(__file__), "..", "k8s")
    manifests = ["mysql.yaml", "backend.yaml", "frontend.yaml", "hpa.yaml"]
    for m in manifests:
        path = os.path.join(k8s_dir, m)
        assert os.path.exists(path), f"Manifest {m} missing!"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "apiVersion:" in content and "kind:" in content
        print(f"[PASS] Kubernetes manifest {m} structure validated.")

def generate_topology_diagram():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)

    # External Client
    client_box = patches.FancyBboxPatch((0.5, 4.5), 1.8, 1.3, boxstyle="round,pad=0.15", facecolor="#E1F5FE", edgecolor="#0288D1", linewidth=1.5)
    ax.add_patch(client_box)
    ax.text(1.4, 5.15, "Client Browser\nhttp://<IP>:30080", ha="center", va="center", fontsize=9, fontweight="bold", color="#01579B")

    # Kubernetes Cluster Boundary
    k8s_boundary = patches.FancyBboxPatch((2.8, 0.5), 7.8, 6.0, boxstyle="round,pad=0.2", facecolor="#F8FAFC", edgecolor="#455A64", linewidth=1.5, linestyle="--")
    ax.add_patch(k8s_boundary)
    ax.text(6.7, 6.2, "Kubernetes Cluster (Namespace: multiapp)", ha="center", va="center", fontsize=11, fontweight="bold", color="#263238")

    # Tier 1: Frontend
    fe_box = patches.FancyBboxPatch((3.2, 3.8), 2.2, 1.8, boxstyle="round,pad=0.15", facecolor="#E8F5E9", edgecolor="#2E7D32", linewidth=1.5)
    ax.add_patch(fe_box)
    fe_text = "Frontend Tier\n• Nginx Alpine\n• NodePort: 30080\n• Replicas: 2 -> 4\n• HPA: 50% CPU"
    ax.text(4.3, 4.7, fe_text, ha="center", va="center", fontsize=8.5, color="#1B5E20")

    # Tier 2: Backend
    be_box = patches.FancyBboxPatch((5.8, 3.8), 2.1, 1.8, boxstyle="round,pad=0.15", facecolor="#FFF3E0", edgecolor="#EF6C00", linewidth=1.5)
    ax.add_patch(be_box)
    be_text = "Backend Tier\n• Flask REST API\n• ClusterIP: 5000\n• Replicas: 2\n• /api/students"
    ax.text(6.85, 4.7, be_text, ha="center", va="center", fontsize=8.5, color="#E65100")

    # Tier 3: Database
    db_box = patches.FancyBboxPatch((8.3, 3.8), 2.0, 1.8, boxstyle="round,pad=0.15", facecolor="#EDE7F6", edgecolor="#5E35B1", linewidth=1.5)
    ax.add_patch(db_box)
    db_text = "Database Tier\n• MySQL 8.0\n• ClusterIP: 3306\n• Secret & PVC 1Gi\n• init.sql Data"
    ax.text(9.3, 4.7, db_text, ha="center", va="center", fontsize=8.5, color="#4A148C")

    # Arrows between tiers
    arrowprops = dict(arrowstyle="->", lw=2, color="#37474F")
    ax.annotate("", xy=(3.2, 5.15), xytext=(2.3, 5.15), arrowprops=arrowprops)
    ax.text(2.75, 5.4, "NodePort\n:30080", ha="center", va="bottom", fontsize=7.5, color="#0277BD", fontweight="bold")

    ax.annotate("", xy=(5.8, 4.7), xytext=(5.4, 4.7), arrowprops=arrowprops)
    ax.text(5.6, 4.95, "HTTP\n:5000", ha="center", va="bottom", fontsize=7.5, color="#EF6C00", fontweight="bold")

    ax.annotate("", xy=(8.3, 4.7), xytext=(7.9, 4.7), arrowprops=arrowprops)
    ax.text(8.1, 4.95, "TCP\n:3306", ha="center", va="bottom", fontsize=7.5, color="#5E35B1", fontweight="bold")

    # Autoscaler & Monitoring Info Panel
    panel = patches.FancyBboxPatch((3.2, 0.8), 7.1, 2.3, boxstyle="round,pad=0.15", facecolor="#ECEFF1", edgecolor="#90A4AE", linewidth=1.2)
    ax.add_patch(panel)
    panel_desc = (
        "Autoscaling & Operational Management Architecture:\n"
        "• Scaling Command: kubectl scale deployment frontend --replicas=4\n"
        "• Horizontal Pod Autoscaler (HPA): min 2, max 6, target CPU 50%\n"
        "• Service Discovery: DNS Resolution via CoreDNS (mysql-service:3306, backend-service:5000)\n"
        "• Storage & Secrets: PersistentVolumeClaim ensures data persistence; Secret securely mounts root credentials.\n"
        "• Academic Ownership: Angulakshmi S (Reg: 192524402) | Saveetha School of Engineering, SIMATS"
    )
    ax.text(6.75, 1.95, panel_desc, ha="center", va="center", fontsize=8.5, color="#263238", linespacing=1.35)

    plt.title("Multi-Container Tiered Architecture & Scaling on Kubernetes", fontsize=11, fontweight="bold", pad=12)
    
    diagram_dir = os.path.join(os.path.dirname(__file__), "..", "diagrams")
    os.makedirs(diagram_dir, exist_ok=True)
    out_img = os.path.join(diagram_dir, "multi_container_k8s_topology.png")
    plt.tight_layout()
    plt.savefig(out_img, dpi=300)
    plt.close()
    print(f"[PASS] Topology diagram generated at {out_img}")

if __name__ == "__main__":
    print("=== Running Experiment 23 Automated Verification ===")
    test_flask_backend()
    test_k8s_manifests()
    generate_topology_diagram()
    print("=== All Experiment 23 Verifications Passed Successfully ===")
