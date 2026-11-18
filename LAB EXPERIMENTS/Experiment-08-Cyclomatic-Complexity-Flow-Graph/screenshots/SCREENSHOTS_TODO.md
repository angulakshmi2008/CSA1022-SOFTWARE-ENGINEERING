# Screenshots To-Do List: Experiment 08 (RAPTOR / CFG)

To capture native desktop screenshots of the Cyclomatic Complexity calculation and Flow Graph in **RAPTOR** or your diagramming tool, follow this checklist:

| Step # | Screen / State | Details to Model and Capture | Target File Name |
|---|---|---|---|
| 1 | RAPTOR Workspace | Complete calculation flowchart: `Start` → Inputs (`E = 17`, `N = 13`, `P = 5`) → Assignment (`V_edges ← E - N + 2`, `V_pred ← P + 1`) → Outputs → `End`. | `screenshots/Figure_8.1_RAPTOR_CFG_Formula.png` |
| 2 | RAPTOR MasterConsole | Execution output showing the evaluation of inputs and display of Cyclomatic Complexity value `V(G) = 6` verified by both methods. | `screenshots/Figure_8.2_Master_Console_Output.png` |
| 3 | Control Flow Graph Diagram | Labeled CFG with 13 vertices, 17 directed edges, 5 highlighted predicate nodes, and 6 regions ($R_1 \dots R_6$). | `screenshots/Figure_8.3_Control_Flow_Graph.png` |

---

### Step-by-Step Instructions:
1. Open **RAPTOR** on Windows.
2. Build the visual flowchart:
   - **Input 1**: Prompt `"Enter number of edges (E):"` $\rightarrow$ `e`
   - **Input 2**: Prompt `"Enter number of nodes (N):"` $\rightarrow$ `n`
   - **Input 3**: Prompt `"Enter number of predicate nodes (P):"` $\rightarrow$ `p`
   - **Assignment 1**: `v_formula1 ← e - n + 2`
   - **Assignment 2**: `v_formula2 ← p + 1`
   - **Output 1**: `"Cyclomatic Complexity V(G) = " + v_formula1`
   - **Output 2**: `"Verified using Predicates V(G) = " + v_formula2`
3. Click **Run → Execute to Completion**. Supply `17`, `13`, and `5`.
4. Capture screenshots of the workspace and Master Console using `Win + Shift + S` and save them into this `screenshots/` directory.
