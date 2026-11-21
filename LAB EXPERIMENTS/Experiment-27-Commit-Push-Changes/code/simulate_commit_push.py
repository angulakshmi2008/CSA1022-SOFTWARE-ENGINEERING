"""
Git Sandbox Simulation and Verification for Experiment 27:
Committing and Pushing Changes to GitHub

Author: Angulakshmi S (192524402)
Department: CSE / AI & Data Science, Saveetha School of Engineering, SIMATS
"""

import os
import shutil
import subprocess
import tempfile
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def run_git_commit_push_sandbox():
    sandbox_base = os.path.join(tempfile.gettempdir(), "git_exp27_sandbox")
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

    # 1. Initialize Bare Remote
    run_cmd(["git", "init", "--bare", "--initial-branch=main", remote_dir], log_comment="Initialize remote repository on GitHub")

    # 2. Seed initial remote content
    temp_seed = os.path.join(sandbox_base, "seed")
    run_cmd(["git", "clone", remote_dir, temp_seed], log_comment="Seed initial repository on GitHub")
    with open(os.path.join(temp_seed, "README.md"), "w", encoding="utf-8") as f:
        f.write("# My-Personal-Project\n\nInitial repository description.\n")
    run_cmd(["git", "config", "user.name", "Angulakshmi S"], cwd=temp_seed)
    run_cmd(["git", "config", "user.email", "angulakshmi2008@example.com"], cwd=temp_seed)
    run_cmd(["git", "add", "README.md"], cwd=temp_seed)
    run_cmd(["git", "commit", "-m", "Initial commit"], cwd=temp_seed)
    run_cmd(["git", "push", "origin", "main"], cwd=temp_seed)

    # 3. Step 1 in Manual: Clone the repository
    run_cmd(["git", "clone", remote_dir, local_dir], log_comment="Step 1: Clone repository locally")
    run_cmd(["git", "config", "user.name", "Angulakshmi S"], cwd=local_dir)
    run_cmd(["git", "config", "user.email", "angulakshmi2008@example.com"], cwd=local_dir)

    # 4. Step 2 in Manual: Navigate to repository
    run_cmd(["git", "status"], cwd=local_dir, log_comment="Step 2: Navigate and check clean status")

    # 5. Step 3 in Manual: Open and modify the file
    readme_local = os.path.join(local_dir, "README.md")
    updated_content = (
        "# My-Personal-Project\n\n"
        "A personal software development repository demonstrating version control best practices using Git and GitHub.\n\n"
        "## Project Description\n"
        "This repository hosts utility scripts, algorithms, and documentation developed as part of the Software Engineering curriculum.\n\n"
        "## Experiment 27: Staged & Committed Changes\n"
        "- Updated README documentation with project objectives.\n"
        "- Staged modifications into the Git index.\n"
        "- Committed changes with message: Updated README.\n"
        "- Pushed commit to remote GitHub repository (origin/main).\n\n"
        "## Student Information\n"
        "- **Name:** Angulakshmi S\n"
        "- **Register Number:** 192524402\n"
        "- **Course:** CSA10 - Software Engineering Lab\n"
        "- **Institution:** Saveetha School of Engineering, SIMATS\n"
    )
    with open(readme_local, "w", encoding="utf-8") as f:
        f.write(updated_content)

    # 6. Step 4 in Manual: Verify the changes with git status
    run_cmd(["git", "status"], cwd=local_dir, log_comment="Step 4: Verify modified state (Changes not staged for commit)")
    run_cmd(["git", "diff"], cwd=local_dir, log_comment="View unstaged diff")

    # 7. Step 5 in Manual: Stage the changes with git add
    run_cmd(["git", "add", "README.md"], cwd=local_dir, log_comment="Step 5: Stage changes into index (git add README.md)")
    run_cmd(["git", "status"], cwd=local_dir, log_comment="Verify staged state (Changes to be committed)")

    # 8. Step 6 in Manual: Commit the changes
    run_cmd(["git", "commit", "-m", "Updated README"], cwd=local_dir, log_comment="Step 6: Commit changes (git commit -m 'Updated README')")
    run_cmd(["git", "status"], cwd=local_dir, log_comment="Verify local commit ahead of origin/main by 1 commit")

    # 9. Step 7 in Manual: Push changes to GitHub
    run_cmd(["git", "push", "origin", "main"], cwd=local_dir, log_comment="Step 7: Push changes to remote (git push origin main)")

    # 10. Step 8 in Manual: Verify the push
    run_cmd(["git", "status"], cwd=local_dir, log_comment="Step 8: Verify working tree clean and synchronized")
    run_cmd(["git", "log", "--graph", "--oneline", "--all"], cwd=local_dir, log_comment="Verify complete commit history graph")

    # Save transcript
    transcript_text = "\n".join(transcript)
    out_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "terminal_transcript.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(transcript_text)
    print(f"[PASS] Real sandbox terminal transcript written to {out_file}")

def generate_commit_push_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    states = [
        (0.5, 3.4, 2.1, 1.8, "#FFCDD2", "#C62828", "State 1: Modified\n\n• README.md edited\n• 'Changes not staged\n  for commit'\n• Untracked in index"),
        (2.9, 3.4, 2.1, 1.8, "#FFF59D", "#F57F17", "State 2: Staged\n\n• git add README.md\n• 'Changes to be\n  committed'\n• Ready for snapshot"),
        (5.3, 3.4, 2.1, 1.8, "#C8E6C9", "#2E7D32", "State 3: Committed\n\n• git commit -m '...'\n• 'Your branch is ahead\n  by 1 commit'\n• Local commit recorded"),
        (7.7, 3.4, 2.1, 1.8, "#BBDEFB", "#1565C0", "State 4: Pushed & Sync\n\n• git push origin main\n• 'working tree clean'\n• Local & remote\n  synchronized"),
    ]

    for x, y, w, h, bg, border, txt in states:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, txt, ha="center", va="center", fontsize=8.5, color="#212121")

    arrowprops = dict(arrowstyle="->", lw=2, color="#37474F")
    ax.annotate("", xy=(2.9, 4.3), xytext=(2.6, 4.3), arrowprops=arrowprops)
    ax.annotate("", xy=(5.3, 4.3), xytext=(5.0, 4.3), arrowprops=arrowprops)
    ax.annotate("", xy=(7.7, 4.3), xytext=(7.4, 4.3), arrowprops=arrowprops)

    # Lower info box
    info = patches.FancyBboxPatch((0.5, 0.6), 9.3, 2.1, boxstyle="round,pad=0.15", facecolor="#ECEFF1", edgecolor="#78909C", linewidth=1.2)
    ax.add_patch(info)
    desc = (
        "Experiment 27: Commit & Push State Transition Lifecycle\n"
        "Student: Angulakshmi S (Reg: 192524402) | Department of CSE / AI & Data Science\n"
        "• Modified -> Staged: git add stages file into the index.\n"
        "• Staged -> Committed: git commit generates SHA-1 hash with author and message.\n"
        "• Committed -> Pushed: git push sends local commits to GitHub origin/main.\n"
        "• Status Verification: git status reflects transition through all 4 distinct working tree states."
    )
    ax.text(5.15, 1.65, desc, ha="center", va="center", fontsize=8.5, color="#37474F", linespacing=1.35)

    plt.title("Git State Transitions: Working Tree -> Staged -> Committed -> Pushed", fontsize=11, fontweight="bold", pad=12)

    diagram_dir = os.path.join(os.path.dirname(__file__), "..", "diagrams")
    os.makedirs(diagram_dir, exist_ok=True)
    out_img = os.path.join(diagram_dir, "git_commit_push_lifecycle.png")
    plt.tight_layout()
    plt.savefig(out_img, dpi=300)
    plt.close()
    print(f"[PASS] Architecture diagram generated at {out_img}")

if __name__ == "__main__":
    print("=== Running Experiment 27 Git Sandbox Simulation ===")
    run_git_commit_push_sandbox()
    generate_commit_push_diagram()
    print("=== All Experiment 27 Steps Completed Successfully ===")
