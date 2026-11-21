"""
Verification and Test Script for Experiment 24:
CI/CD Pipeline for Flask Application using GitHub Actions with Cloud Deployment

Author: Angulakshmi S (192524402)
Department: CSE / AI & Data Science, Saveetha School of Engineering, SIMATS
"""

import os
import sys
import subprocess
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def run_pytest():
    app_dir = os.path.join(os.path.dirname(__file__), "..", "app")
    test_file = os.path.join(app_dir, "test_app.py")
    cmd = [sys.executable, "-m", "pytest", test_file, "-v"]
    env = os.environ.copy()
    env["PYTHONPATH"] = app_dir
    print(f"[EXEC] Running command: {' '.join(cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr)
    assert proc.returncode == 0, "pytest suite failed!"
    print("[PASS] Pytest suite executed and passed successfully.")

def validate_pipeline_manifest():
    wf_path = os.path.join(os.path.dirname(__file__), "..", "workflows", "ci-cd.yml")
    assert os.path.exists(wf_path), "Workflow file missing!"
    with open(wf_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "test:" in content and "build-and-push:" in content and "deploy:" in content
    assert "needs: test" in content and "needs: build-and-push" in content
    print("[PASS] GitHub Actions workflow YAML structure & stage dependencies validated.")

def generate_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)

    # Stages: Commit -> Test -> Build & Push -> Deploy
    stages = [
        (0.5, 3.2, 2.0, 1.8, "#E3F2FD", "#1565C0", "Stage 1: Developer Push\n• git push origin main\n• Triggers GitHub Actions\n• Webhook Dispatch"),
        (3.0, 3.2, 2.2, 1.8, "#E8F5E9", "#2E7D32", "Stage 2: CI Test Job\n• Runner: ubuntu-latest\n• Python 3.11 environment\n• pytest test_app.py\n• Result: 4 passed"),
        (5.7, 3.2, 2.3, 1.8, "#FFF3E0", "#EF6C00", "Stage 3: Build & Push\n• needs: test\n• Docker Buildx Engine\n• Build multi-platform img\n• Push to Docker Hub"),
        (8.5, 3.2, 2.1, 1.8, "#F3E5F5", "#7B1FA2", "Stage 4: Cloud CD\n• needs: build-and-push\n• Deploy to Heroku/Render\n• Zero-downtime release\n• Live App on Cloud"),
    ]

    for x, y, w, h, bg, border, txt in stages:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", facecolor=bg, edgecolor=border, linewidth=1.6)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, txt, ha="center", va="center", fontsize=8.5, color="#212121")

    arrowprops = dict(arrowstyle="->", lw=2, color="#37474F")
    ax.annotate("", xy=(3.0, 4.1), xytext=(2.5, 4.1), arrowprops=arrowprops)
    ax.annotate("", xy=(5.7, 4.1), xytext=(5.2, 4.1), arrowprops=arrowprops)
    ax.annotate("", xy=(8.5, 4.1), xytext=(8.0, 4.1), arrowprops=arrowprops)

    # Lower explanatory card
    card = patches.FancyBboxPatch((0.5, 0.6), 10.1, 2.0, boxstyle="round,pad=0.15", facecolor="#ECEFF1", edgecolor="#78909C", linewidth=1.2)
    ax.add_patch(card)
    summary = (
        "Pipeline Architecture & Security Controls:\n"
        "• Quality Gate: If pytest fails, build-and-push and deploy jobs are skipped, preventing broken builds in production.\n"
        "• Secret Masking: Sensitive keys (DOCKERHUB_TOKEN, CLOUD_API_KEY) are encrypted in GitHub Secrets.\n"
        "• Immutable Artifacts: Tags created with semantic versions and Git commit SHAs (${{ github.sha }}).\n"
        "• Student Author: Angulakshmi S (Reg: 192524402) | CSA10 Software Engineering Laboratory"
    )
    ax.text(5.5, 1.6, summary, ha="center", va="center", fontsize=8.5, color="#37474F", linespacing=1.35)

    plt.title("Automated CI/CD Pipeline Flow (GitHub Actions -> Docker Hub -> Cloud Web Service)", fontsize=11, fontweight="bold", pad=12)

    diagram_dir = os.path.join(os.path.dirname(__file__), "..", "diagrams")
    os.makedirs(diagram_dir, exist_ok=True)
    out_img = os.path.join(diagram_dir, "cicd_cloud_pipeline.png")
    plt.tight_layout()
    plt.savefig(out_img, dpi=300)
    plt.close()
    print(f"[PASS] Pipeline diagram generated at {out_img}")

if __name__ == "__main__":
    print("=== Running Experiment 24 Automated Verification ===")
    run_pytest()
    validate_pipeline_manifest()
    generate_pipeline_diagram()
    print("=== All Experiment 24 Verifications Passed Successfully ===")
