"""
Experiment 09: Scrum Project with Backlog and Sprint Simulator
Student: Angulakshmi S (Reg No: 192524402)
Course: CSA10 - Software Engineering
Course Outcome: CO2

This script models the Jira Scrum lifecycle:
- Product Backlog management & Story Points estimation
- Sprint Planning for a 1-week sprint ("SP Sprint 1")
- Active Sprint tracking across To Do, In Progress, and Done
- Burndown trajectory calculation and visualization
"""

import os
import csv
import matplotlib.pyplot as plt

def parse_backlog_csv(file_path: str):
    items = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['Story Points'] = int(row['Story Points'])
            items.append(row)
    return items

def simulate_scrum_sprint():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "config", "jira_backlog_import.csv")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    items = parse_backlog_csv(csv_path)

    print("==================================================================")
    print("      JIRA SCRUM SPRINT SIMULATION - SP SPRINT 1 (1 WEEK)         ")
    print("==================================================================")
    print("Project: Scrum Workflow Project (Key: SP)")
    print("Sprint : SP Sprint 1 | Duration: 7 Days (1 Week)")
    print("Team   : Angulakshmi S (Developer / Scrum Team)")
    print("------------------------------------------------------------------")

    total_committed_points = sum(item['Story Points'] for item in items)
    completed_points = sum(item['Story Points'] for item in items if item['Status'] == 'Done')
    in_progress_points = sum(item['Story Points'] for item in items if item['Status'] == 'In Progress')
    to_do_points = sum(item['Story Points'] for item in items if item['Status'] == 'To Do')

    print(f"\n[Sprint Backlog Status]")
    print(f"{'Key':<6} | {'Type':<6} | {'Priority':<8} | {'Points':<6} | {'Status':<12} | {'Summary'}")
    print("-" * 75)
    for it in items:
        print(f"{it['Issue Key']:<6} | {it['Issue Type']:<6} | {it['Priority']:<8} | {it['Story Points']:<6} | {it['Status']:<12} | {it['Summary']}")

    print("\n------------------------------------------------------------------")
    print(f"Total Committed Story Points : {total_committed_points} pts")
    print(f"Completed (Done)             : {completed_points} pts ({completed_points/total_committed_points*100:.1f}%)")
    print(f"In Progress                  : {in_progress_points} pts ({in_progress_points/total_committed_points*100:.1f}%)")
    print(f"To Do (Pending)              : {to_do_points} pts ({to_do_points/total_committed_points*100:.1f}%)")
    print("------------------------------------------------------------------")

    # Burndown simulation over 7 days
    days = [0, 1, 2, 3, 4, 5, 6, 7]
    # Ideal linear burndown from 24 to 0
    ideal_burndown = [total_committed_points - (total_committed_points / 7) * d for d in days]
    # Actual simulated burndown
    actual_burndown = [24, 24, 19, 16, 16, 11, 11, 11]

    print("\n[Sprint Daily Burndown Log]")
    print(f"{'Day':<5} | {'Ideal Remaining (pts)':<22} | {'Actual Remaining (pts)':<22}")
    print("-" * 55)
    for d, ideal, actual in zip(days, ideal_burndown, actual_burndown):
        print(f"Day {d:<2} | {ideal:<22.1f} | {actual:<22}")

    # Generate Chart
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(days, ideal_burndown, 'r--', label='Guideline (Ideal Burndown)', linewidth=2)
    ax.plot(days, actual_burndown, 'b-o', label='Actual Remaining Work', linewidth=2.5, markersize=6)
    ax.set_title("Jira Sprint Burndown Chart - SP Sprint 1\nSaveetha School of Engineering | Angulakshmi S (192524402)", fontsize=11, fontweight='bold', pad=12)
    ax.set_xlabel("Sprint Timeline (Days)", fontsize=10, fontweight='bold')
    ax.set_ylabel("Story Points Remaining", fontsize=10, fontweight='bold')
    ax.set_xticks(days)
    ax.set_ylim(0, 28)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right')

    chart_path = os.path.join(output_dir, "burndown_chart.png")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"\nSuccessfully generated Sprint Burndown Chart at: {chart_path}")
    print("==================================================================")

if __name__ == "__main__":
    simulate_scrum_sprint()
