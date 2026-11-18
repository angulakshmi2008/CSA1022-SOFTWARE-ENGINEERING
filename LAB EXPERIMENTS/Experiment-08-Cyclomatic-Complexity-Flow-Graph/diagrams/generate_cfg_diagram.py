import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_cfg():
    fig, ax = plt.subplots(figsize=(10, 14), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Color Scheme
    c_node = '#E8F8F5'
    c_node_border = '#16A085'
    c_pred = '#FDEDEC'
    c_pred_border = '#C0392B'
    c_edge = '#2C3E50'

    # Node positions (x, y) for the 13 nodes
    # Entry at Node 1 (6, 14.8)
    pos = {
        1: (6.0, 14.8),
        2: (6.0, 13.0),
        3: (4.0, 11.5),
        4: (8.0, 11.5),
        5: (6.0, 10.0),
        6: (4.0, 8.5),
        7: (8.0, 8.5),
        8: (6.0, 7.0),
        9: (4.0, 5.5),
        10: (8.0, 5.5),
        11: (6.0, 4.0),
        12: (4.0, 2.5),
        13: (6.0, 1.0)
    }

    predicates = {1, 2, 5, 8, 11}

    # Draw directed edges
    edges = [
        (1, 2), (2, 3), (2, 4), (3, 5), (4, 5),
        (5, 6), (5, 7), (6, 8), (7, 8),
        (8, 9), (8, 10), (9, 11), (10, 11),
        (11, 12), (11, 13), (12, 13)
    ]

    for u, v in edges:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        ax.annotate('', xy=(x2, y2 + 0.35 if y2 < y1 else y2 - 0.35), xytext=(x1, y1 - 0.35 if y1 > y2 else y1 + 0.35),
                    arrowprops=dict(facecolor=c_edge, edgecolor=c_edge, width=1.4, headwidth=6, headlength=6))

    # Bypass edge 17: (1, 13) curved arc on the right
    ax.annotate('', xy=(6.35, 1.0), xytext=(6.35, 14.8),
                arrowprops=dict(facecolor='#8E44AD', edgecolor='#8E44AD', width=1.5, headwidth=6, headlength=6,
                                connectionstyle="arc3,rad=-0.45", linestyle='--'))
    ax.text(10.8, 8.0, "Edge 17 (Bypass)", fontsize=9, fontweight='bold', color='#8E44AD', rotation=-90)

    # Draw regions labels
    ax.text(6.0, 11.5, "Region R1", ha='center', va='center', fontsize=9, fontweight='bold', color='#2980B9')
    ax.text(6.0, 8.5, "Region R2", ha='center', va='center', fontsize=9, fontweight='bold', color='#2980B9')
    ax.text(6.0, 5.5, "Region R3", ha='center', va='center', fontsize=9, fontweight='bold', color='#2980B9')
    ax.text(4.8, 2.1, "Region R4", ha='center', va='center', fontsize=9, fontweight='bold', color='#2980B9')
    ax.text(8.8, 7.5, "Region R5", ha='center', va='center', fontsize=9, fontweight='bold', color='#2980B9')
    ax.text(1.2, 8.0, "Outer Region R6\n(Unbounded)", ha='center', va='center', fontsize=9, fontweight='bold', color='#7D3C98')

    # Draw Nodes
    for n, (x, y) in pos.items():
        is_p = n in predicates
        bg = c_pred if is_p else c_node
        border = c_pred_border if is_p else c_node_border
        c = patches.Circle((x, y), 0.38, facecolor=bg, edgecolor=border, linewidth=2.0)
        ax.add_patch(c)
        ax.text(x, y, str(n), ha='center', va='center', fontsize=11, fontweight='bold', color='#1B2631')
        if is_p:
            ax.text(x + 0.55, y, "[P]", fontsize=8, fontweight='bold', color=c_pred_border)

    # Legend
    legend_elements = [
        patches.Patch(facecolor=c_pred, edgecolor=c_pred_border, label='Predicate (Decision) Node (out-degree ≥ 2)'),
        patches.Patch(facecolor=c_node, edgecolor=c_node_border, label='Sequential Processing Node'),
        patches.Patch(facecolor='none', edgecolor='#8E44AD', linestyle='--', label='Bypass Edge (Edge 17)')
    ]
    ax.legend(handles=legend_elements, loc='upper left', frameon=True, fontsize=8.5)

    # Calculations banner at the bottom
    ax.text(6.0, 0.2, "Formula 1: V(G) = E - N + 2 = 17 - 13 + 2 = 6  |  Formula 2: V(G) = P + 1 = 5 + 1 = 6  |  Regions = 6",
            ha='center', va='center', fontsize=9.5, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#EAEDED', edgecolor='#BDC3C7'))

    plt.title("Control Flow Graph (CFG) for Cyclomatic Complexity\nNodes N=13, Edges E=17, Predicates P=5 → V(G) = 6\nSaveetha School of Engineering | CSA10 | Angulakshmi S (192524402)",
              fontsize=11.5, fontweight='bold', pad=15, color='#2C3E50')
    plt.tight_layout()
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-08-Cyclomatic-Complexity-Flow-Graph\diagrams\control_flow_graph.png", dpi=300)
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-08-Cyclomatic-Complexity-Flow-Graph\diagrams\control_flow_graph.svg")
    plt.close()
    print("Control flow graph diagrams generated successfully.")

if __name__ == "__main__":
    draw_cfg()
