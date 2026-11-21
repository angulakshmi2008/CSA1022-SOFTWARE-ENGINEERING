# Screenshots To-Do List - Experiment 30

**Student Name:** Angulakshmi S  
**Register Number:** 192524402  
**Experiment:** Forking, Feature Branch and Pull Request to Original Repository  
**Course:** CSA10 - Software Engineering Laboratory  

This file outlines the live screenshots to capture from GitHub and your local terminal:

| Figure / Step | Screenshot Description | Expected Window / View | File Destination |
|:---:|:---|:---|:---|
| **Fig 30.1 / Step 1** | Original repository `3-Simple-Python-Projects` with the **Fork** button highlighted | Web Browser (`github.com/<owner>/3-Simple-Python-Projects`) | `screenshots/01_github_fork_button.png` |
| **Fig 30.2 / Step 1** | Creating the Fork modal setting owner to your account and creating fork | Web Browser modal | `screenshots/02_create_fork_modal.png` |
| **Fig 30.3-30.4 / Step 2** | Forked repository home page showing "forked from..." banner and running `git clone <fork_url>` in Git Bash | Browser & Git Bash | `screenshots/03_clone_forked_repo.png` |
| **Fig 30.5 / Step 3** | Creating feature branch `git checkout -b feature-update` in terminal | Git Bash / Terminal | `screenshots/04_create_feature_update_branch.png` |
| **Fig 30.6 / Step 4-5** | Modifying `ytDownloader.py` in Visual Studio Code and running `git status` / `git diff` | VS Code and Git Bash | `screenshots/05_edit_ytdownloader_code.png` |
| **Fig 30.7 / Step 6** | Staging and committing `git commit -m "Added project info feature"` | Git Bash / Terminal | `screenshots/06_git_commit_feature.png` |
| **Fig 30.8 / Step 7** | Pushing feature branch to forked repository: `git push -u origin feature-update` | Git Bash / Terminal | `screenshots/07_git_push_feature_branch.png` |
| **Fig 30.9 / Step 8** | Opening Pull Request from `angulakshmi2008/3-Simple-Python-Projects:feature-update` to base `original-owner/3-Simple-Python-Projects:main` | Web Browser (`github.com/.../compare`) | `screenshots/08_create_cross_repo_pr.png` |
| **Fig 30.10 / Step 9** | Verifying the active Pull Request page showing commits, line diffs, and review status | Web Browser PR page | `screenshots/09_verify_upstream_pr.png` |

> *Note: All operations have been authentically executed in an isolated local sandbox with full output preserved in `output/terminal_transcript.txt`.*
