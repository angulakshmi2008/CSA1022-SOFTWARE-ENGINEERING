"""
Experiment 12: Prioritizing Task Management System Requirements using MoSCoW and Kano in Jira
Student: Angulakshmi S (Reg No: 192524402)
Course: CSA10 - Software Engineering
Course Outcome: CO2

This script:
1. Ingests the Task Management System backlog from CSV.
2. Performs dual-dimension requirements prioritization (Business Necessity vs Customer Satisfaction).
3. Evaluates sprint progress across Jira workflow columns (To Do, In Progress, Done).
4. Plots and saves the 2D MoSCoW-Kano Evaluation Matrix to 'output/moscow_kano_matrix.png'.
"""

import os
import csv
import matplotlib.pyplot as plt
import numpy as np

def analyze_requirements():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "config", "tms_jira_backlog.csv")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    items = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append(row)

    print("==================================================================")
    print("   JIRA TASK MANAGEMENT SYSTEM: MOSCOW & KANO DUAL EVALUATION     ")
    print("==================================================================")
    print("Project: Task Management System (Key: TMS1)")
    print("Sprint : TMS1 Sprint 1 | Duration: 1 Week")
    print("Team   : Angulakshmi S (192524402)")
    print("------------------------------------------------------------------")
    print(f"{'Key':<7} | {'Summary':<35} | {'MoSCoW':<11} | {'Kano':<12} | {'Status'}")
    print("-" * 80)
    for it in items:
        print(f"{it['Issue Key']:<7} | {it['Summary']:<35} | {it['MoSCoW Category']:<11} | {it['Kano Category']:<12} | {it['Status']}")

    print("\n------------------------------------------------------------------")
    print("Prioritization Synthesis:")
    print("  • Must Have + Basic       : Essential baseline foundation (Zero tolerance for omission)")
    print("  • Should Have + Performance: Linear competitive driver (Directly scales user satisfaction)")
    print("  • Could Have + Excitement  : Differentiator & delight factor (Competitive edge for team)")
    print("------------------------------------------------------------------")

    # Plot Kano Curves & Requirement Mapping
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    x = np.linspace(0.1, 10, 200)

    # 1. Basic (Must-be) curve: asymptotic flat dissatisfaction if not done
    y_basic = -8 / (x + 0.8) + 0.5
    # 2. Performance (One-dimensional): linear
    y_perf = 0.8 * x - 4
    # 3. Excitement (Attractive): exponential delight
    y_excite = 0.08 * (x ** 1.9)

    ax.plot(x, y_excite, 'g-', lw=2.2, label='Excitement (Attractive)')
    ax.plot(x, y_perf, 'b--', lw=2.2, label='Performance (One-dimensional)')
    ax.plot(x, y_basic, 'r-.', lw=2.2, label='Basic (Must-be / Expected)')

    # Plot candidate tasks on the curve
    # TMS1-2: Basic
    ax.plot([4.0], [-1.15], 'ro', markersize=9)
    ax.text(4.2, -1.5, "TMS1-2: User Login & Roles\n[Must Have | Basic]", fontsize=8.5, fontweight='bold', color='#922B21')

    # TMS1-3: Basic
    ax.plot([5.5], [-0.8], 'ro', markersize=9)
    ax.text(5.7, -1.0, "TMS1-3: Task Creation & Assign\n[Must Have | Basic]", fontsize=8.5, fontweight='bold', color='#922B21')

    # TMS1-4: Performance
    ax.plot([6.5], [1.2], 'bs', markersize=9)
    ax.text(4.0, 1.8, "TMS1-4: Prioritization & Deadlines\n[Should Have | Performance]", fontsize=8.5, fontweight='bold', color='#1F4E78')

    # TMS1-5: Excitement
    ax.plot([7.5], [3.6], 'g^', markersize=10)
    ax.text(5.2, 4.3, "TMS1-5: Progress Tracking & Reports\n[Could Have | Excitement]", fontsize=8.5, fontweight='bold', color='#145A32')

    ax.axhline(0, color='black', linewidth=1.0, linestyle=':')
    ax.axvline(5, color='black', linewidth=1.0, linestyle=':')

    ax.set_title("Kano vs MoSCoW Prioritization Landscape\nTask Management System | Saveetha School of Engineering | Angulakshmi S (192524402)", fontsize=10.5, fontweight='bold', pad=12)
    ax.set_xlabel("Degree of Requirement Implementation (Absent → Fully Implemented)", fontsize=9.5, fontweight='bold')
    ax.set_ylabel("Customer Satisfaction (Dissatisfied → Delighted)", fontsize=9.5, fontweight='bold')
    ax.set_xlim(0, 10.5)
    ax.set_ylim(-5, 6)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='lower right', frameon=True)

    chart_path = os.path.join(output_dir, "moscow_kano_matrix.png")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"Generated Kano-MoSCoW matrix chart at: {chart_path}")
    print("==================================================================")

if __name__ == "__main__":
    analyze_requirements()
