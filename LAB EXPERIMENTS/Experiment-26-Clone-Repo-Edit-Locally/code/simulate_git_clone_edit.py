"""
Git Sandbox Simulation and Verification for Experiment 26:
Cloning a GitHub Repository and Editing Files Locally

Author: Angulakshmi S (192524402)
Department: CSE / AI & Data Science, Saveetha School of Engineering, SIMATS
"""

import os
import shutil
import subprocess
import tempfile
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def run_git_clone_edit_sandbox():
    sandbox_base = os.path.join(tempfile.gettempdir(), "git_exp26_sandbox")
    if os.path.exists(sandbox_base):
        shutil.rmtree(sandbox_base, ignore_errors=True)
    os.makedirs(sandbox_base, exist_ok=True)

    remote_dir = os.path.join(sandbox_base, "remote", "My-Personal-Project.git")
    local_dir = os.path.join(sandbox_base, "workspace", "My-Personal-Project")
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
    run_cmd(["git", "clone", remote_dir, temp_seed], log_comment="Seed upstream repository with base project")
    with open(os.path.join(temp_seed, "README.md"), "w", encoding="utf-8") as f:
        f.write("# My-Personal-Project\n\nA personal software development repository.\n")
    run_cmd(["git", "config", "user.name", "Angulakshmi S"], cwd=temp_seed)
    run_cmd(["git", "config", "user.email", "angulakshmi2008@example.com"], cwd=temp_seed)
    run_cmd(["git", "add", "README.md"], cwd=temp_seed)
    run_cmd(["git", "commit", "-m", "Initial commit from GitHub"], cwd=temp_seed)
    run_cmd(["git", "push", "origin", "main"], cwd=temp_seed)

    # 3. Step 2 in Manual: Clone the repository to the local machine
    run_cmd(["git", "clone", remote_dir, local_dir], log_comment="Step 2: Clone repository to local system")
    run_cmd(["git", "config", "user.name", "Angulakshmi S"], cwd=local_dir)
    run_cmd(["git", "config", "user.email", "angulakshmi2008@example.com"], cwd=local_dir)

    # 4. Step 3 in Manual: Navigate to repository and list contents
    run_cmd(["git", "status"], cwd=local_dir, log_comment="Step 3: Verify clean working directory")
    run_cmd(["git", "remote", "-v"], cwd=local_dir, log_comment="Verify origin remote fetch and push URLs")

    # 5. Step 4 in Manual: Open and modify a file locally
    readme_local = os.path.join(local_dir, "README.md")
    updated_content = (
        "# My-Personal-Project\n\n"
        "A personal software development repository demonstrating version control best practices using Git and GitHub.\n\n"
        "## Project Description\n"
        "This repository hosts utility scripts, algorithms, and documentation developed as part of the Software Engineering curriculum.\n\n"
        "## Local Modifications & New Modules\n"
        "- Added setup guide for virtual environments (python -m venv .venv).\n"
        "- Added code formatting standards using PEP 8 guidelines.\n"
        "- Configured Git pre-commit hooks for automated linting.\n\n"
        "## Contributors\n"
        "- **Angulakshmi S** (Register Number: 192524402) - CSE / AI & Data Science\n"
        "- Saveetha School of Engineering, SIMATS\n"
    )
    with open(readme_local, "w", encoding="utf-8") as f:
        f.write(updated_content)

    # 6. Step 5 in Manual: Verify the changes
    run_cmd(["git", "status"], cwd=local_dir, log_comment="Step 5: Verify changes with git status (modified: README.md)")
    run_cmd(["git", "diff"], cwd=local_dir, log_comment="Inspect working tree diff against HEAD")

    # Save transcript
    transcript_text = "\n".join(transcript)
    out_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "terminal_transcript.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(transcript_text)
    print(f"[PASS] Real sandbox terminal transcript written to {out_file}")

def generate_clone_edit_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    boxes = [
        (0.6, 3.4, 2.5, 1.8, "#E3F2FD", "#1565C0", "GitHub Remote\n(origin)\n• Hosted repository\n• Remote URL: https://...\n• Commit history & main branch"),
        (4.0, 3.4, 2.5, 1.8, "#FFF3E0", "#E65100", "Local Clone & Disk\n• git clone <url>\n• cd My-Personal-Project\n• Complete working tree & .git"),
        (7.4, 3.4, 2.2, 1.8, "#E8F5E9", "#2E7D32", "Local Workspace Edit\n• Open README.md in VS Code\n• Update documentation\n• git status -> modified"),
    ]

    for x, y, w, h, bg, border, txt in boxes:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, txt, ha="center", va="center", fontsize=8.5, color="#212121")

    arrowprops = dict(arrowstyle="->", lw=2, color="#37474F")
    ax.annotate("", xy=(4.0, 4.3), xytext=(3.1, 4.3), arrowprops=arrowprops)
    ax.text(3.55, 4.5, "git clone", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#1565C0")

    ax.annotate("", xy=(7.4, 4.3), xytext=(6.5, 4.3), arrowprops=arrowprops)
    ax.text(6.95, 4.5, "code / edit", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#E65100")

    # Lower info box
    info = patches.FancyBboxPatch((0.6, 0.6), 9.0, 2.1, boxstyle="round,pad=0.15", facecolor="#ECEFF1", edgecolor="#78909C", linewidth=1.2)
    ax.add_patch(info)
    desc = (
        "Experiment 26: Clone and Local File Modification Architecture\n"
        "Student: Angulakshmi S (Reg: 192524402) | Saveetha School of Engineering, SIMATS\n"
        "1. git clone creates an identical local replica including all objects, commits, and refs.\n"
        "2. Working tree files are directly modifiable in any text editor or IDE.\n"
        "3. git status tracks file modifications comparing the working tree against the index.\n"
        "4. git diff displays exact unstaged line additions and deletions before staging."
    )
    ax.text(5.1, 1.65, desc, ha="center", va="center", fontsize=8.5, color="#37474F", linespacing=1.35)

    plt.title("Git Clone, Inspection & Local Working Directory Modification Flow", fontsize=11, fontweight="bold", pad=12)

    diagram_dir = os.path.join(os.path.dirname(__file__), "..", "diagrams")
    os.makedirs(diagram_dir, exist_ok=True)
    out_img = os.path.join(diagram_dir, "git_clone_edit_flow.png")
    plt.tight_layout()
    plt.savefig(out_img, dpi=300)
    plt.close()
    print(f"[PASS] Architecture diagram generated at {out_img}")

if __name__ == "__main__":
    print("=== Running Experiment 26 Git Sandbox Simulation ===")
    run_git_clone_edit_sandbox()
    generate_clone_edit_diagram()
    print("=== All Experiment 26 Steps Completed Successfully ===")
