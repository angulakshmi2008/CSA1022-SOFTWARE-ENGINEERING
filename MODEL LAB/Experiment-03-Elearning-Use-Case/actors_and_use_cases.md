# Q3 — E-Learning Platform: Actors, Use Cases & Relationships Specification

**Course:** Software Engineering (CSA10)  
**Topic:** UML Use Case Modeling for Online Learning Management System (LMS)  
**Assessment:** Model Practical – Set 2  

---

## 1. System Boundary

- **System Name:** `E-Learning Platform`
- **Boundary Scope:** Defines all internal software capabilities, business logic, user services, and administrative interfaces.
- **External Environment:** Third-party financial systems (Payment Gateway) and human end-users interact across this boundary.

---

## 2. Actor Profiles & Classifications

| Actor Name | Type | Description & System Responsibilities |
| :--- | :---: | :--- |
| **Student** | Primary Human Actor | Registered learner who accesses learning materials, enrols in free/paid courses, streams video lectures, completes quizzes, submits assignments, and downloads certificates. |
| **Instructor** | Primary Human Actor | Subject matter expert who authors courses, uploads lecture video modules, designs interactive quizzes, and oversees academic content. |
| **Administrator** | Primary Human Actor | System super-user responsible for user account governance (students/instructors), role authorizations, course catalogue approvals, and platform compliance. |
| **External Payment Gateway** | Secondary External System Actor | External third-party financial clearinghouse (e.g., Stripe, PayPal, Razorpay) responsible for authenticating payment methods, processing monetary charges, and returning transaction verification tokens. |

---

## 3. Comprehensive Use Case Inventory

### A. Student-Facing Use Cases

1. **Browse Course Catalogue (Public):**
   - *Description:* Allows any visitor or authenticated user to search, view course syllabi, instructor profiles, reviews, and pricing.
   - *Authentication Required:* **No** (Publicly accessible).

2. **Enrol in Course:**
   - *Description:* Student registers for a selected course. Triggers `Process Payment` if the course has a non-zero fee.
   - *Authentication Required:* **Yes** (Logged-in student).

3. **Watch Lectures:**
   - *Description:* Streams high-definition video lessons and tracks playback progress.
   - *Authentication Required:* **Yes** (Must be logged in and enrolled in the course).

4. **Attempt Quizzes:**
   - *Description:* Takes time-bound assessment quizzes associated with course modules.
   - *Authentication Required:* **Yes** (Must be logged in and enrolled).

5. **Submit Assignments:**
   - *Description:* Uploads homework, code projects, or documents for instructor evaluation.
   - *Authentication Required:* **Yes** (Must be logged in and enrolled).

6. **Download Completion Certificate:**
   - *Description:* Generates and downloads an authenticated PDF certificate upon successfully fulfilling course completion criteria.
   - *Authentication Required:* **Yes** (Must be logged in and verified).

---

### B. Instructor-Facing Use Cases

7. **Upload Lecture Videos / Courses:**
   - *Description:* Publishes new course curricula, descriptions, and video lecture files to the platform staging environment.
   - *Authentication Required:* **Yes** (Instructor credentials required).

8. **Create Quizzes:**
   - *Description:* Configures multiple-choice questions, answer keys, passing scores, and attempt limits for course assessments.
   - *Authentication Required:* **Yes** (Instructor credentials required).

---

### C. Administrator-Facing Use Cases

9. **Manage Users:**
   - *Description:* Creates, activates, suspends, or modifies student and instructor accounts and permissions.
   - *Authentication Required:* **Yes** (Platform Administrator credentials required).

10. **Approve New Courses:**
    - *Description:* Reviews course content uploaded by instructors for quality, copyright compliance, and academic rigor before making them publicly live in the catalogue.
    - *Authentication Required:* **Yes** (Platform Administrator credentials required).

---

### D. External Actor & Specialized Sub-Use Cases

11. **Process Payment:**
    - *Description:* Transmits purchase details to the external payment gateway, securely captures credit card/UPI transactions, and returns authorization confirmation.
    - *Initiator:* Included by `Enrol in Course` (when course is paid).
    - *Interacting Actor:* **External Payment Gateway**.

12. **Apply Discount Coupon:**
    - *Description:* Validates and applies a promotional discount code to reduce course fees before payment processing.
    - *Relationship:* Extends `Enrol in Course`.

13. **Ask Doubt in Discussion Forum:**
    - *Description:* Allows a student to post a question or timestamped doubt while watching a lecture.
    - *Relationship:* Extends `Watch Lectures`.

14. **Verify Course Requirements:**
    - *Description:* Automated audit confirming that 100% of lectures are watched, all quizzes are passed, and all assignments are submitted.
    - *Relationship:* Included by `Download Completion Certificate`.

---

## 4. Use Case Relationships Analysis Table

| Relationship | Base Use Case | Target Use Case | Condition / Justification |
| :---: | :--- | :--- | :--- |
| `<<include>>` | `Enrol in Course` | `Process Payment` | **Mandatory:** When a student enrols in a paid course, financial authorization via the gateway must execute. Enrolment cannot finalize without successful payment. |
| `<<include>>` | `Download Completion Certificate` | `Verify Course Requirements` | **Mandatory:** The platform cannot issue an accredited certificate without programmatically auditing that the student satisfied all completion benchmarks. |
| `<<extend>>` | `Enrol in Course` | `Apply Discount Coupon` | **Optional:** A student may choose to enter a promotional discount voucher during enrolment if they possess one. |
| `<<extend>>` | `Watch Lectures` | `Ask Doubt in Discussion Forum` | **Optional:** A student may post a doubt to the instructor/peer forum while watching a lecture. |
