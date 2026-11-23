# Part B — Analysis: Pull Request Protection & Merge Conflict Resolution

**Course:** Software Engineering (CSA10)  
**Question:** Q1 Part B (10 Marks)  
**Topic:** Pull Request Review Protection & Merge Conflict Resolution Workflow  

---

## Question:
> *"Explain how reviewing a pull request before merging protects the main branch. Describe how you would detect and resolve a merge conflict if main had also changed signup.py."*

---

## 1. How Reviewing a Pull Request Protects the Main Branch

In modern version control workflows (such as GitHub Flow or GitLab Flow), the `main` branch represents the single source of truth and production-ready state of the software. Direct pushes to `main` are restricted to maintain system stability, security, and quality.

### A. Gatekeeping and Code Quality Assurance
1. **Defect and Bug Detection:** Reviewers inspect the logic before code enters the release pipeline. They identify unhandled edge cases (such as `None` values, empty strings, or buffer overflows) that the original developer may have overlooked.
2. **Security Vulnerability Prevention:** Reviewers check for credential mishandling, injection flaws, hardcoded secrets, or insecure password storage practices (e.g., ensuring passwords meet minimum length and are ready for hashing).
3. **Adherence to Coding Standards:** Code reviews enforce architectural guidelines, naming conventions, documentation, and maintainability rules across the engineering team.

### B. Automated Continuous Integration (CI) Checks
A Pull Request serves as a synchronization point for automated DevOps pipelines:
- **Automated Unit Tests:** Test suites (like `test_signup.py`) automatically execute against the PR. If any test fails, merging is blocked.
- **Code Coverage & Linters:** Static analysis tools verify code formatting and ensure test coverage thresholds are satisfied.
- **Security Scanners:** Tools like SAST (Static Application Security Testing) scan code for known vulnerabilities.

### C. Enforcing Branch Protection Policies
GitHub Branch Protection Rules require:
- At least 1–2 peer approvals before a PR can be merged.
- All CI status checks to pass.
- Up-to-date branch status (requiring the feature branch to incorporate any recent changes from `main` before merging).
- Prevention of accidental forced pushes (`git push --force`) or branch deletions.

---

## 2. Detecting a Merge Conflict (When Main Also Changed `signup.py`)

### A. Why the Conflict Occurs
A merge conflict occurs when Developer A modifies `signup.py` on `feature-signup`, while Developer B (or another PR) concurrently modifies the exact same lines of `signup.py` on `main`. Because Git uses a **three-way merge** algorithm based on the common ancestor commit, it cannot determine which version is authoritative and pauses the merge.

### B. How Git Detects and Alerts the Developer
When the developer attempts to merge `main` into `feature-signup` (or merge `feature-signup` into `main`):
```bash
git checkout feature-signup
git merge main
```
Git halts the operation and outputs:
```text
Auto-merging Q1_Feature_Branch_Signup/signup.py
CONFLICT (content): Merge conflict in Q1_Feature_Branch_Signup/signup.py
Automatic merge failed; fix conflicts and then commit the result.
```

### C. Identifying Conflicted Lines
Running `git status` lists the file under **Unmerged paths**:
```bash
git status
# Output shows: both modified: signup.py
```
Opening `signup.py` reveals Git's standard three conflict markers:
```python
<<<<<<< HEAD
    # Current branch logic (e.g., feature-signup):
    if len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters long."}
=======
    # Incoming branch logic (e.g., updated main branch):
    if len(password) < 8 or not any(c.isupper() for c in password):
        return {"success": False, "message": "Password must be at least 8 characters with an uppercase letter."}
>>>>>>> main
```

- `<<<<<<< HEAD` indicates the start of changes on the current active branch.
- `=======` separates the conflicting versions.
- `>>>>>>> main` marks the end of conflicting changes from the incoming branch.

---

## 3. Step-by-Step Merge Conflict Resolution Procedure

To resolve this conflict cleanly and protect the integrity of the application, follow these five steps:

### Step 1: Analyze and Reconcile with the Team
Inspect both implementations using `git diff`. Coordinate with the author of the conflicting commit to determine whether to adopt one version, combine both features, or formulate a new consensus.

### Step 2: Edit the File and Eliminate All Conflict Markers
Manually edit `signup.py` to keep the agreed-upon business logic. For example, adopt the stronger validation rule while retaining clear messaging:
```python
    # Reconciled logic:
    if len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters long."}
```
**Mandatory Action:** Delete all marker lines (`<<<<<<<`, `=======`, `>>>>>>>`). Leaving any marker in the source code causes syntax errors.

### Step 3: Run Automated Verification Tests
Run the unit test suite immediately after editing:
```bash
python -m unittest test_signup.py
```
Ensure all boundary conditions (e.g., empty username, password lengths 5 and 6) pass.

### Step 4: Stage the Resolved File
Staging marks the file as resolved in Git's index:
```bash
git add signup.py
git status
# Output confirms: "All conflicts fixed but you are still merging."
```

### Step 5: Conclude the Merge Commit
Finalize the merge by committing the resolution:
```bash
git commit -m "Merge main into feature-signup: reconcile password validation conflict"
```
The feature branch is now up to date with `main`, conflict-free, verified by tests, and ready for clean Pull Request merging.

---

## 4. Key Summary for Lab Viva

| Concept | Explanation |
| :--- | :--- |
| **Pull Request (PR)** | A formal proposal to merge changes from a feature branch into the target branch, allowing peer review and CI checks. |
| **Main Branch Protection** | Enforced repository policies preventing broken or unvetted code from entering production. |
| **Merge Conflict** | A state where Git cannot automatically reconcile concurrent, overlapping changes to the same file. |
| **Conflict Delimiters** | `<<<<<<< HEAD` (current), `=======` (separator), and `>>>>>>> <branch>` (incoming). |
| **Resolution Rule** | Discuss $\rightarrow$ Edit code $\rightarrow$ Remove all markers $\rightarrow$ Execute tests $\rightarrow$ Stage (`git add`) $\rightarrow$ Commit. |
