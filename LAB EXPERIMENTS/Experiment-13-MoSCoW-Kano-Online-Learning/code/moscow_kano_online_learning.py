"""
Experiment 13: Prioritizing Online Learning Platform Requirements using MoSCoW and Kano in Jira
Author: Angulakshmi S (Reg No: 192524402)
Department of Computer Science and Engineering
Saveetha School of Engineering, SIMATS
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Data representation of the 6 Online Learning Platform requirements
REQUIREMENTS = [
    {
        "id": "OLP-1",
        "title": "Course Enrollment and Registration",
        "moscow": "Must Have",
        "kano": "Basic",
        "story_points": 5,
        "sprint": "Sprint 1 (MVP)",
        "business_value": 95,
        "satisfaction_impact": "High Dissatisfaction if Absent (Must-be)",
        "justification": "Fundamental platform entry point; users cannot access courses without identity and enrollment."
    },
    {
        "id": "OLP-2",
        "title": "Video Lecture Streaming",
        "moscow": "Must Have",
        "kano": "Performance",
        "story_points": 8,
        "sprint": "Sprint 1 (MVP)",
        "business_value": 90,
        "satisfaction_impact": "Linear Satisfaction with video quality & speed",
        "justification": "Primary learning delivery mechanism; core value proposition of an e-learning platform."
    },
    {
        "id": "OLP-3",
        "title": "Interactive Quizzes and Assignments",
        "moscow": "Should Have",
        "kano": "Performance",
        "story_points": 5,
        "sprint": "Sprint 1 (Targeted)",
        "business_value": 75,
        "satisfaction_impact": "Directly enhances assessment and learning validation",
        "justification": "Critical pedagogical reinforcement; highly expected for academic credibility."
    },
    {
        "id": "OLP-4",
        "title": "Progress Tracking Dashboard",
        "moscow": "Should Have",
        "kano": "Performance",
        "story_points": 5,
        "sprint": "Sprint 1 (Targeted)",
        "business_value": 70,
        "satisfaction_impact": "Enhances learner motivation and course completion rates",
        "justification": "Essential self-monitoring tool for learners to view completion status and streaks."
    },
    {
        "id": "OLP-5",
        "title": "Peer-to-Peer Discussion Forums",
        "moscow": "Could Have",
        "kano": "Excitement",
        "story_points": 5,
        "sprint": "Sprint 2 (Enhancement)",
        "business_value": 50,
        "satisfaction_impact": "Unexpected delight, fosters organic student community",
        "justification": "Collaborative social layer; valuable differentiator but not required for Day 1 launch."
    },
    {
        "id": "OLP-6",
        "title": "Certificate Generation",
        "moscow": "Could Have",
        "kano": "Excitement",
        "story_points": 3,
        "sprint": "Sprint 2 (Enhancement)",
        "business_value": 45,
        "satisfaction_impact": "High celebratory reward upon completion; drives sharing",
        "justification": "Post-completion credentialing; can be issued retroactively upon Sprint 2 rollout."
    }
]

def generate_report():
    print("=" * 85)
    print("EXPERIMENT 13: ONLINE LEARNING PLATFORM REQUIREMENTS PRIORITIZATION")
    print("STUDENT: Angulakshmi S | REGISTER NUMBER: 192524402")
    print("=" * 85)
    print("\n[1] REQUIREMENT ANALYSIS MATRIX (MoSCoW vs. KANO):\n")
    print(f"{'Key':<7} | {'Requirement Title':<38} | {'MoSCoW':<12} | {'Kano':<12} | {'SP':<3} | {'Sprint'}")
    print("-" * 85)
    for r in REQUIREMENTS:
        print(f"{r['id']:<7} | {r['title']:<38} | {r['moscow']:<12} | {r['kano']:<12} | {r['story_points']:<3} | {r['sprint']}")
    
    print("\n" + "=" * 85)
    print("[2] SPRINT PLANNING BREAKDOWN:")
    sprint_1_points = sum(r['story_points'] for r in REQUIREMENTS if "Sprint 1" in r['sprint'])
    sprint_2_points = sum(r['story_points'] for r in REQUIREMENTS if "Sprint 2" in r['sprint'])
    
    print(f"\n- SPRINT 1 (MVP Delivery - Must & High Shoulds):")
    for r in REQUIREMENTS:
        if "Sprint 1" in r['sprint']:
            print(f"  * [{r['id']}] {r['title']} ({r['story_points']} pts) -> MoSCoW: {r['moscow']}, Kano: {r['kano']}")
    print(f"  Total Sprint 1 Story Points: {sprint_1_points} pts")

    print(f"\n- SPRINT 2 (Enhancement & Delight - Coulds):")
    for r in REQUIREMENTS:
        if "Sprint 2" in r['sprint']:
            print(f"  * [{r['id']}] {r['title']} ({r['story_points']} pts) -> MoSCoW: {r['moscow']}, Kano: {r['kano']}")
    print(f"  Total Sprint 2 Story Points: {sprint_2_points} pts")
    
    print("\n" + "=" * 85)
    print("[3] DUAL-FRAMEWORK STRATEGY SUMMARY:")
    print("  * MoSCoW governs immediate release feasibility (Must = Non-negotiable, Should = High value).")
    print("  * Kano governs user satisfaction and adoption dynamics (Basic = Baseline trust, Performance = Quality, Excitement = Delighters).")
    print("  * The unified roadmap ensures the MVP is reliable (Basic), competitive (Performance), and primed for viral retention (Excitement).")
    print("=" * 85)

def plot_matrix(output_path):
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    
    # Coordinate grid for MoSCoW vs Kano
    # Kano X-axis: Basic (1), Performance (2), Excitement (3)
    # MoSCoW Y-axis: Could (1), Should (2), Must (3)
    
    ax.set_xlim(0.5, 3.5)
    ax.set_ylim(0.5, 3.5)
    
    # Draw background zones
    ax.axhspan(2.5, 3.5, color='#e8f4f8', alpha=0.5, label='Must-Have Zone (Release Critical)')
    ax.axhspan(1.5, 2.5, color='#fff9e6', alpha=0.5, label='Should-Have Zone (High Impact)')
    ax.axhspan(0.5, 1.5, color='#f2f4f8', alpha=0.5, label='Could-Have Zone (Delighters)')
    
    # Grid lines
    ax.axvline(1.5, color='#cbd5e1', linestyle='--', linewidth=1)
    ax.axvline(2.5, color='#cbd5e1', linestyle='--', linewidth=1)
    ax.axhline(1.5, color='#cbd5e1', linestyle='--', linewidth=1)
    ax.axhline(2.5, color='#cbd5e1', linestyle='--', linewidth=1)
    
    kano_map = {"Basic": 1.0, "Performance": 2.0, "Excitement": 3.0}
    moscow_map = {"Could Have": 1.0, "Should Have": 2.0, "Must Have": 3.0}
    
    # Items with slight offsets to avoid overlap
    coords = [
        ("OLP-1", 1.0, 3.0, "Course Enrollment\n& Registration", "#dc2626"),
        ("OLP-2", 2.0, 3.0, "Video Lecture\nStreaming", "#dc2626"),
        ("OLP-3", 1.85, 2.0, "Interactive Quizzes\n& Assignments", "#ea580c"),
        ("OLP-4", 2.15, 2.0, "Progress Tracking\nDashboard", "#ea580c"),
        ("OLP-5", 2.85, 1.0, "Discussion\nForums", "#0284c7"),
        ("OLP-6", 3.15, 1.0, "Certificate\nGeneration", "#0284c7")
    ]
    
    for key, x, y, label, col in coords:
        ax.scatter(x, y, color=col, s=280, zorder=5, edgecolor='black', linewidth=1.5)
        ax.text(x, y + 0.16, f"{key}\n{label}", ha='center', va='bottom', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=col, alpha=0.9))
        
    ax.set_xticks([1.0, 2.0, 3.0])
    ax.set_xticklabels(['Basic (Must-be)', 'Performance (One-dimensional)', 'Excitement (Attractive)'], fontsize=11, fontweight='bold')
    
    ax.set_yticks([1.0, 2.0, 3.0])
    ax.set_yticklabels(['Could Have', 'Should Have', 'Must Have'], fontsize=11, fontweight='bold')
    
    ax.set_xlabel('Kano Model Category (Customer Satisfaction Impact)', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_ylabel('MoSCoW Priority Category (Release Necessity)', fontsize=12, fontweight='bold', labelpad=10)
    
    ax.set_title('Online Learning Platform – MoSCoW & Kano Prioritization Matrix\nStudent: Angulakshmi S (192524402) | CSA10 Software Engineering',
                 fontsize=12, fontweight='bold', pad=15)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[+] Prioritization Matrix chart generated: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(base_dir, ".."))
    out_dir = os.path.join(exp_dir, "output")
    os.makedirs(out_dir, exist_ok=True)
    
    matrix_img = os.path.join(out_dir, "moscow_kano_olp_matrix.png")
    plot_matrix(matrix_img)
    
    report_file = os.path.join(out_dir, "run_output.txt")
    import sys
    orig_stdout = sys.stdout
    with open(report_file, "w", encoding="utf-8") as f:
        sys.stdout = f
        generate_report()
    sys.stdout = orig_stdout
    generate_report()
    print(f"[+] Output log saved: {report_file}")
