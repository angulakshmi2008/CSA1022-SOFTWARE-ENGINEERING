# Screenshots To-Do List: Experiment 05

To complete the lab record submission with native desktop screenshots, perform the following in **RAPTOR** on Windows:

| Step # | Screen / State | Description to Capture | Target File Name |
|---|---|---|---|
| 1 | RAPTOR Workspace | Complete flowchart connecting `Start` → Inputs (`str`, `ch1`, `ch2`) → Assignment (`i <- 1, n <- Length_Of(str)`) → Loop (`i <= n`) with two Selection blocks (`str[i] == ch1` and `str[i] == ch2`) → Increment (`i <- i + 1`) → Output (`PUT "Modified string = " + str`) → `End`. | `screenshots/Figure_5.1_Validate_Flowchart.png` |
| 2 | RAPTOR MasterConsole | Interactive input dialogs entering `str = "ccad"`, `ch1 = "c"`, `ch2 = "a"`, followed by MasterConsole output displaying `Modified string = aacd` and symbol count evaluated. | `screenshots/Figure_5.2_Master_Console_Result.png` |

---

### Step-by-Step Instructions to Capture:
1. Open RAPTOR on Windows (`Start Menu` -> `RAPTOR`).
2. Build the visual algorithm:
   - **Input 1**: `"Enter the string:"` $\rightarrow$ `str`
   - **Input 2**: `"Enter first character (ch1):"` $\rightarrow$ `ch1`
   - **Input 3**: `"Enter second character (ch2):"` $\rightarrow$ `ch2`
   - **Assignment**: `i ← 1`, `n ← Length_Of(str)`
   - **Loop**: Condition `i > n` (exit condition)
     - Inside loop:
       - **Selection 1**: Condition `str[i] = ch1`
         - Yes path: Assignment `str[i] ← ch2`
         - No path: **Selection 2**: Condition `str[i] = ch2`
           - Yes path: Assignment `str[i] ← ch1`
       - **Assignment**: `i ← i + 1`
   - **Output**: `"Modified string = " + str`
3. Click **Run → Execute to Completion**.
4. Enter `ccad`, `c`, and `a` in the successive prompt dialogs.
5. Capture with `Win + Shift + S` and save the images into this `screenshots/` directory.
