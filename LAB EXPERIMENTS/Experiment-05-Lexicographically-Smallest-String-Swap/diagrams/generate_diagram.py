import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_flowchart():
    fig, ax = plt.subplots(figsize=(10, 14), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Color palette
    c_start = '#D4EFDF'
    c_border_start = '#27AE60'
    c_io = '#FCF3CF'
    c_border_io = '#F39C12'
    c_assign = '#D6EAF8'
    c_border_assign = '#2980B9'
    c_decision = '#FDEDEC'
    c_border_decision = '#C0392B'
    c_arrow = '#2C3E50'

    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=c_arrow, edgecolor=c_arrow, width=1.5, headwidth=7, headlength=7))
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx + 0.15, my, label, fontsize=9, fontweight='bold', color='#2C3E50')

    # 1. Start (Oval) at (6, 15.2)
    start_p = patches.FancyBboxPatch((4.5, 14.8), 3.0, 0.7, boxstyle="round,pad=0.2,rounding_size=0.35",
                                     facecolor=c_start, edgecolor=c_border_start, linewidth=2)
    ax.add_patch(start_p)
    ax.text(6.0, 15.15, "Start", ha='center', va='center', fontsize=11, fontweight='bold')

    draw_arrow(6.0, 14.8, 6.0, 14.1)

    # 2. Input str, ch1, ch2 (Parallelogram)
    in_poly = patches.Polygon([[3.2, 13.1], [8.8, 13.1], [8.3, 14.1], [2.7, 14.1]],
                              facecolor=c_io, edgecolor=c_border_io, linewidth=2)
    ax.add_patch(in_poly)
    ax.text(5.75, 13.75, "Input: GET str, ch1, ch2", ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(5.75, 13.35, "e.g., str='ccad', ch1='c', ch2='a'", ha='center', va='center', fontsize=8.5, fontstyle='italic')

    draw_arrow(6.0, 13.1, 6.0, 12.3)

    # 3. Assignment: i <- 1, n <- Length_Of(str)
    as1_patch = patches.Rectangle((3.5, 11.4), 5.0, 0.9,
                                  facecolor=c_assign, edgecolor=c_border_assign, linewidth=2)
    ax.add_patch(as1_patch)
    ax.text(6.0, 12.0, "i ← 1", ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(6.0, 11.6, "n ← Length_Of(str)", ha='center', va='center', fontsize=10, fontweight='bold')

    draw_arrow(6.0, 11.4, 6.0, 10.6)

    # 4. Loop Condition: i <= n (Diamond)
    cond1 = patches.Polygon([[6.0, 10.6], [7.8, 9.7], [6.0, 8.8], [4.2, 9.7]],
                            facecolor=c_decision, edgecolor=c_border_decision, linewidth=2)
    ax.add_patch(cond1)
    ax.text(6.0, 9.7, "i <= n ?", ha='center', va='center', fontsize=10, fontweight='bold')

    # If NO (i > n) -> exit loop to Output
    # Arrow from (7.8, 9.7) -> right to x=10.2 -> down to y=2.6
    ax.plot([7.8, 10.2], [9.7, 9.7], color=c_arrow, linewidth=1.5)
    ax.plot([10.2, 10.2], [9.7, 2.6], color=c_arrow, linewidth=1.5)
    draw_arrow(10.2, 2.6, 7.8, 2.6)
    ax.text(8.3, 9.9, "No (Exit)", fontsize=9, fontweight='bold', color='#C0392B')

    # If YES -> Enter loop body
    draw_arrow(6.0, 8.8, 6.0, 7.9, label="Yes")

    # 5. Decision 1: str[i] == ch1 ?
    cond2 = patches.Polygon([[6.0, 7.9], [7.7, 7.1], [6.0, 6.3], [4.3, 7.1]],
                            facecolor=c_decision, edgecolor=c_border_decision, linewidth=2)
    ax.add_patch(cond2)
    ax.text(6.0, 7.1, "str[i] == ch1 ?", ha='center', va='center', fontsize=9.5, fontweight='bold')

    # If YES -> replace with ch2: str[i] <- ch2
    # Arrow to left: (4.3, 7.1) -> (2.6, 7.1)
    draw_arrow(4.3, 7.1, 2.8, 7.1, label="Yes")
    rep1_patch = patches.Rectangle((0.8, 6.6), 2.0, 0.9, facecolor=c_assign, edgecolor=c_border_assign, linewidth=1.5)
    ax.add_patch(rep1_patch)
    ax.text(1.8, 7.05, "str[i] ← ch2", ha='center', va='center', fontsize=9, fontweight='bold')

    # From rep1 down to join at y=4.4
    ax.plot([1.8, 1.8], [6.6, 4.4], color=c_arrow, linewidth=1.5)
    ax.plot([1.8, 6.0], [4.4, 4.4], color=c_arrow, linewidth=1.5)

    # If NO -> Check str[i] == ch2
    draw_arrow(6.0, 6.3, 6.0, 5.5, label="No")

    # 6. Decision 2: str[i] == ch2 ?
    cond3 = patches.Polygon([[6.0, 5.5], [7.5, 4.8], [6.0, 4.1], [4.5, 4.8]],
                            facecolor=c_decision, edgecolor=c_border_decision, linewidth=1.8)
    ax.add_patch(cond3)
    ax.text(6.0, 4.8, "str[i] == ch2 ?", ha='center', va='center', fontsize=9, fontweight='bold')

    # If YES -> replace with ch1: str[i] <- ch1 (to right)
    draw_arrow(7.5, 4.8, 8.2, 4.8, label="Yes")
    rep2_patch = patches.Rectangle((8.2, 4.35), 1.9, 0.9, facecolor=c_assign, edgecolor=c_border_assign, linewidth=1.5)
    ax.add_patch(rep2_patch)
    ax.text(9.15, 4.8, "str[i] ← ch1", ha='center', va='center', fontsize=9, fontweight='bold')

    # From rep2 down to join
    ax.plot([9.15, 9.15], [4.35, 3.8], color=c_arrow, linewidth=1.5)
    ax.plot([9.15, 6.0], [3.8, 3.8], color=c_arrow, linewidth=1.5)

    # If NO -> join directly
    draw_arrow(6.0, 4.1, 6.0, 3.4, label="No")

    # 7. Increment counter: i <- i + 1 at y=3.4
    inc_patch = patches.Rectangle((4.5, 3.0), 3.0, 0.7, facecolor=c_assign, edgecolor=c_border_assign, linewidth=2)
    ax.add_patch(inc_patch)
    ax.text(6.0, 3.35, "i ← i + 1", ha='center', va='center', fontsize=10, fontweight='bold')

    # Loop back line from (4.5, 3.35) -> x=0.3 -> up to y=9.7 -> (4.2, 9.7)
    ax.plot([4.5, 0.3], [3.35, 3.35], color=c_arrow, linewidth=1.5)
    ax.plot([0.3, 0.3], [3.35, 9.7], color=c_arrow, linewidth=1.5)
    draw_arrow(0.3, 9.7, 4.2, 9.7)

    # 8. Output symbol at y=2.6
    out_poly = patches.Polygon([[3.0, 2.1], [8.5, 2.1], [8.0, 3.0], [2.5, 3.0]],
                               facecolor=c_io, edgecolor=c_border_io, linewidth=2)
    ax.add_patch(out_poly)
    ax.text(5.5, 2.55, 'Output: PUT "Modified string = " + str', ha='center', va='center', fontsize=9.5, fontweight='bold')

    draw_arrow(5.5, 2.1, 5.5, 1.4)

    # 9. End (Oval) at (5.5, 1.0)
    end_p = patches.FancyBboxPatch((4.0, 0.7), 3.0, 0.7, boxstyle="round,pad=0.2,rounding_size=0.35",
                                   facecolor=c_start, edgecolor=c_border_start, linewidth=2)
    ax.add_patch(end_p)
    ax.text(5.5, 1.05, "End", ha='center', va='center', fontsize=11, fontweight='bold')

    plt.title("RAPTOR Flowchart: Lexicographically Smallest String by Swapping Two Characters\nSaveetha School of Engineering | CSA10",
              fontsize=12, fontweight='bold', pad=15, color='#0F3057')
    plt.tight_layout()
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-05-Lexicographically-Smallest-String-Swap\diagrams\flowchart.png", dpi=300)
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-05-Lexicographically-Smallest-String-Swap\diagrams\flowchart.svg")
    plt.close()
    print("Generated Exp 5 flowchart diagrams successfully.")

if __name__ == "__main__":
    draw_flowchart()
