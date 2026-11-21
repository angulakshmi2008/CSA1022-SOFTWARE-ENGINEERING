import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
ax.set_xlim(0, 11)
ax.set_ylim(0, 6)
ax.axis('off')

# Title
ax.text(5.5, 5.6, "Fork-and-Pull-Request Collaboration Workflow", 
        ha='center', va='center', fontsize=14, fontweight='bold', color='#1e293b')
ax.text(5.5, 5.2, "Student: Angulakshmi S (192524402) | CSA10 - Software Engineering", 
        ha='center', va='center', fontsize=10, color='#64748b')

# Boxes
# 1. Upstream
box_upstream = patches.FancyBboxPatch((0.6, 3.4), 2.8, 1.3, boxstyle="round,pad=0.1", 
                                      ec="#2563eb", fc="#eff6ff", lw=2)
ax.add_patch(box_upstream)
ax.text(2.0, 4.3, "Upstream Repository", ha='center', va='center', fontsize=11, fontweight='bold', color='#1e40af')
ax.text(2.0, 3.8, "(Original Repo)\nmain branch", ha='center', va='center', fontsize=9, color='#1e3a8a')

# 2. Origin (Fork)
box_fork = patches.FancyBboxPatch((7.6, 3.4), 2.8, 1.3, boxstyle="round,pad=0.1", 
                                  ec="#16a34a", fc="#f0fdf4", lw=2)
ax.add_patch(box_fork)
ax.text(9.0, 4.3, "Origin Repository", ha='center', va='center', fontsize=11, fontweight='bold', color='#15803d')
ax.text(9.0, 3.8, "(User's GitHub Fork)\nmain & feature branches", ha='center', va='center', fontsize=9, color='#14532d')

# 3. Local Clone
box_local = patches.FancyBboxPatch((4.1, 0.7), 2.8, 1.5, boxstyle="round,pad=0.1", 
                                   ec="#9333ea", fc="#faf5ff", lw=2)
ax.add_patch(box_local)
ax.text(5.5, 1.8, "Local Workstation", ha='center', va='center', fontsize=11, fontweight='bold', color='#7e22ce')
ax.text(5.5, 1.2, "git checkout -b update-readme\nedit -> commit", ha='center', va='center', fontsize=9, color='#581c87')

# Arrows
# Step 1: Fork
ax.annotate("", xy=(7.5, 4.2), xytext=(3.5, 4.2),
            arrowprops=dict(arrowstyle="->", color="#0284c7", lw=2.5))
ax.text(5.5, 4.45, "1. Fork (GitHub Web)", ha='center', va='center', fontsize=10, fontweight='bold', color='#0284c7')

# Step 2: Clone
ax.annotate("", xy=(5.5, 2.3), xytext=(8.0, 3.3),
            arrowprops=dict(arrowstyle="->", color="#16a34a", lw=2))
ax.text(7.2, 2.7, "2. git clone", ha='center', va='center', fontsize=9, fontweight='bold', color='#16a34a')

# Step 3: Push
ax.annotate("", xy=(8.7, 3.3), xytext=(6.5, 2.3),
            arrowprops=dict(arrowstyle="->", color="#e11d48", lw=2))
ax.text(8.0, 2.2, "3. git push -u origin\nupdate-readme", ha='center', va='center', fontsize=8, fontweight='bold', color='#e11d48')

# Step 4: Open Pull Request
ax.annotate("", xy=(3.5, 3.7), xytext=(7.5, 3.7),
            arrowprops=dict(arrowstyle="->", color="#f59e0b", lw=2.5, linestyle="--"))
ax.text(5.5, 3.35, "4. Create Pull Request (#122481)\n& Review Feedback", ha='center', va='center', fontsize=9, fontweight='bold', color='#d97706')

# Step 5: Merge
ax.text(2.0, 2.6, "5. Upstream Maintainer\nMerges PR into main", ha='center', va='center', fontsize=9, fontweight='bold', color='#1e40af',
        bbox=dict(boxstyle='square,pad=0.3', facecolor='#dbeafe', edgecolor='#93c5fd'))

plt.tight_layout()
out_dir = r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-14-Fork-Pull-Request-Workflow\diagrams"
os.makedirs(out_dir, exist_ok=True)
img_path = os.path.join(out_dir, "fork_pr_workflow.png")
plt.savefig(img_path, dpi=300)
plt.close()
print("Saved diagram to", img_path)
