"""
Git Sandbox Simulation and Verification for Experiment 25:
Creating a GitHub Repository and Pushing a README File

Author: Angulakshmi S (192524402)
Department: CSE / AI & Data Science, Saveetha School of Engineering, SIMATS
"""

import os
import shutil
import subprocess
import tempfile
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def run_git_sandbox():
    sandbox_base = os.path.join(tempfile.gettempdir(), "git_exp25_sandbox")
    if os.path.exists(sandbox_base):
        shutil.rmtree(sandbox_base, ignore_errors=True)
    os.makedirs(sandbox_base, exist_ok=True)

    remote_dir = os.path.join(sandbox_base, "remote", "My-Personal-Project.git")
    local_dir = os.path.join(sandbox_base, "local", "My-Personal-Project")
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

    # 1. Initialize Bare Remote Repository representing GitHub remote
    run_cmd(["git", "init", "--bare", "--initial-branch=main", remote_dir], log_comment="Initialize remote repository on GitHub")

    # 2. Seed initial repository with initial README.md via temporary clone
    temp_init = os.path.join(sandbox_base, "temp_init")
    run_cmd(["git", "clone", remote_dir, temp_init], log_comment="GitHub web initializes repository with README.md")
    readme_init = os.path.join(temp_init, "README.md")
    with open(readme_init, "w", encoding="utf-8") as f:
        f.write("# My-Personal-Project\n\nInitial repository created on GitHub.\n")
    run_cmd(["git", "config", "user.name", "Angulakshmi S"], cwd=temp_init)
    run_cmd(["git", "config", "user.email", "angulakshmi2008@example.com"], cwd=temp_init)
    run_cmd(["git", "add", "README.md"], cwd=temp_init)
    run_cmd(["git", "commit", "-m", "Initial commit"], cwd=temp_init)
    run_cmd(["git", "push", "origin", "main"], cwd=temp_init)

    # 3. Step 2 in Manual: Clone the repository to the local machine
    os.makedirs(os.path.dirname(local_dir), exist_ok=True)
    run_cmd(["git", "clone", remote_dir, local_dir], log_comment="Step 2: Clone repository to local machine")
    run_cmd(["git", "config", "user.name", "Angulakshmi S"], cwd=local_dir)
    run_cmd(["git", "config", "user.email", "angulakshmi2008@example.com"], cwd=local_dir)

    # Step 3 in Manual: Navigate to repository and list files
    run_cmd(["git", "status"], cwd=local_dir, log_comment="Check initial clean working tree")

    # Step 4 in Manual: Open and modify README.md
    readme_local = os.path.join(local_dir, "README.md")
    updated_readme_content = (
        "# My-Personal-Project\n\n"
        "A personal software development repository demonstrating version control best practices using Git and GitHub.\n\n"
        "## Project Description\n"
        "This repository hosts utility scripts, algorithms, and documentation developed as part of the Software Engineering curriculum.\n\n"
        "## Features\n"
        "- Modular code architecture for algorithms and utilities.\n"
        "- Clean Git commit history following imperative message standards.\n"
        "- Documentation and environment setup instructions.\n\n"
        "## Author Details\n"
        "- **Student Name:** Angulakshmi S\n"
        "- **Register Number:** 192524402\n"
        "- **Department:** Computer Science and Engineering / AI & Data Science\n"
        "- **Institution:** Saveetha School of Engineering, SIMATS\n"
    )
    with open(readme_local, "w", encoding="utf-8") as f:
        f.write(updated_readme_content)

    # Step 5 in Manual: Verify the changes with git status and git diff
    run_cmd(["git", "status"], cwd=local_dir, log_comment="Step 5: Verify changes (modified: README.md)")
    run_cmd(["git", "diff"], cwd=local_dir, log_comment="Inspect line-by-line diff")

    # Step 6 in Manual: Stage the changes with git add
    run_cmd(["git", "add", "README.md"], cwd=local_dir, log_comment="Step 6: Stage README.md into index")
    run_cmd(["git", "status"], cwd=local_dir, log_comment="Verify staged changes ready to be committed")

    # Step 7 in Manual: Commit the changes
    run_cmd(["git", "commit", "-m", "Updated README with project description"], cwd=local_dir, log_comment="Step 7: Commit staged changes")

    # Step 8 in Manual: Push changes to GitHub
    run_cmd(["git", "push", "origin", "main"], cwd=local_dir, log_comment="Step 8: Push commits to remote origin main")

    # Verification: Log history
    run_cmd(["git", "log", "--graph", "--oneline", "--all"], cwd=local_dir, log_comment="Verify commit log and branch sync")

    # Write transcript
    transcript_text = "\n".join(transcript)
    out_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "terminal_transcript.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(transcript_text)
    print(f"[PASS] Real sandbox terminal transcript written to {out_file}")

def generate_git_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    # Three areas of Git + Remote
    boxes = [
        (0.5, 3.4, 2.0, 1.8, "#FFEBEE", "#C62828", "Working Directory\n\n• Edit README.md\n• Modified state\n• Local disk files"),
        (2.9, 3.4, 2.0, 1.8, "#FFF9C4", "#F57F17", "Staging Area (Index)\n\n• git add README.md\n• Prepares snapshot\n• Changes to be committed"),
        (5.3, 3.4, 2.0, 1.8, "#E8F5E9", "#2E7D32", "Local Repository\n\n• git commit -m '...'\n• HEAD -> main\n• SHA snapshot saved"),
        (7.7, 3.4, 2.0, 1.8, "#E1F5FE", "#0277BD", "Remote Repository\n(GitHub)\n\n• origin/main\n• Synchronized\n• Collaborator access"),
    ]

    for x, y, w, h, bg, border, txt in boxes:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, txt, ha="center", va="center", fontsize=8.5, color="#212121")

    # Arrows
    arrowprops = dict(arrowstyle="->", lw=2, color="#37474F")
    ax.annotate("", xy=(2.9, 4.3), xytext=(2.5, 4.3), arrowprops=arrowprops)
    ax.text(2.7, 4.5, "git add", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#C62828")

    ax.annotate("", xy=(5.3, 4.3), xytext=(4.9, 4.3), arrowprops=arrowprops)
    ax.text(5.1, 4.5, "git commit", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#F57F17")

    ax.annotate("", xy=(7.7, 4.3), xytext=(7.3, 4.3), arrowprops=arrowprops)
    ax.text(7.5, 4.5, "git push", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#2E7D32")

    # Lower info box
    info = patches.FancyBboxPatch((0.5, 0.6), 9.2, 2.1, boxstyle="round,pad=0.15", facecolor="#ECEFF1", edgecolor="#78909C", linewidth=1.2)
    ax.add_patch(info)
    desc = (
        "Experiment 25: Git Version Control Lifecycle Architecture\n"
        "Student: Angulakshmi S (Reg: 192524402) | Department of CSE / AI & Data Science\n"
        "1. git clone: Copies remote repository including full commit history to local machine.\n"
        "2. Working Directory -> Staging Area: git add stages modified README.md.\n"
        "3. Staging Area -> Local Repository: git commit permanently records snapshot with author metadata.\n"
        "4. Local Repository -> Remote GitHub: git push origin main transmits commits to upstream remote."
    )
    ax.text(5.1, 1.65, desc, ha="center", va="center", fontsize=8.5, color="#37474F", linespacing=1.35)

    plt.title("Git Repository Lifecycle: Working Directory -> Index -> Local HEAD -> Remote GitHub", fontsize=11, fontweight="bold", pad=12)

    diagram_dir = os.path.join(os.path.dirname(__file__), "..", "diagrams")
    os.makedirs(diagram_dir, exist_ok=True)
    out_img = os.path.join(diagram_dir, "git_create_push_flow.png")
    plt.tight_layout()
    plt.savefig(out_img, dpi=300)
    plt.close()
    print(f"[PASS] Architecture diagram generated at {out_img}")

if __name__ == "__main__":
    print("=== Running Experiment 25 Git Sandbox Simulation ===")
    run_git_sandbox()
    generate_git_diagram()
    print("=== All Experiment 25 Steps Completed Successfully ===")
