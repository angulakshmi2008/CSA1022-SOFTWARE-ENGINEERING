# Merge Conflict Detection and Resolution Demonstration

## 1. What is a Merge Conflict?

A **merge conflict** occurs in Git when two branches modify the **exact same line(s)** of a file in different ways, or when one branch modifies a file that another branch deleted. 

Git's automatic three-way merge algorithm cannot automatically decide which change is correct; it pauses the merge process, marks the conflicted area with special **conflict markers**, and requests human intervention.

---

## 2. Realistic Scenario: Conflicting Password Requirements

Imagine two developers working concurrently:
- **Developer A (Branch: `feature-strict-password`):** Increases the password minimum length to 8 characters and adds an uppercase check.
- **Developer B (Branch: `main`):** Updates the password validation line to require 6 characters plus a special character symbol check.

When Developer A attempts to merge their branch into `main`:
```bash
git checkout main
git merge feature-strict-password
```
Git prints:
```text
Auto-merging Q1_Feature_Branch_Signup/signup.py
CONFLICT (content): Merge conflict in Q1_Feature_Branch_Signup/signup.py
Automatic merge failed; fix conflicts and then commit the result.
```

---

## 3. Anatomy of Git Conflict Markers

Git injects three conflict delimiters directly into the file:

```python
<<<<<<< HEAD
    # Branch: main (Current branch)
    if len(password) < 6 or not any(char in "!@#$%^&*" for char in password):
        return {"success": False, "message": "Password requires 6 chars and a special symbol."}
=======
    # Branch: feature-strict-password (Incoming branch)
    if len(password) < 8 or not any(char.isupper() for char in password):
        return {"success": False, "message": "Password requires 8 chars and an uppercase letter."}
>>>>>>> feature-strict-password
```

### Explanation of Markers:
1. `<<<<<<< HEAD` : Marks the beginning of the conflicting lines from the current branch (`main`).
2. `=======` : The separator between the two conflicting versions.
3. `>>>>>>> <branch-name>` : Marks the end of conflicting lines from the incoming branch being merged.

---

## 4. Step-by-Step Resolution Process

### Step 1: Detect and Identify Conflicted Files
Check Git status to list all unmerged paths:
```bash
git status
```
*Output:*
```text
Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   signup.py
```

### Step 2: Open and Edit the File to Resolve the Conflict
Open `signup.py` in your code editor. Discuss with the team to synthesize the best requirements. 
Suppose the team agrees that passwords should be at least **8 characters** long AND contain an uppercase letter:

**Resolved Code (clean drop-in with conflict markers removed):**
```python
    # Final Resolved Implementation:
    if len(password) < 8 or not any(char.isupper() for char in password):
        return {
            "success": False, 
            "message": "Password must be at least 8 characters long and contain an uppercase letter."
        }
```

> **CRITICAL RULE:** All conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) MUST be completely deleted!

### Step 3: Run Tests to Verify the Resolution
Never commit without testing!
```bash
python -m unittest test_signup.py
```

### Step 4: Stage the Resolved File
Staging tells Git that the conflict in this file is resolved:
```bash
git add signup.py
git status
```
*Output:*
```text
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)
```

### Step 5: Conclude the Merge Commit
Complete the merge with a clear commit message:
```bash
git commit -m "Merge branch 'feature-strict-password': resolve password length validation conflict"
```

---

## 5. Safe Interactive Simulation Script

To see this in action without modifying the working `signup.py`, run our included safe simulation script:
```bash
python Q1_Feature_Branch_Signup/demo_conflict.py
```
This script creates a temporary isolated sandbox, initializes a dummy repo, creates conflicting commits on two branches, triggers a real Git conflict, inspects the markers, resolves it programmatically, and verifies the clean merge history.
