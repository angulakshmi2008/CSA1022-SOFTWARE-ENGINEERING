"""
Git Sandbox Simulation and Verification for Experiment 28:
Pulling Collaborator Changes from GitHub

Author: Angulakshmi S (192524402)
Department: CSE / AI & Data Science, Saveetha School of Engineering, SIMATS
"""

import os
import shutil
import subprocess
import tempfile
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def run_git_collab_sandbox():
    sandbox_base = os.path.join(tempfile.gettempdir(), "git_exp28_sandbox")
    if os.path.exists(sandbox_base):
        shutil.rmtree(sandbox_base, ignore_errors=True)
    os.makedirs(sandbox_base, exist_ok=True)

    remote_dir = os.path.join(sandbox_base, "remote", "collab_repo.git")
    student_dir = os.path.join(sandbox_base, "student_workstation", "collab_repo")
    collab_dir = os.path.join(sandbox_base, "collaborator_workstation", "collab_repo")
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

    # 2. Seed initial commit from Student workstation
    run_cmd(["git", "clone", remote_dir, student_dir], log_comment="Student clones empty repository")
    run_cmd(["git", "config", "user.name", "Angulakshmi S"], cwd=student_dir)
    run_cmd(["git", "config", "user.email", "angulakshmi2008@example.com"], cwd=student_dir)
    readme_path = os.path.join(student_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# Collaborative Project Repository\n\nInitial repository created by Angulakshmi S (192524402).\n")
    run_cmd(["git", "add", "README.md"], cwd=student_dir)
    run_cmd(["git", "commit", "-m", "Initial repository setup"], cwd=student_dir)
    run_cmd(["git", "push", "origin", "main"], cwd=student_dir)

    # 3. Step 1 in Manual: Collaborator clones and pushes changes to GitHub
    run_cmd(["git", "clone", remote_dir, collab_dir], log_comment="Step 1: Collaborator clones repository on separate workstation")
    run_cmd(["git", "config", "user.name", "Peer Collaborator"], cwd=collab_dir)
    run_cmd(["git", "config", "user.email", "collaborator@example.com"], cwd=collab_dir)

    # Collaborator edits README.md and creates contributor_notes.txt
    collab_readme = os.path.join(collab_dir, "README.md")
    with open(collab_readme, "a", encoding="utf-8") as f:
        f.write("\n## Collaborator Contribution\nAdded project guidelines and team contribution workflow.\n")
    notes_file = os.path.join(collab_dir, "contributor_notes.txt")
    with open(notes_file, "w", encoding="utf-8") as f:
        f.write("Project Collaboration Notes:\n- Verified unit test suite.\n- Added guidelines.\n")
    
    run_cmd(["git", "add", "README.md", "contributor_notes.txt"], cwd=collab_dir, log_comment="Collaborator stages changes")
    run_cmd(["git", "commit", "-m", "Collaborator: Added project guidelines and notes"], cwd=collab_dir, log_comment="Collaborator commits changes")
    run_cmd(["git", "push", "origin", "main"], cwd=collab_dir, log_comment="Collaborator pushes changes to GitHub origin/main")

    # 4. Step 2 in Manual: On student's local machine, pull latest changes
    run_cmd(["git", "status"], cwd=student_dir, log_comment="Step 2: Student checks local status before pulling")
    run_cmd(["git", "pull", "origin", "main"], cwd=student_dir, log_comment="Step 2: Student executes git pull origin main (Fast-forward)")

    # 5. Step 3 in Manual: Verify local repository is up to date and check files
    run_cmd(["git", "status"], cwd=student_dir, log_comment="Step 3: Verify student working tree is clean and synchronized")
    run_cmd(["git", "log", "--graph", "--oneline", "--all"], cwd=student_dir, log_comment="Inspect updated commit graph showing collaborator's commit")

    # Save transcript
    transcript_text = "\n".join(transcript)
    out_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "terminal_transcript.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(transcript_text)
    print(f"[PASS] Real sandbox terminal transcript written to {out_file}")

def generate_pull_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    nodes = [
        (0.6, 3.4, 2.4, 1.8, "#FFF3E0", "#E65100", "Collaborator Machine\n(Dev-2)\n• Edits README.md\n• git commit\n• git push origin main"),
        (3.8, 3.4, 2.4, 1.8, "#E3F2FD", "#1565C0", "Central GitHub Remote\n(origin/main)\n• Holds latest commit\n• Ahead of local by 1\n• Single source of truth"),
        (7.0, 3.4, 2.4, 1.8, "#E8F5E9", "#2E7D32", "Student Machine\n(Angulakshmi S)\n• git pull origin main\n• Fast-forward merge\n• Working tree updated"),
    ]

    for x, y, w, h, bg, border, txt in nodes:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, txt, ha="center", va="center", fontsize=8.5, color="#212121")

    arrowprops = dict(arrowstyle="->", lw=2, color="#37474F")
    ax.annotate("", xy=(3.8, 4.3), xytext=(3.0, 4.3), arrowprops=arrowprops)
    ax.text(3.4, 4.5, "git push", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#E65100")

    ax.annotate("", xy=(7.0, 4.3), xytext=(6.2, 4.3), arrowprops=arrowprops)
    ax.text(6.6, 4.5, "git pull", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#2E7D32")

    # Lower info box
    info = patches.FancyBboxPatch((0.6, 0.6), 8.8, 2.1, boxstyle="round,pad=0.15", facecolor="#ECEFF1", edgecolor="#78909C", linewidth=1.2)
    ax.add_patch(info)
    desc = (
        "Experiment 28: Remote Synchronization (git pull) Architecture\n"
        "Student: Angulakshmi S (Reg: 192524402) | Department of CSE / AI & Data Science\n"
        "1. git pull combines: (a) git fetch origin (downloads objects) + (b) git merge origin/main (integrates into HEAD).\n"
        "2. Fast-Forward Merge: When local branch has no divergent commits, Git simply moves HEAD pointer forward.\n"
        "3. Local disk files and working tree are immediately updated to reflect collaborator's additions.\n"
        "4. git log displays the full unified timeline of contributions across team members."
    )
    ax.text(5.0, 1.65, desc, ha="center", va="center", fontsize=8.5, color="#37474F", linespacing=1.35)

    plt.title("Collaborator Synchronization Flow: Remote Origin -> git pull -> Local Workspace", fontsize=11, fontweight="bold", pad=12)

    diagram_dir = os.path.join(os.path.dirname(__file__), "..", "diagrams")
    os.makedirs(diagram_dir, exist_ok=True)
    out_img = os.path.join(diagram_dir, "git_pull_collaborator_flow.png")
    plt.tight_layout()
    plt.savefig(out_img, dpi=300)
    plt.close()
    print(f"[PASS] Architecture diagram generated at {out_img}")

if __name__ == "__main__":
    print("=== Running Experiment 28 Git Sandbox Simulation ===")
    run_git_collab_sandbox()
    generate_pull_diagram()
    print("=== All Experiment 28 Steps Completed Successfully ===")
