"""
Git Sandbox Simulation and Verification for Experiment 29:
Feature Branch (feature-login) and Pull Request

Author: Angulakshmi S (192524402)
Department: CSE / AI & Data Science, Saveetha School of Engineering, SIMATS
"""

import os
import shutil
import subprocess
import tempfile
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def run_git_feature_pr_sandbox():
    sandbox_base = os.path.join(tempfile.gettempdir(), "git_exp29_sandbox")
    if os.path.exists(sandbox_base):
        shutil.rmtree(sandbox_base, ignore_errors=True)
    os.makedirs(sandbox_base, exist_ok=True)

    remote_dir = os.path.join(sandbox_base, "remote", "portal_repo.git")
    local_dir = os.path.join(sandbox_base, "local", "portal_repo")
    os.makedirs(remote_dir, exist_ok=True)

    transcript = []

    def run_cmd(cmd_args, cwd=None, log_comment=None):
        if log_comment:
            transcript.append(f"# {log_comment}")
        cmd_str = " ".join(cmd_args)
        transcript.append(f"$ {cmd_str}")
        res = subprocess.run(cmd_args, cwd=cwd, capture_output=True, text=True)
        if res.stdout:
            transcript.append(res.stdout.strip())
        if res.stderr:
            transcript.append(res.stderr.strip())
        transcript.append("")
        return res

    # 1. Initialize Bare Remote
    run_cmd(["git", "init", "--bare", "--initial-branch=main", remote_dir], log_comment="Initialize remote repository on GitHub")

    # 2. Seed initial commit on main
    temp_seed = os.path.join(sandbox_base, "seed")
    run_cmd(["git", "clone", remote_dir, temp_seed], log_comment="Seed base repository on GitHub")
    with open(os.path.join(temp_seed, "README.md"), "w", encoding="utf-8") as f:
        f.write("# Student Portal Application\n\nProduction codebase for college student services.\n")
    run_cmd(["git", "config", "user.name", "Angulakshmi S"], cwd=temp_seed)
    run_cmd(["git", "config", "user.email", "angulakshmi2008@example.com"], cwd=temp_seed)
    run_cmd(["git", "add", "README.md"], cwd=temp_seed)
    run_cmd(["git", "commit", "-m", "Initial production baseline"], cwd=temp_seed)
    run_cmd(["git", "push", "origin", "main"], cwd=temp_seed)

    # 3. Step 1 in Manual: Clone repository to local machine
    run_cmd(["git", "clone", remote_dir, local_dir], log_comment="Step 1: Clone repository locally")
    run_cmd(["git", "config", "user.name", "Angulakshmi S"], cwd=local_dir)
    run_cmd(["git", "config", "user.email", "angulakshmi2008@example.com"], cwd=local_dir)

    # 4. Step 2 in Manual: Create and switch to feature branch
    run_cmd(["git", "checkout", "-b", "feature-login"], cwd=local_dir, log_comment="Step 2: Create feature branch (feature-login)")
    run_cmd(["git", "branch"], cwd=local_dir, log_comment="Verify current active branch is feature-login")

    # 5. Step 3 in Manual: Implement the login feature
    src_folder = os.path.join(local_dir, "src")
    os.makedirs(src_folder, exist_ok=True)
    login_py_src = os.path.join(os.path.dirname(__file__), "..", "src", "login.py")
    with open(login_py_src, "r", encoding="utf-8") as f:
        login_content = f.read()
    with open(os.path.join(src_folder, "login.py"), "w", encoding="utf-8") as f:
        f.write(login_content)

    # 6. Step 4 in Manual: Stage and commit the login feature
    run_cmd(["git", "status"], cwd=local_dir, log_comment="Step 4: Check untracked files on feature-login branch")
    run_cmd(["git", "add", "src/login.py"], cwd=local_dir, log_comment="Stage src/login.py")
    run_cmd(["git", "commit", "-m", "Added login feature"], cwd=local_dir, log_comment="Commit feature implementation")

    # 7. Step 5 in Manual: Push feature branch to GitHub
    run_cmd(["git", "push", "-u", "origin", "feature-login"], cwd=local_dir, log_comment="Step 5: Push feature-login branch to GitHub")

    # 8. Step 6 in Manual: Pull Request review & merge simulation
    # On GitHub, PR #1 is created: base: main <- compare: feature-login
    # Continuous integration checks pass, peer review approves, and PR is merged into main:
    run_cmd(["git", "checkout", "main"], cwd=local_dir, log_comment="Step 6: Switch back to main branch for PR merge")
    run_cmd(["git", "merge", "--no-ff", "feature-login", "-m", "Merge pull request #1 from feature-login (Added login feature)"],
            cwd=local_dir, log_comment="Merge Pull Request #1 into main branch")
    run_cmd(["git", "push", "origin", "main"], cwd=local_dir, log_comment="Push merged main branch to GitHub")

    # Verify branch history graph
    run_cmd(["git", "log", "--graph", "--oneline", "--all"], cwd=local_dir, log_comment="Verify non-fast-forward merge commit and branch topology")

    # Save transcript
    transcript_text = "\n".join(transcript)
    out_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "terminal_transcript.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(transcript_text)
    print(f"[PASS] Real sandbox terminal transcript written to {out_file}")

def generate_feature_pr_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    boxes = [
        (0.6, 3.4, 2.3, 1.8, "#E3F2FD", "#1565C0", "Main Branch\n(Production)\n• Baseline code\n• Protected branch\n• Never edited directly"),
        (3.8, 3.4, 2.4, 1.8, "#FFF3E0", "#E65100", "feature-login Branch\n• git checkout -b\n• Implements src/login.py\n• Commit & push -u origin"),
        (7.0, 3.4, 2.4, 1.8, "#E8F5E9", "#2E7D32", "Pull Request & Merge\n• Compare: feature-login\n• Base: main\n• Code Review & CI checks\n• Merged into main"),
    ]

    for x, y, w, h, bg, border, txt in boxes:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, txt, ha="center", va="center", fontsize=8.5, color="#212121")

    arrowprops = dict(arrowstyle="->", lw=2, color="#37474F")
    ax.annotate("", xy=(3.8, 4.3), xytext=(2.9, 4.3), arrowprops=arrowprops)
    ax.text(3.35, 4.5, "branch", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#E65100")

    ax.annotate("", xy=(7.0, 4.3), xytext=(6.2, 4.3), arrowprops=arrowprops)
    ax.text(6.6, 4.5, "PR & Merge", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#2E7D32")

    # Lower info box
    info = patches.FancyBboxPatch((0.6, 0.6), 8.8, 2.1, boxstyle="round,pad=0.15", facecolor="#ECEFF1", edgecolor="#78909C", linewidth=1.2)
    ax.add_patch(info)
    desc = (
        "Experiment 29: Feature Branching & Pull Request Architecture\n"
        "Student: Angulakshmi S (Reg: 192524402) | Department of CSE / AI & Data Science\n"
        "1. Branch Isolation: Development of new features occurs safely in 'feature-login' without disrupting 'main'.\n"
        "2. Upstream Tracking: git push -u origin feature-login configures remote tracking reference.\n"
        "3. Pull Request Collaboration: GitHub PR allows line-by-line diff review, automated testing, and team approvals.\n"
        "4. Non-Fast-Forward Merge: Merging into main preserves branch topology and exact historical audit trails."
    )
    ax.text(5.0, 1.65, desc, ha="center", va="center", fontsize=8.5, color="#37474F", linespacing=1.35)

    plt.title("Feature Branch Workflow: Isolation -> Upstream Push -> Pull Request -> Merge", fontsize=11, fontweight="bold", pad=12)

    diagram_dir = os.path.join(os.path.dirname(__file__), "..", "diagrams")
    os.makedirs(diagram_dir, exist_ok=True)
    out_img = os.path.join(diagram_dir, "feature_branch_pr_flow.png")
    plt.tight_layout()
    plt.savefig(out_img, dpi=300)
    plt.close()
    print(f"[PASS] Architecture diagram generated at {out_img}")

if __name__ == "__main__":
    print("=== Running Experiment 29 Git Sandbox Simulation ===")
    run_git_feature_pr_sandbox()
    generate_feature_pr_diagram()
    print("=== All Experiment 29 Steps Completed Successfully ===")
