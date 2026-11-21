"""
Automated Controlled Defect Injection, Execution, and Evidence Capture Script.
Demonstrates:
- Controlled Defect 1 (D1): Sensor threshold equality operator defect (>= instead of >).
- Controlled Defect 2 (D2): Priority matrix High/High defect (returns M2 instead of M1).
Saves genuine before-and-after terminal logs to docs/evidence/.
"""

import os
import subprocess
import sys


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EVIDENCE_DIR = os.path.join(PROJECT_DIR, "docs", "evidence")
SENSOR_FILE = os.path.join(PROJECT_DIR, "app", "services", "sensor_service.py")
PRIORITY_FILE = os.path.join(PROJECT_DIR, "app", "services", "priority_service.py")

os.makedirs(EVIDENCE_DIR, exist_ok=True)


def run_pytest(test_target: str) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "pytest", test_target, "-v", "--tb=short"]
    return subprocess.run(cmd, cwd=PROJECT_DIR, capture_output=True, text=True)


def demonstrate_defect_1():
    print("=" * 60)
    print("DEMONSTRATING CONTROLLED DEFECT 1: Sensor Threshold Operator")
    print("=" * 60)

    # Read original sensor_service.py
    with open(SENSOR_FILE, "r", encoding="utf-8") as f:
        original_code = f.read()

    # Inject defect: return value >= threshold instead of return value > threshold
    defective_code = original_code.replace(
        "return value > threshold",
        "return value >= threshold  # CONTROLLED DEFECT 1: Equality operator defect"
    )
    assert defective_code != original_code, "Failed to inject defect 1"

    with open(SENSOR_FILE, "w", encoding="utf-8") as f:
        f.write(defective_code)

    print("[*] Injected Controlled Defect 1: 'value >= threshold'")
    res_failing = run_pytest("tests/unit/test_sensor.py::test_u6_sensor_values_28_00_and_28_01")
    print(f"[*] Exit code: {res_failing.returncode} (Expected non-zero failure)")

    fail_log_path = os.path.join(EVIDENCE_DIR, "defect-1-failure.txt")
    with open(fail_log_path, "w", encoding="utf-8") as f:
        f.write("=== CONTROLLED DEFECT 1 EXECUTION FAILURE LOG ===\n")
        f.write("Injected defect: sensor_breached uses >= instead of strict >\n")
        f.write(f"Executed command: pytest tests/unit/test_sensor.py::test_u6_sensor_values_28_00_and_28_01\n")
        f.write(f"Return code: {res_failing.returncode}\n\n")
        f.write(res_failing.stdout + "\n" + res_failing.stderr)
    print(f"[+] Saved failure evidence to {fail_log_path}")

    # Revert / Correct
    with open(SENSOR_FILE, "w", encoding="utf-8") as f:
        f.write(original_code)
    print("[*] Reverted Controlled Defect 1 to correct strict greater-than logic")

    res_passing = run_pytest("tests/unit/test_sensor.py::test_u6_sensor_values_28_00_and_28_01")
    print(f"[*] Exit code: {res_passing.returncode} (Expected 0 passing)")

    pass_log_path = os.path.join(EVIDENCE_DIR, "defect-1-correction.txt")
    with open(pass_log_path, "w", encoding="utf-8") as f:
        f.write("=== CONTROLLED DEFECT 1 RESOLUTION AND PASSING RETEST LOG ===\n")
        f.write("Corrected code: return value > threshold\n")
        f.write(f"Executed command: pytest tests/unit/test_sensor.py::test_u6_sensor_values_28_00_and_28_01\n")
        f.write(f"Return code: {res_passing.returncode}\n\n")
        f.write(res_passing.stdout + "\n" + res_passing.stderr)
    print(f"[+] Saved correction evidence to {pass_log_path}")


def demonstrate_defect_2():
    print("\n" + "=" * 60)
    print("DEMONSTRATING CONTROLLED DEFECT 2: Priority Matrix Mapping")
    print("=" * 60)

    # Read original priority_service.py
    with open(PRIORITY_FILE, "r", encoding="utf-8") as f:
        original_code = f.read()

    # Inject defect: High/High returns M2 instead of M1
    defective_code = original_code.replace(
        '"High": "M1",',
        '"High": "M2",  # CONTROLLED DEFECT 2: Injected wrong priority'
    )
    assert defective_code != original_code, "Failed to inject defect 2"

    with open(PRIORITY_FILE, "w", encoding="utf-8") as f:
        f.write(defective_code)

    print("[*] Injected Controlled Defect 2: High/High -> M2")
    res_failing = run_pytest("tests/unit/test_priority.py::test_u1_high_impact_high_urgency")
    print(f"[*] Exit code: {res_failing.returncode} (Expected non-zero failure)")

    fail_log_path = os.path.join(EVIDENCE_DIR, "defect-2-failure.txt")
    with open(fail_log_path, "w", encoding="utf-8") as f:
        f.write("=== CONTROLLED DEFECT 2 EXECUTION FAILURE LOG ===\n")
        f.write("Injected defect: PRIORITY_MATRIX['High']['High'] returns 'M2' instead of 'M1'\n")
        f.write(f"Executed command: pytest tests/unit/test_priority.py::test_u1_high_impact_high_urgency\n")
        f.write(f"Return code: {res_failing.returncode}\n\n")
        f.write(res_failing.stdout + "\n" + res_failing.stderr)
    print(f"[+] Saved failure evidence to {fail_log_path}")

    # Revert / Correct
    with open(PRIORITY_FILE, "w", encoding="utf-8") as f:
        f.write(original_code)
    print("[*] Reverted Controlled Defect 2 to correct M1 mapping")

    res_passing = run_pytest("tests/unit/test_priority.py::test_u1_high_impact_high_urgency")
    print(f"[*] Exit code: {res_passing.returncode} (Expected 0 passing)")

    pass_log_path = os.path.join(EVIDENCE_DIR, "defect-2-correction.txt")
    with open(pass_log_path, "w", encoding="utf-8") as f:
        f.write("=== CONTROLLED DEFECT 2 RESOLUTION AND PASSING RETEST LOG ===\n")
        f.write("Corrected code: PRIORITY_MATRIX['High']['High'] = 'M1'\n")
        f.write(f"Executed command: pytest tests/unit/test_priority.py::test_u1_high_impact_high_urgency\n")
        f.write(f"Return code: {res_passing.returncode}\n\n")
        f.write(res_passing.stdout + "\n" + res_passing.stderr)
    print(f"[+] Saved correction evidence to {pass_log_path}")


if __name__ == "__main__":
    demonstrate_defect_1()
    demonstrate_defect_2()
    print("\n[SUCCESS] Both controlled defects successfully demonstrated, logged, and corrected.")
