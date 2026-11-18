# Screenshots To-Do List: Experiment 04

To complete the lab record submission with native desktop screenshots, follow these steps in **RAPTOR** on Windows:

| Step # | Screen / State | Description to Capture | Target File Name |
|---|---|---|---|
| 1 | RAPTOR Workspace | Complete flowchart connecting `Start` → `Input ("Enter a String:", str)` → `Assignment (length <- Length_Of(str))` → `Output ("Total Number of Characters = " + length)` → `End`. | `screenshots/Figure_4.1_Execute_Flowchart.png` |
| 2 | RAPTOR MasterConsole | Dialog showing string prompt `SoftwareEngineering`, followed by the MasterConsole output displaying `Total Number of Characters = 19` and `Run Complete: 5 Symbols Evaluated`. | `screenshots/Figure_4.2_Master_Console.png` |

---

### Step-by-Step Instructions to Capture:
1. Open RAPTOR on Windows (`Start Menu` -> `RAPTOR`).
2. Click **File -> New**.
3. From the left symbol toolbar:
   - Drag an **Input** symbol between `Start` and `End`. Double-click it:
     - Prompt: `"Enter a String:"`
     - Variable: `str`
   - Drag an **Assignment** symbol below Input. Double-click it:
     - Set: `length`
     - To: `Length_Of(str)`
   - Drag an **Output** symbol below Assignment. Double-click it:
     - Output: `"Total Number of Characters = " + length`
     - Check "End of Current Line"
4. Click **Run -> Execute to Completion** (or press the green Play button).
5. Enter `"SoftwareEngineering"` in the prompt box and click **Done**.
6. Use `Win + Shift + S` to capture the workspace and Master Console, and save them in this `screenshots/` directory.
