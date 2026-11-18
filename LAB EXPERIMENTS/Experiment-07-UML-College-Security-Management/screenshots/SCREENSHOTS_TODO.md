# Screenshots To-Do List: Experiment 07 (Umbrello / StarUML)

To capture native desktop screenshots of the UML diagrams using **Umbrello UML Modeller** or **StarUML**, follow this checklist:

| Step # | Diagram Type | Details to Model and Capture | Target File Name |
|---|---|---|---|
| 1 | Class Diagram | Classes: `Administrator`, `SecurityPersonnel`, `DutySchedule`, `CampusLocation`, `Attendance`, `Leave`, `Salary`, `AccountsOfficer` with attributes, methods, visibility markers (`+`, `-`), associations, and multiplicities (`1`, `0..*`, `1..*`). | `screenshots/Figure_7.1_Class_Diagram.png` |
| 2 | Use Case Diagram | Actors: `Administrator`, `Security Personnel`, `Accounts Officer` with system boundary `College Security Management System` enclosing use cases: Login, Assign Duty, View Duty Schedule, Record Attendance, Apply Leave, Approve Leave, Calculate Salary, Generate Reports, Logout. | `screenshots/Figure_7.2_Use_Case_Diagram.png` |
| 3 | Activity Diagram | Initial Node → Login → Admin Assigns Duty → Guard Checks-In → Patrol & Duty → Decision Node: Leave Applied? (`[Yes]` → Admin Approves, `[No]` → Continue) → Guard Checks-Out → Accounts Officer Calculates Salary → Payslip Generated → Final Node. | `screenshots/Figure_7.3_Activity_Diagram.png` |

---

### Step-by-Step Instructions:
1. Open **Umbrello** or **StarUML** on your PC.
2. Create a new UML project titled `"Online Security Management System"`.
3. Model the 3 diagrams:
   - **Class Diagram**: Place all 8 entities, specify typed fields and operations, and draw associations with cardinalities.
   - **Use Case Diagram**: Place the 3 actors, draw boundary box, insert use case ovals, and connect with associations.
   - **Activity Diagram**: Draw initial node, rounded action rectangles, decision diamond, and final bullseye node.
4. Export via **Diagram → Export as Image** (or capture using `Win + Shift + S`) and save into this `screenshots/` directory.
