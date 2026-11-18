# Screenshots To-Do List: Experiment 06 (Umbrello / StarUML)

To capture native desktop screenshots of the UML diagrams using **Umbrello UML Modeller** or **StarUML**, follow this checklist:

| Step # | Diagram Type | Details to Model and Capture | Target File Name |
|---|---|---|---|
| 1 | Class Diagram | Classes: `Customer`, `Restaurant`, `Menu`, `FoodItem`, `Order`, `Payment`, `DeliveryAgent`, `Delivery` with attributes, methods, visibility (`+`, `-`), association, aggregation (Menu to FoodItem), and composition (Restaurant to Menu). | `screenshots/Figure_6.1_Class_Diagram.png` |
| 2 | Use Case Diagram | Actors: `Customer`, `Restaurant`, `Delivery Agent`, `Administrator` with system boundary `Online Food Delivery Platform` enclosing use cases: Browse Restaurants, View Menu, Place Order, Make Payment, Track Order, Manage Menu, Update Order Status, Accept Delivery. | `screenshots/Figure_6.2_Use_Case_Diagram.png` |
| 3 | Activity Diagram | Initial Node → Browse Restaurants → Select Food Items → Place Order → Payment Decision (`[Yes]` / `[No]`) → Restaurant Prepares Food → Assign Delivery Agent → Track Delivery → Deliver Order → Final Node. | `screenshots/Figure_6.3_Activity_Diagram.png` |

---

### Step-by-Step Instructions:
1. Open **Umbrello** or **StarUML** on your computer.
2. Create a new project titled `"Online Food Delivery System"`.
3. In the tree view / model explorer:
   - Add a **Class Diagram**: Create the 8 classes, define attributes/operations, and draw the association/aggregation/composition connectors.
   - Add a **Use Case Diagram**: Place stick-figure actors, draw the system boundary box, add ellipses for each use case, and link with association lines.
   - Add an **Activity Diagram**: Insert initial solid node, rounded action rectangles, diamond decision node, control flow arrows, and final double-circle node.
4. Export each diagram via **Diagram → Export as Image** (or take a screenshot using `Win + Shift + S`) and save them in this `screenshots/` directory.
