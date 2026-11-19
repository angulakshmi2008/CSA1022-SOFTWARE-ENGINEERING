"""
Experiment 11: Linking Jira Issues with Confluence for Progress Tracking
Student: Angulakshmi S (Reg No: 192524402)
Course: CSA10 - Software Engineering
Course Outcome: CO2

This script simulates the live synchronization between Jira issues and a Confluence
overview page:
1. Ingests Jira LMS tasks from CSV.
2. Computes the live sprint completion percentage and workflow status counts.
3. Renders a graphical progress bar and dashboard card 'output/confluence_progress_tracker.png'.
"""

import os
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def run_progress_tracker():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "config", "lms_jira_issues.csv")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    issues = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            issues.append(row)

    total_issues = len(issues)
    done_count = sum(1 for it in issues if it["Status"] == "Done")
    in_prog_count = sum(1 for it in issues if it["Status"] == "In Progress")
    todo_count = sum(1 for it in issues if it["Status"] == "To Do")

    done_pct = (done_count / total_issues) * 100
    in_prog_pct = (in_prog_count / total_issues) * 100
    todo_pct = (todo_count / total_issues) * 100

    print("==================================================================")
    print("      ATLASSIAN JIRA + CONFLUENCE PROGRESS TRACKING INTEGRATION   ")
    print("==================================================================")
    print("Confluence Space : Library Management System (LMS)")
    print("Confluence Page  : Library Management System Project Overview")
    print("Jira JQL Query   : project = LMS AND type = Task ORDER BY status DESC")
    print("------------------------------------------------------------------")
    print(f"{'Key':<8} | {'Type':<6} | {'Priority':<8} | {'Status':<12} | {'Summary'}")
    print("-" * 70)
    for it in issues:
        print(f"{it['Issue Key']:<8} | {it['Issue Type']:<6} | {it['Priority']:<8} | {it['Status']:<12} | {it['Summary']}")

    print("\n------------------------------------------------------------------")
    print(f"Total Embedded Issues : {total_issues}")
    print(f"Completed (Done)      : {done_count} ({done_pct:.1f}%)")
    print(f"In Progress           : {in_prog_count} ({in_prog_pct:.1f}%)")
    print(f"To Do                 : {todo_count} ({todo_pct:.1f}%)")
    print(f"Overall Progress      : {done_pct:.1f}% COMPLETE")
    print("------------------------------------------------------------------")

    # Render Confluence Dashboard Card Image
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Background card
    card = patches.FancyBboxPatch((0.5, 0.5), 9.0, 7.0, boxstyle="round,pad=0.2,rounding_size=0.2",
                                  facecolor='#FDFEFE', edgecolor='#BDC3C7', linewidth=1.5)
    ax.add_patch(card)

    # Confluence Title Banner
    ax.text(5.0, 7.0, "Confluence Page: Library Management System Project Overview",
            ha='center', va='center', fontsize=11, fontweight='bold', color='#172B4D')
    ax.text(5.0, 6.6, "Live Jira Integration | Saveetha School of Engineering | Angulakshmi S (192524402)",
            ha='center', va='center', fontsize=8.5, color='#5E6C84')

    # Progress bar outline
    ax.text(1.0, 5.8, f"Sprint Delivery Progress: {done_pct:.0f}% Completed ({done_count} of {total_issues} Tasks Done)",
            fontsize=9.5, fontweight='bold', color='#172B4D')
    
    # Base bar (gray)
    bar_bg = patches.Rectangle((1.0, 5.0), 8.0, 0.5, facecolor='#EBECF0', edgecolor='#DFE1E6', linewidth=1)
    ax.add_patch(bar_bg)
    # Done part (green)
    w_done = 8.0 * (done_pct / 100.0)
    bar_done = patches.Rectangle((1.0, 5.0), w_done, 0.5, facecolor='#36B37E', edgecolor='none')
    ax.add_patch(bar_done)
    # In progress part (blue)
    w_prog = 8.0 * (in_prog_pct / 100.0)
    bar_prog = patches.Rectangle((1.0 + w_done, 5.0), w_prog, 0.5, facecolor='#0052CC', edgecolor='none')
    ax.add_patch(bar_prog)

    # Legend
    ax.plot([1.2], [4.4], marker='s', color='#36B37E', markersize=8)
    ax.text(1.4, 4.4, f"Done ({done_count} tasks - {done_pct:.0f}%)", va='center', fontsize=8, color='#172B4D')

    ax.plot([4.0], [4.4], marker='s', color='#0052CC', markersize=8)
    ax.text(4.2, 4.4, f"In Progress ({in_prog_count} task - {in_prog_pct:.0f}%)", va='center', fontsize=8, color='#172B4D')

    ax.plot([7.0], [4.4], marker='s', color='#DFE1E6', markersize=8)
    ax.text(7.2, 4.4, f"To Do ({todo_count} tasks - {todo_pct:.0f}%)", va='center', fontsize=8, color='#172B4D')

    # Embedded Jira Table Header
    ax.plot([1.0, 9.0], [3.8, 3.8], color='#0052CC', lw=1.5)
    ax.text(1.2, 3.5, "Key", fontweight='bold', fontsize=8.5, color='#172B4D')
    ax.text(2.4, 3.5, "Summary", fontweight='bold', fontsize=8.5, color='#172B4D')
    ax.text(6.8, 3.5, "Assignee", fontweight='bold', fontsize=8.5, color='#172B4D')
    ax.text(8.2, 3.5, "Status", fontweight='bold', fontsize=8.5, color='#172B4D')
    ax.plot([1.0, 9.0], [3.3, 3.3], color='#DFE1E6', lw=1.0)

    # Table rows
    y = 2.9
    for it in issues:
        st_color = '#36B37E' if it['Status'] == 'Done' else ('#0052CC' if it['Status'] == 'In Progress' else '#42526E')
        ax.text(1.2, y, it['Issue Key'], fontsize=8, color='#0052CC', fontweight='bold')
        ax.text(2.4, y, it['Summary'], fontsize=8, color='#172B4D')
        ax.text(6.8, y, it['Assignee'], fontsize=8, color='#5E6C84')
        ax.text(8.2, y, it['Status'], fontsize=8, fontweight='bold', color=st_color)
        y -= 0.45

    chart_path = os.path.join(output_dir, "confluence_progress_tracker.png")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"Generated Confluence tracker image at: {chart_path}")
    print("==================================================================")

if __name__ == "__main__":
    run_progress_tracker()
