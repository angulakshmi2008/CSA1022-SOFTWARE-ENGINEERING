# Q2 — Cyclomatic Complexity Calculations & Mathematical Analysis

**Course:** Software Engineering (CSA10)  
**Topic:** Calculation of Cyclomatic Complexity for Control Flow Graph (CFG)  
**Assessment:** Model Practical – Set 2  

---

## 1. Given Data from the Examination Question

- **Number of Edges ($E$):** $22$
- **Number of Nodes ($N$):** $17$
- **Number of Predicate (Decision) Nodes:** $6$
- **Connected Components ($P$):** $1$ (for a single monolithic program or function)

---

## 2. Step-by-Step Calculation Methods

### Method 1: Edges and Nodes Formula (McCabe's Fundamental Theorem)

The cyclomatic complexity $V(G)$ of a flow graph $G$ is mathematically defined as:
$$V(G) = E - N + 2P$$

Where:
- $E = 22$ (total directed control flow edges)
- $N = 17$ (total program statement and decision nodes)
- $P = 1$ (single connected component / program entry-exit graph)

#### Substitution and Derivation:
$$V(G) = 22 - 17 + 2(1)$$
$$V(G) = 5 + 2$$
$$\mathbf{V(G) = 7}$$

---

### Method 2: Predicate-Node Formula

In structured programming, every binary decision statement (such as `if`, `while`, or `for`) acts as a **predicate node** having exactly two outgoing edges (True and False branches). Each predicate increases the number of linearly independent paths by 1.

The formula is:
$$V(G) = \text{Number of Predicate Nodes} + 1$$

Where:
- Predicate Nodes $= 6$

#### Substitution and Derivation:
$$V(G) = 6 + 1$$
$$\mathbf{V(G) = 7}$$

---

### Method 3: Planar Graph Region Count Method (Verification Method)

For any planar control flow graph, cyclomatic complexity equals the total number of enclosed planar regions plus the single unbounded external region:
$$V(G) = R$$

In our verified graph:
- Number of internal enclosed regions ($R_1, R_2, R_3, R_4, R_5, R_6$) = $6$
- Outer unbounded region ($R_7$) = $1$
- Total regions $R = 6 + 1 = \mathbf{7}$

---

## 3. Comparison and Verification of Results

| Method | Formula | Substitution | Calculated $V(G)$ | Agreement |
| :--- | :--- | :--- | :---: | :---: |
| **Method 1 (Edges & Nodes)** | $V(G) = E - N + 2P$ | $22 - 17 + 2(1)$ | **7** | **MATCH** |
| **Method 2 (Predicate Nodes)** | $V(G) = \text{Predicates} + 1$ | $6 + 1$ | **7** | **MATCH** |
| **Method 3 (Bounded Regions)** | $V(G) = R$ | $6 + 1$ | **7** | **MATCH** |

**Conclusion:** All three independent mathematical formulations yield the exact same value: $\mathbf{V(G) = 7}$.

---

## 4. What Cyclomatic Complexity Means

Developed by Thomas J. McCabe in 1976, **Cyclomatic Complexity** is a quantitative software engineering metric that measures the structural and logical complexity of a program. 

Specifically:
1. **Upper Bound on Independent Execution Paths:** It defines the maximum number of linearly independent paths through the source code.
2. **Basis Path Testing:** It specifies the **minimum number of test cases** required to achieve 100% branch and statement coverage (meaning every statement is executed at least once and every decision outcome is evaluated in both directions).
3. **Complexity Threshold:** A complexity of **7** falls within the healthy, highly testable, and low-risk bracket ($1 \le V(G) \le 10$).

---

## 5. Linearly Independent Basis Path Set (7 Test Cases)

For the verified Control Flow Graph ($N=17, E=22$), the 7 linearly independent paths that span the execution space are:

1. **Path 1 (Baseline Path):**  
   `1 -> 2 -> 3 -> 5 -> 10 -> 11 -> 13 -> 15 -> 17`  
   *Condition Profile:* Decision 1 True, Decision 2 False (Skip loop), Decision 4 True, Decision 6 False.

2. **Path 2 (Exercise Decision 1 False Branch):**  
   `1 -> 2 -> 4 -> 5 -> 10 -> 11 -> 13 -> 15 -> 17`  
   *Condition Profile:* Decision 1 False (Node 4), skips loop, Decision 4 True, Decision 6 False.

3. **Path 3 (Exercise Loop Body with Decision 3 True):**  
   `1 -> 2 -> 3 -> 5 -> 6 -> 7 -> 9 -> 5 -> 10 -> 11 -> 13 -> 15 -> 17`  
   *Condition Profile:* Enters loop (Decision 2 True), executes Node 6 True (Node 7), returns via back-edge `9 -> 5`, then exits.

4. **Path 4 (Exercise Loop Body with Decision 3 False):**  
   `1 -> 2 -> 3 -> 5 -> 6 -> 8 -> 9 -> 5 -> 10 -> 11 -> 13 -> 15 -> 17`  
   *Condition Profile:* Enters loop (Decision 2 True), executes Node 6 False (Node 8), returns via back-edge `9 -> 5`.

5. **Path 5 (Exercise Decision 4 False, Decision 5 True):**  
   `1 -> 2 -> 3 -> 5 -> 10 -> 12 -> 13 -> 15 -> 17`  
   *Condition Profile:* Skips loop, Decision 4 False (Node 12), Decision 5 True (Node 13).

6. **Path 6 (Exercise Decision 5 False Branch):**  
   `1 -> 2 -> 3 -> 5 -> 10 -> 12 -> 14 -> 15 -> 17`  
   *Condition Profile:* Skips loop, Decision 4 False, Decision 5 False (Node 14).

7. **Path 7 (Exercise Decision 6 True Branch):**  
   `1 -> 2 -> 3 -> 5 -> 10 -> 11 -> 13 -> 15 -> 16 -> 17`  
   *Condition Profile:* Decision 1 True, skips loop, Decision 4 True, Decision 6 True (Node 16 to Exit).

Each basis path introduces at least one new edge that is not covered by any prior path, satisfying McCabe's linear independence criteria.
