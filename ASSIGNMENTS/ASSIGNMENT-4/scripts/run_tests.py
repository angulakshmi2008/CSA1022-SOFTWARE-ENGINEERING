"""
Command-line test runner for Smart Campus Facility Platform.
Executes unit, integration, and regression tests and produces standard reports.
"""

import os
import subprocess
import sys


def main():
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    evidence_dir = os.path.join(project_dir, "docs", "evidence")
    os.makedirs(evidence_dir, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests",
        "-v",
        "--cov=app",
        f"--cov-report=xml:{os.path.join(evidence_dir, 'coverage.xml')}",
        f"--cov-report=html:{os.path.join(evidence_dir, 'coverage-report')}",
        "--cov-report=term",
        f"--junitxml={os.path.join(evidence_dir, 'test-results.xml')}",
    ]

    print("[*] Running comprehensive test suite with coverage and JUnit XML export...")
    print(f"[*] Command: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=project_dir)
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
