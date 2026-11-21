import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
ax.set_xlim(0, 11)
ax.set_ylim(0, 6.5)
ax.axis('off')

# Title
ax.text(5.5, 6.1, "Git Branching, Merge Conflict & Manual Resolution", 
        ha='center', va='center', fontsize=14, fontweight='bold', color='#1e293b')
ax.text(5.5, 5.7, "Student: Angulakshmi S (192524402) | CSA10 - Software Engineering", 
        ha='center', va='center', fontsize=10, color='#64748b')

# Commit nodes
# C1: Initial
ax.scatter([1.5], [3.5], s=400, color='#3b82f6', zorder=5, edgecolor='black', linewidth=1.5)
ax.text(1.5, 3.5, "C1", ha='center', va='center', color='white', fontweight='bold', fontsize=10)
ax.text(1.5, 2.9, "Initial Commit\n(main)", ha='center', va='top', fontsize=9, fontweight='bold')

# C2: Collaborator on main
ax.scatter([5.0], [4.6], s=400, color='#059669', zorder=5, edgecolor='black', linewidth=1.5)
ax.text(5.0, 4.6, "C2", ha='center', va='center', color='white', fontweight='bold', fontsize=10)
ax.text(5.0, 5.3, "main (Collaborator)\nEdited README line 7", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#047857')

# C3: Feature update branch
ax.scatter([5.0], [2.4], s=400, color='#d97706', zorder=5, edgecolor='black', linewidth=1.5)
ax.text(5.0, 2.4, "C3", ha='center', va='center', color='white', fontweight='bold', fontsize=10)
ax.text(5.0, 1.7, "feature-update (Student)\nEdited README line 7", ha='center', va='top', fontsize=9, fontweight='bold', color='#b45309')

# Conflict zone in the middle
conflict_box = patches.FancyBboxPatch((4.0, 3.2), 2.0, 0.6, boxstyle="round,pad=0.1", ec="#dc2626", fc="#fef2f2", lw=1.5)
ax.add_patch(conflict_box)
ax.text(5.0, 3.5, "CONFLICT!\n<<<<<<< HEAD\n=======\n>>>>>>> main", ha='center', va='center', fontsize=7.5, color='#991b1b', family='monospace')

# C4: Merge commit
ax.scatter([8.5], [2.4], s=450, color='#7c3aed', zorder=5, edgecolor='black', linewidth=1.5)
ax.text(8.5, 2.4, "C4", ha='center', va='center', color='white', fontweight='bold', fontsize=10)
ax.text(8.5, 1.7, "Merge Commit (C4)\n'Resolved merge conflict'\nCombined both changes", ha='center', va='top', fontsize=9, fontweight='bold', color='#6d28d9')

# Edges / Arrows
# C1 -> C2
ax.annotate("", xy=(4.6, 4.5), xytext=(1.9, 3.7), arrowprops=dict(arrowstyle="->", color="#059669", lw=2))
# C1 -> C3
ax.annotate("", xy=(4.6, 2.5), xytext=(1.9, 3.3), arrowprops=dict(arrowstyle="->", color="#d97706", lw=2))
# C3 -> C4
ax.annotate("", xy=(8.05, 2.4), xytext=(5.45, 2.4), arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=2))
# C2 -> C4 (merge arrow)
ax.annotate("", xy=(8.2, 2.7), xytext=(5.3, 4.4), arrowprops=dict(arrowstyle="->", color="#dc2626", lw=2.5, linestyle="--"))

# Legend box
leg_box = patches.FancyBboxPatch((0.5, 0.4), 10.0, 0.7, boxstyle="round,pad=0.1", ec="#94a3b8", fc="#f8fafc", lw=1)
ax.add_patch(leg_box)
ax.text(5.5, 0.75, "Step 1: Branch created -> Step 2: Divergent commits -> Step 3: git merge main causes conflict -> Step 4: Resolve markers & commit C4",
        ha='center', va='center', fontsize=8.5, color='#334155', fontweight='bold')

plt.tight_layout()
out_dir = r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-15-Git-Branches-Merge-Conflicts\diagrams"
os.makedirs(out_dir, exist_ok=True)
img_path = os.path.join(out_dir, "branch_conflict_resolution.png")
plt.savefig(img_path, dpi=300)
plt.close()
print("Saved conflict diagram to", img_path)
