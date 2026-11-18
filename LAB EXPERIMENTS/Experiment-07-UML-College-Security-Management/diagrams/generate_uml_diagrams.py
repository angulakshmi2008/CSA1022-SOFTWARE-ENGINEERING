import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 14)
    ax.axis('off')

    def draw_class(x, y, w, h, name, attrs, methods, bg='#F9EBEA', border='#922B21'):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                      facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        ax.plot([x, x + w], [y + h - 0.7, y + h - 0.7], color=border, linewidth=1.2)
        ax.text(x + w/2, y + h - 0.45, name, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#641E16')
        ay = y + h - 1.0
        for att in attrs:
            ax.text(x + 0.2, ay, att, fontsize=7.5, va='top', family='monospace')
            ay -= 0.35
        div_y = y + h - 0.7 - len(attrs)*0.35 - 0.1
        ax.plot([x, x + w], [div_y, div_y], color=border, linewidth=1.0)
        my = div_y - 0.2
        for m in methods:
            ax.text(x + 0.2, my, m, fontsize=7.5, va='top', family='monospace')
            my -= 0.35

    # Top row: Administrator (left), SecurityPersonnel (middle), CampusLocation (right)
    draw_class(0.6, 9.0, 4.2, 3.6, "Administrator",
               ["- adminId: int", "- username: String", "- password: String"],
               ["+ assignDuty(): void", "+ approveLeave(): void", "+ generateReports(): void"])

    draw_class(5.8, 8.8, 4.6, 4.2, "SecurityPersonnel",
               ["- securityId: int", "- name: String", "- phone: String", "- designation: String", "- basicSalary: double"],
               ["+ viewSchedule(): List", "+ applyLeave(): void", "+ recordAttendance(): void"],
               bg='#EAF2F8', border='#2471A3')

    draw_class(11.4, 9.2, 4.0, 3.2, "CampusLocation",
               ["- locationId: int", "- buildingName: String", "- gateNo: int", "- isMonitored: bool"],
               ["+ getLocationInfo(): String"],
               bg='#E8F8F5', border='#117A65')

    # Middle row: DutySchedule (left), Attendance (middle), Leave (right)
    draw_class(0.6, 4.2, 4.2, 3.8, "DutySchedule",
               ["- dutyId: int", "- date: String", "- startTime: String", "- endTime: String", "- status: String"],
               ["+ assignDuty(): void", "+ updateStatus(): void"],
               bg='#FEF9E7', border='#B7950B')

    draw_class(5.8, 4.4, 4.6, 3.4, "Attendance",
               ["- attendanceId: int", "- securityId: int", "- date: String", "- checkIn: String", "- checkOut: String"],
               ["+ recordAttendance(): void"],
               bg='#F4F6F7', border='#5D6D7E')

    draw_class(11.4, 4.4, 4.0, 3.4, "Leave",
               ["- leaveId: int", "- securityId: int", "- leaveDate: String", "- reason: String", "- status: String"],
               ["+ applyLeave(): void", "+ approve(): void"],
               bg='#FDEDEC', border='#A93226')

    # Bottom row: Salary (middle), AccountsOfficer (right)
    draw_class(5.8, 0.5, 4.6, 3.2, "Salary",
               ["- salaryId: int", "- basicSalary: double", "- totalDuties: int", "- leaveCount: int", "- finalSalary: double"],
               ["+ calculateSalary(): double", "+ printPayslip(): void"],
               bg='#E8F6F3', border='#16A085')

    draw_class(11.4, 0.5, 4.0, 2.6, "AccountsOfficer",
               ["- officerId: int", "- name: String"],
               ["+ processSalaries(): void", "+ generateReport(): void"],
               bg='#F5EEF8', border='#884EA0')

    # Connectors
    # Admin to DutySchedule
    ax.plot([2.7, 2.7], [9.0, 8.0], color='#2C3E50', lw=1.5)
    ax.text(2.9, 8.5, "1 to *", fontsize=8)

    # SecurityPersonnel to DutySchedule
    ax.plot([5.8, 4.8], [10.0, 6.0], color='#2C3E50', lw=1.5)

    # DutySchedule to CampusLocation
    ax.plot([4.8, 11.4], [7.0, 9.8], color='#2C3E50', lw=1.2, linestyle=':')

    # SecurityPersonnel to Attendance
    ax.plot([8.1, 8.1], [8.8, 7.8], color='#2C3E50', lw=1.5)
    ax.text(8.3, 8.3, "1 to *", fontsize=8)

    # SecurityPersonnel to Leave
    ax.plot([10.4, 11.4], [10.0, 6.5], color='#2C3E50', lw=1.5)
    ax.text(10.8, 8.4, "1 to *", fontsize=8)

    # SecurityPersonnel to Salary
    ax.plot([8.1, 8.1], [4.4, 3.7], color='#2C3E50', lw=1.5)
    ax.text(8.3, 4.0, "1 to 1..*", fontsize=8)

    # AccountsOfficer to Salary
    ax.plot([11.4, 10.4], [1.8, 1.8], color='#2C3E50', lw=1.5)

    plt.title("UML Class Diagram: College Security Management System\nSaveetha School of Engineering | CSA10 | Angulakshmi S (192524402)",
              fontsize=13, fontweight='bold', pad=15, color='#2C3E50')
    plt.tight_layout()
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-07-UML-College-Security-Management\diagrams\class_diagram.png", dpi=300)
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-07-UML-College-Security-Management\diagrams\class_diagram.svg")
    plt.close()
    print("Security Class diagram generated.")

def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(12, 9), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # System boundary
    rect = patches.Rectangle((3.8, 0.8), 6.4, 10.4, facecolor='#FDFEFE', edgecolor='#34495E', linewidth=2, linestyle='--')
    ax.add_patch(rect)
    ax.text(7.0, 10.8, "College Security Management System", ha='center', fontsize=12, fontweight='bold', color='#2C3E50')

    ucs = [
        ("Login / Authentication", 9.8),
        ("Assign Duty & Location Shifts", 8.6),
        ("View Duty Schedule", 7.4),
        ("Record Attendance (Check In/Out)", 6.2),
        ("Apply for Leave", 5.0),
        ("Approve / Reject Leave", 3.8),
        ("Calculate Monthly Salary", 2.6),
        ("Generate Salary & Audit Reports", 1.4)
    ]

    for text, y in ucs:
        ell = patches.Ellipse((7.0, y), 4.4, 0.8, facecolor='#FEF9E7', edgecolor='#D4AC0D', linewidth=1.5)
        ax.add_patch(ell)
        ax.text(7.0, y, text, ha='center', va='center', fontsize=9, fontweight='bold', color='#7D6608')

    def draw_actor(x, y, name, color='#2471A3'):
        c = patches.Circle((x, y), 0.25, facecolor='#EBF5FB', edgecolor=color, lw=1.5)
        ax.add_patch(c)
        ax.plot([x, x], [y - 0.25, y - 0.8], color=color, lw=1.8)
        ax.plot([x - 0.35, x + 0.35], [y - 0.45, y - 0.45], color=color, lw=1.8)
        ax.plot([x, x - 0.3], [y - 0.8, y - 1.3], color=color, lw=1.8)
        ax.plot([x, x + 0.3], [y - 0.8, y - 1.3], color=color, lw=1.8)
        ax.text(x, y - 1.6, name, ha='center', fontsize=9.5, fontweight='bold', color=color)

    draw_actor(1.8, 8.5, "Administrator", '#922B21')
    draw_actor(12.2, 6.0, "Security Personnel", '#2471A3')
    draw_actor(1.8, 2.8, "Accounts Officer", '#117A65')

    # Connections
    # Admin
    for y in [9.8, 8.6, 3.8, 1.4]:
        ax.plot([2.1, 4.8], [8.0, y], color='#7F8C8D', lw=1.2)

    # Security Personnel
    for y in [9.8, 7.4, 6.2, 5.0]:
        ax.plot([11.8, 9.2], [5.5, y], color='#7F8C8D', lw=1.2)

    # Accounts Officer
    for y in [9.8, 2.6, 1.4]:
        ax.plot([2.1, 4.8], [2.3, y], color='#7F8C8D', lw=1.2)

    plt.title("UML Use Case Diagram: College Security Management System\nSaveetha School of Engineering | CSA10 | Angulakshmi S (192524402)",
              fontsize=13, fontweight='bold', pad=15, color='#2C3E50')
    plt.tight_layout()
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-07-UML-College-Security-Management\diagrams\use_case_diagram.png", dpi=300)
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-07-UML-College-Security-Management\diagrams\use_case_diagram.svg")
    plt.close()
    print("Security Use Case diagram generated.")

def generate_activity_diagram():
    fig, ax = plt.subplots(figsize=(8, 12), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')

    def draw_action(y, text, bg='#E8F8F5', border='#117A65'):
        r = patches.FancyBboxPatch((2.0, y - 0.35), 6.0, 0.7, boxstyle="round,pad=0.2,rounding_size=0.35",
                                   facecolor=bg, edgecolor=border, lw=1.5)
        ax.add_patch(r)
        ax.text(5.0, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0E6251')

    def draw_arrow(y1, y2, x=5.0):
        ax.annotate('', xy=(x, y2), xytext=(x, y1),
                    arrowprops=dict(facecolor='#2C3E50', edgecolor='#2C3E50', width=1.5, headwidth=6, headlength=6))

    # Initial Node
    c = patches.Circle((5.0, 13.2), 0.25, facecolor='#2C3E50', edgecolor='#2C3E50')
    ax.add_patch(c)
    draw_arrow(12.95, 12.45)

    draw_action(12.1, "1. Login to Security Management Portal")
    draw_arrow(11.75, 11.05)

    draw_action(10.7, "2. Admin Allocates Duty Shift & Campus Location")
    draw_arrow(10.35, 9.65)

    draw_action(9.3, "3. Guard Views Duty Schedule & Records Check-In")
    draw_arrow(8.95, 8.25)

    draw_action(7.9, "4. Guard Performs Campus Patrol & Shift Duties")
    draw_arrow(7.55, 6.85)

    # Decision: Leave Applied?
    d = patches.Polygon([[5.0, 6.85], [6.5, 6.25], [5.0, 5.65], [3.5, 6.25]], facecolor='#FDEDEC', edgecolor='#C0392B', lw=1.5)
    ax.add_patch(d)
    ax.text(5.0, 6.25, "Leave\nApplied?", ha='center', va='center', fontsize=8, fontweight='bold', color='#78281F')

    # Leave flow
    ax.plot([6.5, 8.8, 8.8], [6.25, 6.25, 5.3], color='#C0392B', lw=1.2)
    ax.text(7.2, 6.4, "[Yes]", fontsize=8, fontweight='bold', color='#C0392B')
    r_leave = patches.FancyBboxPatch((7.6, 4.6), 2.2, 0.7, boxstyle="round,pad=0.1", facecolor='#FADBD8', edgecolor='#C0392B', lw=1.2)
    ax.add_patch(r_leave)
    ax.text(8.7, 4.95, "Admin Reviews &\nApproves/Rejects", ha='center', va='center', fontsize=7.5, fontweight='bold')
    ax.plot([8.7, 8.7, 5.0], [4.6, 3.8, 3.8], color='#C0392B', lw=1.2)

    # No leave
    draw_arrow(5.65, 4.85)
    ax.text(5.15, 5.25, "[No]", fontsize=8, fontweight='bold', color='#117A65')

    draw_action(4.5, "5. Guard Completes Shift & Records Check-Out")
    draw_arrow(4.15, 3.45)

    draw_action(3.1, "6. Accounts Officer Calculates Monthly Salary")
    draw_arrow(2.75, 2.05)

    draw_action(1.7, "7. Generate Salary Payslip & Disburse Pay")
    draw_arrow(1.35, 0.75)

    # Final Node
    c_out = patches.Circle((5.0, 0.5), 0.25, facecolor='none', edgecolor='#2C3E50', lw=1.8)
    c_in = patches.Circle((5.0, 0.5), 0.14, facecolor='#2C3E50')
    ax.add_patch(c_out); ax.add_patch(c_in)

    plt.title("UML Activity Diagram: College Security Workflow\nSaveetha School of Engineering | CSA10 | Angulakshmi S (192524402)",
              fontsize=12, fontweight='bold', pad=15, color='#2C3E50')
    plt.tight_layout()
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-07-UML-College-Security-Management\diagrams\activity_diagram.png", dpi=300)
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-07-UML-College-Security-Management\diagrams\activity_diagram.svg")
    plt.close()
    print("Security Activity diagram generated.")

if __name__ == "__main__":
    generate_class_diagram()
    generate_use_case_diagram()
    generate_activity_diagram()
