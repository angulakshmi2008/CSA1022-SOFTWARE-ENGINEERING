"""
Git Sandbox Simulation and Verification for Experiment 30:
Forking, Feature Branch and Pull Request to Original Repository

Author: Angulakshmi S (192524402)
Department: CSE / AI & Data Science, Saveetha School of Engineering, SIMATS
"""

import os
import shutil
import subprocess
import tempfile
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def run_git_fork_pr_sandbox():
    sandbox_base = os.path.join(tempfile.gettempdir(), "git_exp30_sandbox")
    if os.path.exists(sandbox_base):
        shutil.rmtree(sandbox_base, ignore_errors=True)
    os.makedirs(sandbox_base, exist_ok=True)

    upstream_remote = os.path.join(sandbox_base, "upstream_remote", "3-Simple-Python-Projects.git")
    fork_remote = os.path.join(sandbox_base, "fork_remote", "3-Simple-Python-Projects.git")
    local_workspace = os.path.join(sandbox_base, "student_local", "3-Simple-Python-Projects")

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

    # 1. Initialize Upstream Bare Repository
    run_cmd(["git", "init", "--bare", "--initial-branch=main", upstream_remote], log_comment="Original owner initializes upstream repository")

    # 2. Seed initial upstream code
    temp_seed = os.path.join(sandbox_base, "seed")
    run_cmd(["git", "clone", upstream_remote, temp_seed], log_comment="Seed upstream repository with 3-Simple-Python-Projects")
    with open(os.path.join(temp_seed, "README.md"), "w", encoding="utf-8") as f:
        f.write("# 3-Simple-Python-Projects\n\nA collection of starter Python utility scripts.\n")
    with open(os.path.join(temp_seed, "ytDownloader.py"), "w", encoding="utf-8") as f:
        f.write("# Simple YouTube Downloader\ndef download_video(url):\n    print('Downloading video from', url)\n")
    run_cmd(["git", "config", "user.name", "Original Author"], cwd=temp_seed)
    run_cmd(["git", "config", "user.email", "author@example.com"], cwd=temp_seed)
    run_cmd(["git", "add", "README.md", "ytDownloader.py"], cwd=temp_seed)
    run_cmd(["git", "commit", "-m", "Initial upstream release"], cwd=temp_seed)
    run_cmd(["git", "push", "origin", "main"], cwd=temp_seed)

    # 3. Step 1 in Manual: Fork the repository on GitHub
    # In GitHub, forking copies upstream_remote to fork_remote
    run_cmd(["git", "clone", "--bare", upstream_remote, fork_remote], log_comment="Step 1: Student forks 3-Simple-Python-Projects on GitHub")

    # 4. Step 2 in Manual: Clone the forked repository to local machine
    run_cmd(["git", "clone", fork_remote, local_workspace], log_comment="Step 2: Clone forked repository locally")
    run_cmd(["git", "config", "user.name", "Angulakshmi S"], cwd=local_workspace)
    run_cmd(["git", "config", "user.email", "angulakshmi2008@example.com"], cwd=local_workspace)

    # Configure upstream remote
    run_cmd(["git", "remote", "-v"], cwd=local_workspace, log_comment="Check default origin remote pointing to fork")
    run_cmd(["git", "remote", "add", "upstream", upstream_remote], cwd=local_workspace, log_comment="Configure upstream remote to track original repository")
    run_cmd(["git", "remote", "-v"], cwd=local_workspace, log_comment="Verify both origin and upstream remotes")

    # 5. Step 3 in Manual: Create a feature branch named feature-update
    run_cmd(["git", "checkout", "-b", "feature-update"], cwd=local_workspace, log_comment="Step 3: Create and switch to feature-update branch")
    run_cmd(["git", "branch"], cwd=local_workspace, log_comment="Verify active branch is feature-update")

    # 6. Step 4-5 in Manual: Modify ytDownloader.py
    src_code_path = os.path.join(os.path.dirname(__file__), "..", "src", "ytDownloader.py")
    with open(src_code_path, "r", encoding="utf-8") as f:
        enhanced_code = f.read()
    with open(os.path.join(local_workspace, "ytDownloader.py"), "w", encoding="utf-8") as f:
        f.write(enhanced_code)

    run_cmd(["git", "status"], cwd=local_workspace, log_comment="Step 5: Verify modified ytDownloader.py")
    run_cmd(["git", "diff"], cwd=local_workspace, log_comment="Review code diff against original upstream version")

    # 7. Step 6 in Manual: Stage and commit the changes
    run_cmd(["git", "add", "ytDownloader.py"], cwd=local_workspace, log_comment="Step 6: Stage modified file")
    run_cmd(["git", "commit", "-m", "Added project info feature"], cwd=local_workspace, log_comment="Step 6: Commit changes ('Added project info feature')")

    # 8. Step 7 in Manual: Push feature branch to forked repository
    run_cmd(["git", "push", "-u", "origin", "feature-update"], cwd=local_workspace, log_comment="Step 7: Push feature-update branch to personal fork")

    # 9. Step 8-9 in Manual: Open Pull Request to original upstream repository and simulate merge
    upstream_workspace = os.path.join(sandbox_base, "upstream_owner", "3-Simple-Python-Projects")
    run_cmd(["git", "clone", upstream_remote, upstream_workspace], log_comment="Step 8: Upstream owner reviews incoming Pull Request")
    run_cmd(["git", "fetch", fork_remote, "feature-update"], cwd=upstream_workspace, log_comment="Upstream fetches PR branch from student's fork")
    run_cmd(["git", "merge", "--no-ff", "FETCH_HEAD", "-m", "Merge pull request #1 from angulakshmi2008/feature-update (Added project info feature)"],
            cwd=upstream_workspace, log_comment="Step 9: Upstream owner approves and merges PR into main")
    run_cmd(["git", "push", "origin", "main"], cwd=upstream_workspace, log_comment="Upstream main updated with merged contribution")

    # 10. Student syncs fork with upstream
    run_cmd(["git", "checkout", "main"], cwd=local_workspace, log_comment="Step 10: Student switches to main and synchronizes with upstream")
    run_cmd(["git", "fetch", "upstream"], cwd=local_workspace, log_comment="Fetch latest updates from upstream")
    run_cmd(["git", "merge", "upstream/main"], cwd=local_workspace, log_comment="Merge upstream/main into local main")
    run_cmd(["git", "push", "origin", "main"], cwd=local_workspace, log_comment="Push synchronized main to personal fork")

    # Check complete history graph
    run_cmd(["git", "log", "--graph", "--oneline", "--all"], cwd=local_workspace, log_comment="Inspect full commit graph showing fork, PR, and upstream sync")

    # Save transcript
    transcript_text = "\n".join(transcript)
    out_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "terminal_transcript.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(transcript_text)
    print(f"[PASS] Real sandbox terminal transcript written to {out_file}")

def generate_fork_pr_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 5.5), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6)

    boxes = [
        (0.5, 3.5, 2.3, 1.8, "#EDE7F6", "#512DA8", "Upstream Repository\n(Original Owner)\n• 3-Simple-Python-Projects\n• Base repository: main\n• Protected upstream"),
        (4.1, 3.5, 2.3, 1.8, "#E3F2FD", "#1565C0", "Personal Fork\n(Student: angulakshmi)\n• Independent server copy\n• origin: main & feature-update\n• Full write access"),
        (7.7, 3.5, 2.3, 1.8, "#E8F5E9", "#2E7D32", "Local Clone & Branch\n• git clone <fork_url>\n• git checkout -b feature-update\n• Edit ytDownloader.py\n• Commit & push origin"),
    ]

    for x, y, w, h, bg, border, txt in boxes:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, txt, ha="center", va="center", fontsize=8.5, color="#212121")

    arrowprops = dict(arrowstyle="->", lw=2, color="#37474F")
    # Fork action
    ax.annotate("", xy=(4.1, 4.4), xytext=(2.8, 4.4), arrowprops=arrowprops)
    ax.text(3.45, 4.6, "Fork on GitHub", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#512DA8")

    # Clone action
    ax.annotate("", xy=(7.7, 4.4), xytext=(6.4, 4.4), arrowprops=arrowprops)
    ax.text(7.05, 4.6, "git clone", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#1565C0")

    # PR action curved arrow back from Local/Fork to Upstream
    ax.annotate("Pull Request\n(fork:feature-update -> upstream:main)", xy=(1.65, 3.5), xytext=(5.25, 2.5),
                arrowprops=dict(arrowstyle="->", lw=2, color="#00796B", connectionstyle="arc3,rad=-0.2"),
                ha="center", va="top", fontsize=8.5, fontweight="bold", color="#004D40")

    # Lower info box
    info = patches.FancyBboxPatch((0.5, 0.5), 9.5, 1.8, boxstyle="round,pad=0.15", facecolor="#ECEFF1", edgecolor="#78909C", linewidth=1.2)
    ax.add_patch(info)
    desc = (
        "Experiment 30: Fork-and-Pull-Request Open-Source Collaboration Model\n"
        "Student: Angulakshmi S (Reg: 192524402) | Department of CSE / AI & Data Science\n"
        "• Fork: Creates a personal cloud repository when direct write permissions to upstream are restricted.\n"
        "• Remote Configuration: origin tracks personal fork; upstream tracks authoritative base project.\n"
        "• Upstream PR: Cross-repository Pull Request submits proposed feature for maintainer review and merge.\n"
        "• Upstream Sync: git fetch upstream && git merge upstream/main keeps personal fork current with master project."
    )
    ax.text(5.25, 1.4, desc, ha="center", va="center", fontsize=8.5, color="#37474F", linespacing=1.35)

    plt.title("Open-Source Contribution Architecture (Upstream -> Fork -> Clone -> Feature Branch -> Upstream PR)", fontsize=11, fontweight="bold", pad=12)

    diagram_dir = os.path.join(os.path.dirname(__file__), "..", "diagrams")
    os.makedirs(diagram_dir, exist_ok=True)
    out_img = os.path.join(diagram_dir, "fork_upstream_pr_flow.png")
    plt.tight_layout()
    plt.savefig(out_img, dpi=300)
    plt.close()
    print(f"[PASS] Architecture diagram generated at {out_img}")

if __name__ == "__main__":
    print("=== Running Experiment 30 Git Sandbox Simulation ===")
    run_git_fork_pr_sandbox()
    generate_fork_pr_diagram()
    print("=== All Experiment 30 Steps Completed Successfully ===")
