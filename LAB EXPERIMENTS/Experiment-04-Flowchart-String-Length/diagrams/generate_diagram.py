import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_raptor_flowchart():
    fig, ax = plt.subplots(figsize=(7, 9), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Styles
    box_blue = '#E8F1F5'
    border_blue = '#00587A'
    font_family = 'sans-serif'

    # Symbols:
    # 1. Start (Oval) at y=10.5
    start_patch = patches.FancyBboxPatch((3.5, 10.2), 3.0, 0.9,
                                         boxstyle="round,pad=0.2,rounding_size=0.45",
                                         facecolor=box_blue, edgecolor=border_blue, linewidth=2)
    ax.add_patch(start_patch)
    ax.text(5.0, 10.65, "Start", ha='center', va='center', fontsize=12, fontweight='bold', color='#0F3057')

    # Arrow 1: (5.0, 10.2) -> (5.0, 8.9)
    ax.annotate('', xy=(5.0, 8.9), xytext=(5.0, 10.2),
                arrowprops=dict(facecolor=border_blue, edgecolor=border_blue, width=1.5, headwidth=8, headlength=8))

    # 2. Input Symbol (Parallelogram): "Enter a String" -> GET str at y=8.0
    input_poly = patches.Polygon([[2.3, 7.8], [7.7, 7.8], [7.2, 8.9], [1.8, 8.9]],
                                 facecolor='#FFF6E9', edgecolor='#FF7E67', linewidth=2)
    ax.add_patch(input_poly)
    ax.text(4.75, 8.45, 'Input: "Enter a string"', ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(4.75, 8.1, 'GET str', ha='center', va='center', fontsize=10, fontstyle='italic')

    # Arrow 2: (5.0, 7.8) -> (5.0, 6.5)
    ax.annotate('', xy=(5.0, 6.5), xytext=(5.0, 7.8),
                arrowprops=dict(facecolor=border_blue, edgecolor=border_blue, width=1.5, headwidth=8, headlength=8))

    # 3. Assignment Symbol (Rectangle): length <- Length_Of(str) at y=5.6
    assign_patch = patches.Rectangle((2.5, 5.6), 5.0, 0.9,
                                     facecolor='#E8F8F5', edgecolor='#1ABC9C', linewidth=2)
    ax.add_patch(assign_patch)
    ax.text(5.0, 6.05, "length ← Length_Of(str)", ha='center', va='center', fontsize=11, fontweight='bold', color='#117A65')

    # Arrow 3: (5.0, 5.6) -> (5.0, 4.3)
    ax.annotate('', xy=(5.0, 4.3), xytext=(5.0, 5.6),
                arrowprops=dict(facecolor=border_blue, edgecolor=border_blue, width=1.5, headwidth=8, headlength=8))

    # 4. Output Symbol (Parallelogram): PUT "Total Number of Characters = " + length at y=3.4
    output_poly = patches.Polygon([[2.3, 3.2], [7.7, 3.2], [7.2, 4.3], [1.8, 4.3]],
                                  facecolor='#FEF9E7', edgecolor='#F39C12', linewidth=2)
    ax.add_patch(output_poly)
    ax.text(4.75, 3.85, 'Output:', ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(4.75, 3.5, 'PUT "Total Number of Characters = " + length', ha='center', va='center', fontsize=9)

    # Arrow 4: (5.0, 3.2) -> (5.0, 1.9)
    ax.annotate('', xy=(5.0, 1.9), xytext=(5.0, 3.2),
                arrowprops=dict(facecolor=border_blue, edgecolor=border_blue, width=1.5, headwidth=8, headlength=8))

    # 5. End (Oval) at y=1.0
    end_patch = patches.FancyBboxPatch((3.5, 1.0), 3.0, 0.9,
                                       boxstyle="round,pad=0.2,rounding_size=0.45",
                                       facecolor=box_blue, edgecolor=border_blue, linewidth=2)
    ax.add_patch(end_patch)
    ax.text(5.0, 1.45, "End", ha='center', va='center', fontsize=12, fontweight='bold', color='#0F3057')

    plt.title("RAPTOR Flowchart: Find Length of a String\nSaveetha School of Engineering | CSA10",
              fontsize=13, fontweight='bold', pad=15, color='#0F3057')
    plt.tight_layout()
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-04-Flowchart-String-Length\diagrams\flowchart.png", dpi=300)
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-04-Flowchart-String-Length\diagrams\flowchart.svg")
    plt.close()
    print("Generated flowchart.png and flowchart.svg successfully.")

if __name__ == "__main__":
    draw_raptor_flowchart()
