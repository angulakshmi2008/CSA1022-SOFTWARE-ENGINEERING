"""
Q2: Cyclomatic Complexity Verification & Control Flow Graph Generator
Validates:
- Number of Nodes (N) = 17
- Number of Edges (E) = 22
- Number of Predicate Nodes = 6
- Connected Components (P) = 1
- V(G) Formula 1: E - N + 2P = 22 - 17 + 2(1) = 7
- V(G) Formula 2: Predicates + 1 = 6 + 1 = 7
Generates:
- High-resolution flow_graph.png
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def get_graph():
    nodes = list(range(1, 18))
    edges = [
        (1, 2),        # Start to Predicate 1
        (2, 3), (2, 4),# Predicate 1 (True: 3, False: 4)
        (3, 5),        # Join from branch 3 to 5
        (4, 5),        # Join from branch 4 to 5
        (5, 6), (5, 10),# Predicate 2 (Loop Condition: True -> 6, False -> 10)
        (6, 7), (6, 8),# Predicate 3 (Inside Loop: True -> 7, False -> 8)
        (7, 9),        # Branch 7 to join 9
        (8, 9),        # Branch 8 to join 9
        (9, 5),        # Loop back-edge: 9 to 5
        (10, 11), (10, 12), # Predicate 4 (True -> 11, False -> 12)
        (11, 13),      # Branch 11 to join 13
        (12, 13), (12, 14), # Predicate 5 (True -> 13, False -> 14)
        (13, 15),      # Join 13 to Predicate 6 (node 15)
        (14, 15),      # Join 14 to Predicate 6 (node 15)
        (15, 16), (15, 17), # Predicate 6 (True -> 16, False -> 17)
        (16, 17)       # Branch 16 to Exit (node 17)
    ]
    return nodes, edges

def verify():
    nodes, edges = get_graph()
    num_nodes = len(nodes)
    num_edges = len(edges)
    
    out_degree = {n: 0 for n in nodes}
    in_degree = {n: 0 for n in nodes}
    for u, v in edges:
        out_degree[u] += 1
        in_degree[v] += 1
        
    predicate_nodes = [n for n, deg in out_degree.items() if deg == 2]
    num_predicates = len(predicate_nodes)
    P = 1
    
    vg1 = num_edges - num_nodes + 2 * P
    vg2 = num_predicates + 1
    
    print("=" * 65)
    print(" CONTROL FLOW GRAPH MATHEMATICAL VERIFICATION REPORT")
    print("=" * 65)
    print(f"Total Nodes (N)            : {num_nodes} (Expected: 17)")
    print(f"Total Edges (E)            : {num_edges} (Expected: 22)")
    print(f"Predicate Nodes count      : {num_predicates} (Expected: 6)")
    print(f"Predicate Nodes list       : {predicate_nodes}")
    print(f"Connected Components (P)   : {P}")
    print("-" * 65)
    print(f"Formula 1: V(G) = E - N + 2P  = {num_edges} - {num_nodes} + 2({P}) = {vg1}")
    print(f"Formula 2: V(G) = Pred + 1    = {num_predicates} + 1 = {vg2}")
    print("-" * 65)
    assert num_nodes == 17, f"Expected 17 nodes, got {num_nodes}"
    assert num_edges == 22, f"Expected 22 edges, got {num_edges}"
    assert num_predicates == 6, f"Expected 6 predicate nodes, got {num_predicates}"
    assert vg1 == 7, f"Expected V(G)=7, got {vg1}"
    assert vg2 == 7, f"Expected V(G)=7, got {vg2}"
    print("[PASS] MATHEMATICAL VERIFICATION CONFIRMED: V(G) = 7 BY BOTH METHODS")
    print("=" * 65)
    
    # 7 Independent Basis Paths
    basis_paths = [
        "Path 1 (Baseline: Skip loop, then 10, skip 16): 1 -> 2 -> 3 -> 5 -> 10 -> 11 -> 13 -> 15 -> 17",
        "Path 2 (Flip P1 false):                       1 -> 2 -> 4 -> 5 -> 10 -> 11 -> 13 -> 15 -> 17",
        "Path 3 (Flip P2 true, P3 true inside loop):     1 -> 2 -> 3 -> 5 -> 6 -> 7 -> 9 -> 5 -> 10 -> 11 -> 13 -> 15 -> 17",
        "Path 4 (Flip P3 false inside loop):             1 -> 2 -> 3 -> 5 -> 6 -> 8 -> 9 -> 5 -> 10 -> 11 -> 13 -> 15 -> 17",
        "Path 5 (Flip P4 false, P5 true):               1 -> 2 -> 3 -> 5 -> 10 -> 12 -> 13 -> 15 -> 17",
        "Path 6 (Flip P5 false):                        1 -> 2 -> 3 -> 5 -> 10 -> 12 -> 14 -> 15 -> 17",
        "Path 7 (Flip P6 true):                         1 -> 2 -> 3 -> 5 -> 10 -> 11 -> 13 -> 15 -> 16 -> 17"
    ]
    print("\nLinearly Independent Basis Paths (Total: 7):")
    for bp in basis_paths:
        print(f"  {bp}")
    print("=" * 65)

def render_diagram(output_path="flow_graph.png"):
    nodes, edges = get_graph()
    
    # Coordinates layout: top-to-bottom flow (y decreases from top)
    pos = {
        1:  (4.0, 15.0), # Start
        2:  (4.0, 13.5), # P1
        3:  (2.5, 12.0), # Then
        4:  (5.5, 12.0), # Else
        5:  (4.0, 10.5), # P2 (Loop Header)
        6:  (2.5, 9.0),  # P3 (Loop Body)
        7:  (1.5, 7.8),  # P3 True
        8:  (3.5, 7.8),  # P3 False
        9:  (2.5, 6.5),  # Loop Latch
        10: (5.5, 9.0),  # P4 (After Loop)
        11: (4.5, 7.5),  # P4 True
        12: (6.5, 7.5),  # P5 (P4 False)
        13: (5.0, 6.0),  # P5 True Join
        14: (7.0, 6.0),  # P5 False
        15: (5.5, 4.5),  # P6
        16: (4.0, 3.2),  # P6 True
        17: (5.5, 1.8),  # Exit
    }

    predicates = {2, 5, 6, 10, 12, 15}

    fig, ax = plt.subplots(figsize=(10, 14), dpi=300)
    ax.set_facecolor("#FAFAFA")
    fig.patch.set_facecolor("#FFFFFF")

    # Title and Metadata Header
    ax.text(4.0, 16.2, "Control Flow Graph (CFG)", fontsize=16, fontweight="bold", ha="center", color="#1E293B")
    ax.text(4.0, 15.7, "Nodes (N) = 17  |  Edges (E) = 22  |  Predicate Nodes (P) = 6  |  V(G) = 7", 
            fontsize=11, ha="center", color="#475569", style="italic")

    # Draw Edges with Arrows
    for u, v in edges:
        x1, y1 = pos[u]
        x2, y2 = pos[v]

        # Special curved back-edge for loop (9 -> 5)
        if (u, v) == (9, 5):
            rad = 0.5
            color = "#DC2626"
            lw = 2.0
            arrow = patches.FancyArrowPatch(
                (x1 - 0.25, y1), (x2 - 0.35, y2),
                connectionstyle="arc3,rad=-0.4",
                arrowstyle="-|>,head_length=6,head_width=4",
                color=color, lw=lw, zorder=2
            )
            ax.add_patch(arrow)
            ax.text(0.6, 8.5, "Loop Back-Edge\n(9 -> 5)", fontsize=9, fontweight="bold", color="#DC2626", ha="center")
            continue

        # Normal straight / slight curve edges
        dx = x2 - x1
        dy = y2 - y1
        dist = (dx**2 + dy**2)**0.5
        # Trim near node boundaries (radius ~ 0.35)
        r = 0.36
        sx = x1 + (dx / dist) * r
        sy = y1 + (dy / dist) * r
        ex = x2 - (dx / dist) * r
        ey = y2 - (dy / dist) * r

        arrow = patches.FancyArrowPatch(
            (sx, sy), (ex, ey),
            arrowstyle="-|>,head_length=5,head_width=3.5",
            color="#334155", lw=1.5, zorder=2
        )
        ax.add_patch(arrow)

        # Label decision branches
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        if u in predicates:
            if u == 2:
                lbl = "T" if v == 3 else "F"
                ax.text(mid_x + (0.15 if v==4 else -0.15), mid_y, lbl, fontsize=9, fontweight="bold", color="#2563EB")
            elif u == 5:
                lbl = "Loop True" if v == 6 else "Exit False"
                ax.text(mid_x + (0.35 if v==10 else -0.35), mid_y, lbl, fontsize=8, fontweight="bold", color="#2563EB")
            elif u == 6:
                lbl = "T" if v == 7 else "F"
                ax.text(mid_x + (0.15 if v==8 else -0.15), mid_y, lbl, fontsize=9, fontweight="bold", color="#2563EB")
            elif u == 10:
                lbl = "T" if v == 11 else "F"
                ax.text(mid_x + (0.15 if v==12 else -0.15), mid_y, lbl, fontsize=9, fontweight="bold", color="#2563EB")
            elif u == 12:
                lbl = "T" if v == 13 else "F"
                ax.text(mid_x + (0.15 if v==14 else -0.15), mid_y, lbl, fontsize=9, fontweight="bold", color="#2563EB")
            elif u == 15:
                lbl = "T" if v == 16 else "F"
                ax.text(mid_x + (0.2 if v==17 else -0.2), mid_y, lbl, fontsize=9, fontweight="bold", color="#2563EB")

    # Draw Nodes
    for n in nodes:
        x, y = pos[n]
        if n == 1:
            # Start Node: Green
            circle = plt.Circle((x, y), 0.35, facecolor="#10B981", edgecolor="#047857", lw=2, zorder=3)
            lbl = "1\n(Start)"
            tcolor = "#FFFFFF"
        elif n == 17:
            # Exit Node: Dark Blue / Double Circle
            circle = plt.Circle((x, y), 0.35, facecolor="#64748B", edgecolor="#1E293B", lw=2.5, zorder=3)
            lbl = "17\n(Exit)"
            tcolor = "#FFFFFF"
        elif n in predicates:
            # Predicate / Decision Nodes: Amber / Yellow
            circle = plt.Circle((x, y), 0.35, facecolor="#F59E0B", edgecolor="#B45309", lw=2, zorder=3)
            lbl = f"{n}\n(P)"
            tcolor = "#1E293B"
        else:
            # Sequential Nodes: Soft Blue
            circle = plt.Circle((x, y), 0.35, facecolor="#E0E7FF", edgecolor="#4F46E5", lw=1.5, zorder=3)
            lbl = f"{n}"
            tcolor = "#1E1B4B"

        ax.add_patch(circle)
        ax.text(x, y, lbl, ha="center", va="center", fontsize=8.5, fontweight="bold", color=tcolor, zorder=4)

    # Legend & Formulas Box
    legend_elements = [
        "Legend:",
        "[Green] Node 1: Start (Entry)",
        "[Orange] Nodes 2, 5, 6, 10, 12, 15: Predicates (6 Decisions)",
        "[Red Curve] Edge (9 -> 5): Loop Back-Edge",
        "[Slate] Node 17: Exit Node",
        "\nCyclomatic Complexity:",
        "Formula 1: V(G) = E - N + 2P = 22 - 17 + 2(1) = 7",
        "Formula 2: V(G) = Predicate Nodes + 1 = 6 + 1 = 7",
        "Basis Paths = 7 Independent Test Cases"
    ]
    ax.text(0.1, 2.8, "\n".join(legend_elements), fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.6", facecolor="#F1F5F9", edgecolor="#CBD5E1", lw=1.2),
            va="top", ha="left", color="#1E293B")

    ax.set_xlim(-0.2, 8.2)
    ax.set_ylim(0.8, 16.8)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[+] Rendered Control Flow Graph image to: {output_path}")

if __name__ == "__main__":
    verify()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flow_graph.png")
    render_diagram(out)
