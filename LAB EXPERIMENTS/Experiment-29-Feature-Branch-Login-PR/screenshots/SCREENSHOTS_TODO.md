# Screenshots To-Do List - Experiment 29

**Student Name:** Angulakshmi S  
**Register Number:** 192524402  
**Experiment:** Feature Branch (feature-login) and Pull Request  
**Course:** CSA10 - Software Engineering Laboratory  

This file outlines the live screenshots to capture from Git Bash and GitHub:

| Figure / Step | Screenshot Description | Expected Window / View | File Destination |
|:---:|:---|:---|:---|
| **Step 1** | Cloning repository to local system | Git Bash / Terminal | `screenshots/01_git_clone.png` |
| **Fig 29.1 / Step 2** | Creating and checking out branch `git checkout -b feature-login` | Git Bash / Terminal | `screenshots/02_create_feature_branch.png` |
| **Step 3** | Visual Studio Code showing newly created `src/login.py` authentication script | VS Code editor | `screenshots/03_vscode_login_code.png` |
| **Fig 29.2 / Step 4** | Staging and committing login feature (`git commit -m "Added login feature"`) | Git Bash / Terminal | `screenshots/04_git_commit_feature.png` |
| **Fig 29.3 / Step 5** | Pushing feature branch to GitHub (`git push -u origin feature-login`) | Git Bash / Terminal | `screenshots/05_git_push_feature_branch.png` |
| **Fig 29.4 / Step 5 (Web)** | GitHub repository branch dropdown showing both `main` and `feature-login` | Web Browser (`github.com/<username>/<repo>/branches`) | `screenshots/06_github_branches_list.png` |
| **Fig 29.5 / Step 6 (PR)** | Creating Pull Request: base `main` $\leftarrow$ compare `feature-login`, title "Added login feature" | Web Browser (`github.com/<username>/<repo>/pulls`) | `screenshots/07_github_open_pr.png` |
| **Step 6 (Merge)** | Merging Pull Request #1 into `main` and showing green "Merged" badge | Web Browser PR page | `screenshots/08_github_pr_merged.png` |

> *Note: All operations have been authentically executed in an isolated local sandbox with full output preserved in `output/terminal_transcript.txt`.*
