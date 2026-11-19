# Screenshots To-Do List: Experiment 11 (Jira Cloud & Confluence)

To complete the lab record submission with native Atlassian web UI screenshots, follow these steps:

| Step # | Screen / View | Description to Capture | Target File Name |
|---|---|---|---|
| 1 | Jira Project Creation | Modal creating Jira project `"Library Management System"` (Key: `LMS`, Team-managed). | `screenshots/Figure_11.1_Create_Jira_Issues.png` |
| 2 | Jira Backlog View | Backlog tab displaying the 5 LMS development tasks: `LMS-1` through `LMS-5`. | `screenshots/Figure_11.2_Backlog_View.png` |
| 3 | Jira Active Sprint Board | Board showing task status distribution: 2 in **Done**, 1 in **In Progress**, 2 in **To Do**. | `screenshots/Figure_11.3_Verify_Issues.png` |
| 4 | Confluence Page Editor | Confluence editor creating page `"Library Management System Project Overview"`. | `screenshots/Figure_11.4_Create_Confluence_Page.png` |
| 5 | Published Confluence Page | Final published page showing the embedded Jira Macro issue table and visual progress bar (40% complete). | `screenshots/Figure_11.5_Submit_The_Output.png` |

---

### Step-by-Step Instructions:
1. In Atlassian Cloud, open **Jira Software** and create project `"Library Management System"` (Key: `LMS`).
2. Add the 5 development tasks:
   - `LMS-1`: Develop Book Search Functionality (`Done`)
   - `LMS-2`: Create User Login Page (`Done`)
   - `LMS-3`: Implement Book Borrowing Module (`In Progress`)
   - `LMS-4`: Design Librarian Dashboard (`To Do`)
   - `LMS-5`: Test Library Management System (`To Do`)
3. Open **Confluence** from the top-left app switcher.
4. Create a page titled `"Library Management System Project Overview"`.
5. Type `/jira` and configure the Jira issue macro:
   - Query: `project = LMS ORDER BY status DESC`
   - Display as Table (columns: Key, Summary, Assignee, Priority, Status).
6. Type `/status` or `/progress` to insert the visual progress bar showing `40% Complete`.
7. Click **Publish** and capture the complete screen using `Win + Shift + S`.
8. Save into this `screenshots/` directory.
