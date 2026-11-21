# Screenshots Required for Experiment 15: Working with Git Branches and Resolving Merge Conflicts

**Student Name:** Angulakshmi S  
**Register Number:** 192524402  
**Course:** CSA10 - Software Engineering  

If capturing live terminal and GitHub screenshots, please capture the following screens and place them in this `screenshots/` directory:

| Figure No. | Step Reference | Description to Capture | Recommended File Name |
| :--- | :--- | :--- | :--- |
| **Figure 15.1** | Step 1 & 2: Clone and Branch | Terminal showing `git clone <repo_url>`, `cd <repo>`, and `git checkout -b feature-update`. | `figure_15_1_clone_and_branch.png` |
| **Figure 15.2** | Step 3 & 4: Edit and Commit | Terminal showing `git status`, `git add README.md`, and `git commit -m "Updated README"`. | `figure_15_2_commit_feature.png` |
| **Figure 15.3** | Step 5: Push Feature Branch | Terminal showing `git push -u origin feature-update`. | `figure_15_3_push_feature.png` |
| **Figure 15.4** | Step 6 & 7: Pull Main Changes | Terminal showing `git checkout main` and `git pull origin main` with incoming changes from collaborator. | `figure_15_4_pull_main.png` |
| **Figure 15.5** | Step 8 & 9: Trigger Merge Conflict | Terminal showing `git checkout feature-update` and `git merge main` with `CONFLICT (content): Merge conflict in README.md`. | `figure_15_5_conflict_detected.png` |
| **Figure 15.6** | Step 10: VS Code Conflict Markers | Visual Studio Code editor highlighting the conflicting region with `<<<<<<< HEAD`, `=======`, and `>>>>>>> main`. | `figure_15_6_conflict_markers_vscode.png` |
| **Figure 15.7** | Step 11: Mark Resolved & Commit | Terminal showing `git add README.md`, `git commit -m "Resolved merge conflict"`, and clean `git status`. | `figure_15_7_commit_resolved_merge.png` |
| **Figure 15.8** | Step 12 & 13: Push & Pull Request | GitHub PR page showing `feature-update` into `main` with *"Able to merge - these branches can be automatically merged"*. | `figure_15_8_pr_no_conflicts.png` |

---
*Note: A complete, authentic Git execution transcript recorded in an isolated sandbox environment is available in [`output/terminal_transcript.txt`](../output/terminal_transcript.txt).*
