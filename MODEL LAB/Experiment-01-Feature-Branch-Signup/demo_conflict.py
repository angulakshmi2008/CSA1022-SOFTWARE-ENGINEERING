"""
Safe Simulation Script: Demonstrating Git Merge Conflict Detection and Resolution
Does NOT touch or alter the real working repository. Runs inside a temporary sandbox.
"""

import os
import shutil
import subprocess
import tempfile


def run_git(cmd, cwd):
    """Runs a git shell command and returns stdout and exit code."""
    res = subprocess.run(
        cmd,
        cwd=cwd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return res.stdout.strip(), res.stderr.strip(), res.returncode


def main():
    print("=" * 70)
    print(" SAFE SIMULATION: GIT MERGE CONFLICT LIFECYCLE DEMONSTRATION")
    print("=" * 70)

    # 1. Create isolated temp directory
    temp_dir = tempfile.mkdtemp(prefix="git_conflict_demo_")
    print(f"[+] Created temporary sandbox at: {temp_dir}\n")

    try:
        # 2. Initialize local Git repository
        run_git("git init -b main", temp_dir)
        run_git('git config user.name "Student Demo"', temp_dir)
        run_git('git config user.email "student@simats.edu"', temp_dir)

        # 3. Create initial base file
        file_path = os.path.join(temp_dir, "auth_rule.py")
        with open(file_path, "w") as f:
            f.write("# Authentication Validation Rule\n")
            f.write("MIN_PASSWORD_LENGTH = 6\n")
            f.write("def validate_password(p):\n")
            f.write("    return len(p) >= MIN_PASSWORD_LENGTH\n")

        run_git("git add auth_rule.py", temp_dir)
        run_git('git commit -m "Initial commit: Base 6-char password rule"', temp_dir)
        print("[1] Initial commit created on 'main' branch.")

        # 4. Create and checkout feature branch 'feature-strict'
        run_git("git checkout -b feature-strict", temp_dir)
        with open(file_path, "w") as f:
            f.write("# Authentication Validation Rule\n")
            f.write("MIN_PASSWORD_LENGTH = 8  # Increased to 8 by Feature Team\n")
            f.write("def validate_password(p):\n")
            f.write("    return len(p) >= MIN_PASSWORD_LENGTH\n")

        run_git("git add auth_rule.py", temp_dir)
        run_git('git commit -m "feat: increase minimum password length to 8"', temp_dir)
        print("[2] Committed change on branch 'feature-strict' (MIN_PASSWORD_LENGTH = 8).")

        # 5. Switch back to main and make a conflicting edit
        run_git("git checkout main", temp_dir)
        with open(file_path, "w") as f:
            f.write("# Authentication Validation Rule\n")
            f.write("MIN_PASSWORD_LENGTH = 10  # Increased to 10 by Security Admin on Main\n")
            f.write("def validate_password(p):\n")
            f.write("    return len(p) >= MIN_PASSWORD_LENGTH\n")

        run_git("git add auth_rule.py", temp_dir)
        run_git('git commit -m "sec: increase minimum password length to 10 on main"', temp_dir)
        print("[3] Committed conflicting change on 'main' (MIN_PASSWORD_LENGTH = 10).")

        # 6. Attempt merge -> Triggers Merge Conflict!
        print("\n[4] Attempting merge: 'git merge feature-strict' into 'main'...")
        out, err, code = run_git("git merge feature-strict", temp_dir)
        print(f"    Exit code: {code} (Non-zero indicates conflict)")
        print(f"    Git output:\n    {out}\n")

        # 7. Inspect conflict markers injected by Git
        print("[5] Inspecting conflict markers in 'auth_rule.py':")
        with open(file_path, "r") as f:
            content = f.read()
        print("-" * 50)
        print(content.strip())
        print("-" * 50)

        # 8. Resolve the conflict programmatically (Simulate developer resolution)
        print("\n[6] Resolving conflict manually (agreeing on 10 characters with comments)...")
        resolved_content = (
            "# Authentication Validation Rule\n"
            "# Resolved Conflict: Team agreed on standardizing minimum length to 10 characters\n"
            "MIN_PASSWORD_LENGTH = 10\n"
            "def validate_password(p):\n"
            "    return len(p) >= MIN_PASSWORD_LENGTH\n"
        )
        with open(file_path, "w") as f:
            f.write(resolved_content)

        # 9. Stage and commit resolution
        run_git("git add auth_rule.py", temp_dir)
        run_git('git commit -m "Merge branch \'feature-strict\': resolve password length conflict"', temp_dir)
        print("[7] Conflict resolved, file staged ('git add') and committed successfully!")

        # 10. Display clean git log
        log_out, _, _ = run_git("git log --graph --oneline --all", temp_dir)
        print("\n[8] Final Git commit history graph:")
        print(log_out)
        print("\n[+] DEMONSTRATION COMPLETE: Conflict detected, handled, and resolved cleanly.")

    finally:
        # Clean up temporary sandbox
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"[+] Cleaned up temporary sandbox {temp_dir}.")


if __name__ == "__main__":
    main()
