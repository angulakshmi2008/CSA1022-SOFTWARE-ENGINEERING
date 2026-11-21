import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
ax.set_xlim(0, 11)
ax.set_ylim(0, 7)
ax.axis('off')

# Title
ax.text(5.5, 6.6, "Team Project Version Control & Branch Collaboration Architecture", 
        ha='center', va='center', fontsize=13, fontweight='bold', color='#1e293b')
ax.text(5.5, 6.2, "Student: Angulakshmi S (192524402) | Course: CSA10 - Software Engineering", 
        ha='center', va='center', fontsize=9.5, color='#64748b')

# Branches layout
branches = [
    ("main (Team Lead)", 5.2, "#1e40af", "#eff6ff"),
    ("feature-login (Angulakshmi S)", 4.0, "#059669", "#ecfdf5"),
    ("feature-catalog (Student 2)", 2.8, "#d97706", "#fffbeb"),
    ("feature-cart (Student 3)", 1.6, "#7c3aed", "#faf5ff")
]

for label, y, stroke, bg in branches:
    ax.plot([1.0, 10.0], [y, y], color=stroke, lw=2.5, zorder=1)
    ax.text(0.8, y, label, ha='right', va='center', fontsize=9, fontweight='bold', color=stroke)

# Commits on main
# Initial Commit
ax.scatter([1.5], [5.2], s=250, color='#1e40af', zorder=5, edgecolor='black')
ax.text(1.5, 5.5, "Initial\nREADME", ha='center', va='bottom', fontsize=7.5, fontweight='bold')

# Commits on feature-login
ax.scatter([2.8], [4.0], s=250, color='#059669', zorder=5, edgecolor='black')
ax.text(2.8, 3.6, "Add login.py\n(Angulakshmi)", ha='center', va='top', fontsize=7.5, fontweight='bold', color='#047857')
# Fork arrow main -> feature-login
ax.annotate("", xy=(2.6, 4.1), xytext=(1.7, 5.1), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.5))
# PR 1 Merge arrow
ax.scatter([4.0], [5.2], s=280, color='#1e40af', zorder=5, edgecolor='black')
ax.annotate("", xy=(3.9, 5.1), xytext=(3.0, 4.1), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.5))
ax.text(4.0, 5.5, "Merge PR #1\n(feature-login)", ha='center', va='bottom', fontsize=7.5, fontweight='bold')

# Commits on feature-catalog
ax.scatter([4.2], [2.8], s=250, color='#d97706', zorder=5, edgecolor='black')
ax.text(4.2, 2.4, "Add catalog.py\n(Student 2)", ha='center', va='top', fontsize=7.5, fontweight='bold', color='#b45309')
# PR 2 Merge arrow
ax.scatter([5.5], [5.2], s=280, color='#1e40af', zorder=5, edgecolor='black')
ax.annotate("", xy=(5.4, 5.1), xytext=(4.4, 2.9), arrowprops=dict(arrowstyle="->", color="#d97706", lw=1.5))
ax.text(5.5, 5.5, "Merge PR #2\n(feature-catalog)", ha='center', va='bottom', fontsize=7.5, fontweight='bold')

# Commits on feature-cart
ax.scatter([4.8], [1.6], s=250, color='#7c3aed', zorder=5, edgecolor='black')
ax.text(4.8, 1.2, "Add cart.py\n(Student 3)", ha='center', va='top', fontsize=7.5, fontweight='bold', color='#6d28d9')

# Conflict resolution commit on feature-cart
ax.scatter([6.8], [1.6], s=280, color='#dc2626', zorder=5, edgecolor='black')
ax.text(6.8, 1.2, "Resolve Conflict\n(Combined Modules)", ha='center', va='top', fontsize=7.5, fontweight='bold', color='#b91c1c')
# Pull main into cart arrow
ax.annotate("", xy=(6.6, 1.8), xytext=(5.7, 5.0), arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.5, linestyle="--"))

# PR 3 Merge arrow
ax.scatter([8.0], [5.2], s=280, color='#1e40af', zorder=5, edgecolor='black')
ax.annotate("", xy=(7.9, 5.1), xytext=(7.0, 1.8), arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=1.5))
ax.text(8.0, 5.5, "Merge PR #3\n(feature-cart)", ha='center', va='bottom', fontsize=7.5, fontweight='bold')

# Final Docs Commit
ax.scatter([9.2], [5.2], s=280, color='#1e40af', zorder=5, edgecolor='black')
ax.text(9.2, 5.5, "Final\nREADME.md", ha='center', va='bottom', fontsize=7.5, fontweight='bold')

# Legend Info Box
info_box = patches.FancyBboxPatch((0.8, 0.2), 9.4, 0.65, boxstyle="round,pad=0.1", ec="#94a3b8", fc="#f8fafc", lw=1)
ax.add_patch(info_box)
ax.text(5.5, 0.52, "Team Workflow: Branch Isolation -> Peer Code Review -> Sequential PR Merge -> Local Conflict Resolution -> Verified Stable main",
        ha='center', va='center', fontsize=8.5, color='#334155', fontweight='bold')

plt.tight_layout()
out_dir = r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-20-Team-Project-Repository-README\diagrams"
os.makedirs(out_dir, exist_ok=True)
img_path = os.path.join(out_dir, "team_branch_workflow.png")
plt.savefig(img_path, dpi=300)
plt.close()
print("Saved team workflow diagram to", img_path)
