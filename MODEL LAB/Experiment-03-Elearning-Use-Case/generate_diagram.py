"""
Q3: E-Learning Platform UML Use Case Diagram Generator
Generates high-resolution use_case_diagram.png adhering strictly to UML 2.5 standards:
- System Boundary: E-Learning Platform
- Primary Actors: Student, Instructor, Administrator
- External Supporting Actor: External Payment Gateway
- Associations, <<include>>, and <<extend>> relationships
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_stick_figure(ax, x, y, label, role_color="#1E293B", is_system=False):
    """Draws a standard UML Actor stick figure or external system box."""
    if is_system:
        # External System Actor: Box with <<actor>> / <<system>> stereotype
        box = patches.FancyBboxPatch(
            (x - 0.7, y - 0.5), 1.4, 1.0,
            boxstyle="round,pad=0.1",
            facecolor="#FEF3C7", edgecolor="#D97706", lw=2, zorder=5
        )
        ax.add_patch(box)
        ax.text(x, y + 0.15, "<<system>>\n<<actor>>", ha="center", va="center", fontsize=8, fontweight="bold", color="#B45309", zorder=6)
        ax.text(x, y - 0.25, label, ha="center", va="center", fontsize=9, fontweight="bold", color="#1E293B", zorder=6)
    else:
        # Human Actor Stick Figure
        # Head
        head = plt.Circle((x, y + 0.45), 0.18, facecolor="#F1F5F9", edgecolor=role_color, lw=2, zorder=5)
        ax.add_patch(head)
        # Body
        ax.plot([x, x], [y + 0.27, y - 0.15], color=role_color, lw=2.2, zorder=5)
        # Arms
        ax.plot([x - 0.35, x + 0.35], [y + 0.12, y + 0.12], color=role_color, lw=2.2, zorder=5)
        # Legs
        ax.plot([x, x - 0.25], [y - 0.15, y - 0.55], color=role_color, lw=2.2, zorder=5)
        ax.plot([x, x + 0.25], [y - 0.15, y - 0.55], color=role_color, lw=2.2, zorder=5)
        # Actor Label
        ax.text(x, y - 0.75, label, ha="center", va="top", fontsize=9.5, fontweight="bold", color=role_color, zorder=6)

def draw_use_case(ax, x, y, w, h, text, color="#EFF6FF", border="#3B82F6", is_included_or_extended=False):
    """Draws a standard UML Use Case ellipse."""
    ellipse = patches.Ellipse(
        (x, y), w, h,
        facecolor=color, edgecolor=border,
        lw=1.8 if not is_included_or_extended else 1.5,
        linestyle="-" if not is_included_or_extended else "--",
        zorder=4
    )
    ax.add_patch(ellipse)
    ax.text(x, y, text, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#1E293B", zorder=5)

def render():
    fig, ax = plt.subplots(figsize=(15, 11), dpi=300)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")

    # 1. System Boundary Box
    system_rect = patches.Rectangle(
        (2.8, 0.6), 8.8, 9.8,
        facecolor="#F8FAFC", edgecolor="#475569", lw=2.2, linestyle="-", zorder=1
    )
    ax.add_patch(system_rect)
    # System Title
    ax.text(7.2, 10.15, "System Boundary: E-Learning Platform", ha="center", va="center", 
            fontsize=12, fontweight="bold", color="#0F172A",
            bbox=dict(boxstyle="square,pad=0.4", facecolor="#E2E8F0", edgecolor="#94A3B8", lw=1.2), zorder=2)

    # 2. Actors Positions
    # Left primary actors
    draw_stick_figure(ax, 1.2, 8.5, "Student", role_color="#1D4ED8")
    draw_stick_figure(ax, 1.2, 4.8, "Instructor", role_color="#047857")
    draw_stick_figure(ax, 1.2, 1.8, "Administrator", role_color="#7C2D12")
    # Right external supporting actor
    draw_stick_figure(ax, 13.2, 6.8, "External Payment\nGateway", is_system=True)

    # 3. Use Cases Definitions (x, y, w, h, label, bg, border, is_sub)
    use_cases = {
        # Student Use Cases
        "browse":     (4.8, 9.4, 2.8, 0.75, "Browse Course\nCatalogue", "#EFF6FF", "#2563EB", False),
        "enrol":      (4.8, 7.8, 2.6, 0.75, "Enrol in Course", "#EFF6FF", "#2563EB", False),
        "watch":      (4.8, 6.4, 2.6, 0.75, "Watch Lectures", "#EFF6FF", "#2563EB", False),
        "quiz":       (4.8, 5.0, 2.6, 0.75, "Attempt Quizzes", "#EFF6FF", "#2563EB", False),
        "assign":     (4.8, 3.6, 2.8, 0.75, "Submit Assignments", "#EFF6FF", "#2563EB", False),
        "cert":       (4.8, 2.2, 3.0, 0.80, "Download Completion\nCertificate", "#EFF6FF", "#2563EB", False),

        # Included / Extended Use Cases
        "payment":    (8.8, 6.8, 2.6, 0.75, "Process Payment", "#FEF3C7", "#D97706", False),
        "coupon":     (8.8, 8.4, 2.8, 0.75, "Apply Discount\nCoupon", "#F0FDF4", "#16A34A", True),
        "forum":      (8.8, 5.2, 2.8, 0.75, "Ask Question in\nDiscussion Forum", "#F0FDF4", "#16A34A", True),
        "verify_comp":(8.8, 2.2, 2.8, 0.75, "Verify Course\nRequirements", "#EFF6FF", "#6366F1", True),

        # Instructor Use Cases
        "upload":     (7.2, 4.0, 2.8, 0.75, "Upload Lecture\nVideos / Courses", "#ECFDF5", "#059669", False),
        "create_quiz":(7.2, 2.9, 2.6, 0.75, "Create Quizzes", "#ECFDF5", "#059669", False),

        # Admin Use Cases
        "users":      (7.2, 1.8, 2.5, 0.70, "Manage Users", "#FFFBEB", "#B45309", False),
        "approve":    (7.2, 0.9, 2.8, 0.70, "Approve New Courses", "#FFFBEB", "#B45309", False),
    }

    for key, (ux, uy, uw, uh, text, bg, border, is_sub) in use_cases.items():
        draw_use_case(ax, ux, uy, uw, uh, text, color=bg, border=border, is_included_or_extended=is_sub)

    # 4. Draw Actor Associations (Solid Lines)
    # Student Associations
    student_pos = (1.5, 8.5)
    for target in ["browse", "enrol", "watch", "quiz", "assign", "cert"]:
        tx, ty, tw, th = use_cases[target][:4]
        ax.plot([student_pos[0], tx - tw/2], [student_pos[1], ty], color="#1D4ED8", lw=1.6, zorder=3)

    # Instructor Associations
    instr_pos = (1.5, 4.8)
    for target in ["upload", "create_quiz"]:
        tx, ty, tw, th = use_cases[target][:4]
        ax.plot([instr_pos[0], tx - tw/2], [instr_pos[1], ty], color="#047857", lw=1.6, zorder=3)

    # Admin Associations
    admin_pos = (1.5, 1.8)
    for target in ["users", "approve"]:
        tx, ty, tw, th = use_cases[target][:4]
        ax.plot([admin_pos[0], tx - tw/2], [admin_pos[1], ty], color="#7C2D12", lw=1.6, zorder=3)

    # External Payment Gateway Association
    gw_pos = (12.5, 6.8)
    px, py, pw, ph = use_cases["payment"][:4]
    ax.plot([gw_pos[0], px + pw/2], [gw_pos[1], py], color="#B45309", lw=1.8, zorder=3)

    # 5. Draw <<include>> and <<extend>> Relationships (Dashed Directed Arrows)
    # Enrol --<<include>>--> Process Payment
    ax.annotate(
        "", xy=(use_cases["payment"][0] - use_cases["payment"][2]/2, use_cases["payment"][1] + 0.15),
        xytext=(use_cases["enrol"][0] + use_cases["enrol"][2]/2, use_cases["enrol"][1] - 0.1),
        arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=1.8, linestyle="dashed"),
        zorder=3
    )
    ax.text(6.6, 7.55, "<<include>>\n(for paid courses)", ha="center", va="center", fontsize=8, fontweight="bold", color="#B45309",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFBEB", edgecolor="#FDE68A"))

    # Download Certificate --<<include>>--> Verify Course Requirements
    ax.annotate(
        "", xy=(use_cases["verify_comp"][0] - use_cases["verify_comp"][2]/2, use_cases["verify_comp"][1]),
        xytext=(use_cases["cert"][0] + use_cases["cert"][2]/2, use_cases["cert"][1]),
        arrowprops=dict(arrowstyle="-|>", color="#4F46E5", lw=1.8, linestyle="dashed"),
        zorder=3
    )
    ax.text(6.8, 2.45, "<<include>>", ha="center", va="center", fontsize=8, fontweight="bold", color="#4338CA",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#EEF2FF", edgecolor="#C7D2FE"))

    # Apply Discount Coupon --<<extend>>--> Enrol in Course
    # (Points from Extension use case to Base use case)
    ax.annotate(
        "", xy=(use_cases["enrol"][0] + use_cases["enrol"][2]/2, use_cases["enrol"][1] + 0.2),
        xytext=(use_cases["coupon"][0] - use_cases["coupon"][2]/2, use_cases["coupon"][1] - 0.2),
        arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=1.8, linestyle="dashed"),
        zorder=3
    )
    ax.text(6.7, 8.45, "<<extend>>\n[has promo code]", ha="center", va="center", fontsize=8, fontweight="bold", color="#15803D",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#F0FDF4", edgecolor="#BBF7D0"))

    # Ask Question --<<extend>>--> Watch Lectures
    ax.annotate(
        "", xy=(use_cases["watch"][0] + use_cases["watch"][2]/2, use_cases["watch"][1] - 0.15),
        xytext=(use_cases["forum"][0] - use_cases["forum"][2]/2, use_cases["forum"][1] + 0.15),
        arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=1.8, linestyle="dashed"),
        zorder=3
    )
    ax.text(6.8, 5.9, "<<extend>>\n[posts doubt]", ha="center", va="center", fontsize=8, fontweight="bold", color="#15803D",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#F0FDF4", edgecolor="#BBF7D0"))

    # Legend Card
    legend_text = (
        "UML Notation Legend:\n"
        "─── Solid Line: Actor Association\n"
        "- - > Dashed Arrow: Dependency (<<include>> / <<extend>>)\n"
        "• <<include>>: Mandatory sub-flow executed every time base use case runs\n"
        "• <<extend>>: Optional sub-flow executing only under specific condition\n"
        "• External Actor: Represented outside system boundary with <<system>> stereotype"
    )
    ax.text(0.3, 0.5, legend_text, fontsize=8, va="bottom", ha="left",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#F1F5F9", edgecolor="#CBD5E1", lw=1.2), zorder=6)

    ax.set_xlim(0.0, 14.5)
    ax.set_ylim(0.0, 10.8)
    ax.axis("off")
    plt.tight_layout()

    out_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "use_case_diagram.png")
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"[+] Rendered UML Use Case diagram to: {out_file}")

if __name__ == "__main__":
    render()
