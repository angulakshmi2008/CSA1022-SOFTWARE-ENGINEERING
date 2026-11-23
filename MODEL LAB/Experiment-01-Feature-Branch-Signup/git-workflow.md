# Git Feature Branch & Pull Request (PR) Workflow Guide

## 1. Overview & Industry Best Practice

In modern collaborative software engineering (and Agile/DevOps teams), developers never commit directly to the `main` (production) branch. Instead, they follow the **Feature Branch Workflow**:
1. Create a dedicated branch for each feature or bug fix (`feature-signup`).
2. Implement, test, and commit changes on that branch.
3. Push the feature branch to a remote Git host (like GitHub).
4. Open a **Pull Request (PR)** to request merging the feature into `main`.
5. Conduct peer code review, run automated CI tests, and approve.
6. Merge the pull request into `main` and delete the feature branch.

```
       (main) --- [Initial Commit] ------------------------------------> [PR Merge Commit] ---> (main)
                         \                                                     /
                          \---> [Commit 1] ---> [Commit 2: Tests] ------------/
                                 (branch: feature-signup)
```

---

## 2. Step-by-Step Local Git Implementation Executed in This Project

Because this laboratory project is maintained in an offline/local-first environment without performing an unapproved `git push`, the entire PR review lifecycle was executed locally using actual Git branching mechanics:

### Step 1: Base Branch Preparation
Ensure the repository is on the clean `main` branch:
```bash
git checkout main
git status
```

### Step 2: Create and Switch to the Feature Branch
Create the new branch named `feature-signup`:
```bash
git checkout -b feature-signup
# Or modern syntax:
# git switch -c feature-signup
```
*Verification:* Run `git branch` to confirm `feature-signup` is active (marked with `*`).

### Step 3: Implement Feature & Unit Tests
Created:
- `Q1_Feature_Branch_Signup/signup.py`
- `Q1_Feature_Branch_Signup/test_signup.py`

### Step 4: Run Automated Verification Tests
Verify all 13 unit test cases pass:
```bash
python -m unittest Q1_Feature_Branch_Signup/test_signup.py
```

### Step 5: Stage and Commit Changes on `feature-signup`
```bash
git add Q1_Feature_Branch_Signup/
git commit -m "feat(auth): implement signup function with username & 6-char password validation"
```

---

## 3. Pull Request Simulation & Local Code Review

On GitHub, a Pull Request provides a graphical diff view for teammates to inspect code before merging. Locally, we simulate this peer review using Git diff and log tools:

### Local PR Review Commands:
1. **Inspect Branch Differences (Diff Review):**
   ```bash
   git diff main..feature-signup
   ```
   *Review Checklist:*
   - [x] Are requirements met? (Username required, password $\ge 6$ characters).
   - [x] Are boundary conditions tested? (5 characters fail, 6 characters pass).
   - [x] Does the code adhere to style and clean code standards?
   - [x] Are tests automated and passing?

2. **Inspect Commit History on Feature Branch:**
   ```bash
   git log main..feature-signup --oneline
   ```

### Step 6: Merging the Feature into `main`
Once the simulated PR is reviewed and approved:
```bash
# 1. Switch back to main
git checkout main

# 2. Merge feature-signup with a dedicated merge commit (--no-ff preserves PR history)
git merge --no-ff feature-signup -m "Merge pull request #1 from feature-signup (Signup Feature)"

# 3. Verify the branch history graph
git log --graph --oneline --all
```

---

## 4. How to Execute a Real GitHub Pull Request (When Pushing Later)

When you are ready to push this repository to GitHub, follow these exact steps on the web platform:

1. **Push Both Branches to GitHub:**
   ```bash
   git remote add origin https://github.com/<your-username>/SE-Model-Practical-Set-2.git
   git push -u origin main
   git push -u origin feature-signup
   ```

2. **Navigate to GitHub Repository UI:**
   - GitHub will display a yellow banner: *"feature-signup had recent pushes - Compare & pull request"*.
   - Click **"Compare & pull request"**.

3. **Fill Out the Pull Request Details:**
   - **Base branch:** `main` $\leftarrow$ **Compare branch:** `feature-signup`
   - **Title:** `feat: Add user signup function with credential validation`
   - **Description:**
     ```markdown
     ## Summary of Changes
     - Implemented `signup(username, password)` in `signup.py`.
     - Added validation: username required, password length >= 6 characters.
     - Created 13 unit tests in `test_signup.py` covering boundary values.
     
     ## Verification
     - 13/13 unit tests passed locally.
     ```

4. **Peer Review & Branch Protection:**
   - Assign a reviewer (e.g., classmate or lab instructor).
   - GitHub Actions CI runs automated tests.
   - Reviewer clicks **"Files changed"**, reviews lines, and clicks **"Approve"**.

5. **Merge the PR:**
   - Click the green **"Merge pull request"** button.
   - Choose **"Create a merge commit"** (or Squash and Merge).
   - Confirm merge.
