# Part B — Analysis: UML Relationships, External Actors & Access Control

**Course:** Software Engineering (CSA10)  
**Question:** Q3 Part B (10 Marks)  
**Topic:** Justification of UML Include/Extend Relationships, External Payment Gateway Modeling, and Student Access Control  

---

## Question:
> *"Justify each include or extend relationship you used. Explain why the payment gateway is shown as an actor, and which use cases are available only to a logged-in student."*

---

## 1. Justification of UML `<<include>>` and `<<extend>>` Relationships

In UML 2.5 Use Case diagrams, dependencies between use cases capture commonality, modularity, and conditional behaviors.

### A. Justification of `<<include>>` Relationships (Mandatory Inclusion)
An **`<<include>>`** dependency signifies that the base use case **unconditionally incorporates** the behavior of the included use case. The base use case cannot reach successful completion without the execution of the included use case. The arrow points **from the base use case to the included use case** (`Base` $\dashrightarrow$ `Included`).

1. **`Enrol in Course` $\xrightarrow{<<include>>}$ `Process Payment` (for paid courses):**
   - *Justification:* When a student enrols in a paid course, financial transaction authorization is an indispensable sub-process. Enrolment cannot be finalized, and course access cannot be granted, until payment authorization is successfully returned by the payment gateway. Extracting payment into its own included use case also promotes modular reuse across any future payment-enabled feature (such as purchasing e-books or 1-on-1 tutoring).
2. **`Download Completion Certificate` $\xrightarrow{<<include>>}$ `Verify Course Requirements`:**
   - *Justification:* Generating an academic certificate without verifying eligibility violates institutional integrity. The platform must execute an automated audit verifying that all video lectures were watched, passing marks were attained on all quizzes, and all mandatory assignments were submitted. This verification is mandatory and always precedes certificate issuance.

---

### B. Justification of `<<extend>>` Relationships (Optional / Conditional Behavior)
An **`<<extend>>`** relationship models **optional, conditional, or auxiliary behavior** that executes only if a specific extension point or condition is met. The base use case can execute completely without ever triggering the extension. By UML convention, the arrow points **from the extension use case to the base use case** (`Extension` $\dashrightarrow$ `Base`).

1. **`Apply Discount Coupon` $\xrightarrow{<<extend>>}$ `Enrol in Course`:**
   - *Justification:* Applying a promotional code or scholarship voucher is completely optional. A student can enrol in a course by paying full price without ever providing a coupon. Only when the condition `[student possesses a valid promotional code]` is satisfied at the checkout extension point does this use case execute.
2. **`Ask Doubt in Discussion Forum` $\xrightarrow{<<extend>>}$ `Watch Lectures`:**
   - *Justification:* While viewing a video lesson, a student may simply watch the video to completion without asking any questions. Posting a question in the course discussion thread is an optional interactive behavior triggered only when the student encounters a doubt `[student has a query]`.

---

## 2. Why the Payment Gateway is Shown as an Actor

According to the **OMG Unified Modeling Language (UML) Specification**:
- An **Actor** represents any entity that is **external to the system boundary** and interacts with the system to exchange information or request/provide services.
- Actors are **not limited to human beings**; external software applications, third-party APIs, and external hardware systems that interact across the boundary are recognized as system actors.

### Specific Reasons Why the Payment Gateway is an Actor:
1. **External Boundary Placement:** The payment gateway (e.g., Stripe, PayPal, Razorpay) is hosted, operated, and maintained by a third-party banking/financial infrastructure. It lies completely outside the jurisdiction and code base of the E-Learning Platform.
2. **Autonomous Entity Providing Critical Services:** The e-learning platform does not store sensitive credit card or banking credentials directly (for PCI-DSS compliance). Instead, our system delegates financial authorization to the payment gateway actor, which authenticates the transaction, debits the account, and transmits an asynchronous callback/webhook confirming approval.
3. **Cannot Be Modeled as an Internal Use Case:** A use case represents functionality *performed by our software*. Because our software cannot internally authorize bank credit cards or clear funds, treating payment processing as an internal use case without an external actor would misrepresent system responsibilities.

---

## 3. Access Control: Publicly Available vs. Logged-in Student Use Cases

A fundamental principle of software engineering and security architecture is **Role-Based Access Control (RBAC)**.

```
+---------------------------------------------------------------------------------+
|                                 VISITOR / GUEST                                  |
|                                        │                                        |
|                          Browse Course Catalogue (Public)                       |
+----------------------------------------┬----------------------------------------+
                                         │
                                [Student Login / Auth]
                                         │
+----------------------------------------▼----------------------------------------+
|                               LOGGED-IN STUDENT ONLY                            |
|  • Enrol in Course             • Watch Lectures          • Attempt Quizzes      |
|  • Submit Assignments          • Download Completion Certificate                |
+---------------------------------------------------------------------------------+
```

### A. Publicly Available Use Case (No Login Required)
- **`Browse Course Catalogue`:**  
  Any anonymous internet guest or prospective student can visit the landing page, search courses, view syllabi, read instructor bios, inspect pricing, and view reviews. Requiring login before browsing would deter new user acquisition.

### B. Use Cases Available Only to a Logged-in Student (Authentication Mandatory)
All other student operations require verified authentication:

1. **`Enrol in Course`:** Requires user identity to bind the user's account to the course roster, issue a student profile, and associate billing invoices.
2. **`Watch Lectures`:** Streaming video lectures is proprietary, paid/enrolled content. Authentication is mandatory to prevent unauthorized video scraping, verify active enrollment, and track individual progress.
3. **`Attempt Quizzes`:** Requires an authenticated student ID to record assessment grades, track remaining attempt allowances, and prevent academic impersonation.
4. **`Submit Assignments`:** Requires student identity to map uploaded code or files to the student's gradebook record for instructor grading.
5. **`Download Completion Certificate`:** Requires authentication to print the student's legal name, issue an official cryptographic verification hash, and record the degree/certificate in institutional archives.

---

## 4. Key Summary for Lab Viva

| Component | Classification / Justification |
| :--- | :--- |
| **`<<include>>`** | Mandatory execution; base cannot finish without it (`Enrol` $\rightarrow$ `Payment`, `Certificate` $\rightarrow$ `Verify`). |
| **`<<extend>>`** | Optional execution triggered by condition (`Coupon` $\rightarrow$ `Enrol`, `Forum Doubt` $\rightarrow$ `Watch`). |
| **External Actor** | Payment Gateway is outside system boundary; provides external banking service via APIs. |
| **Public Access** | Only `Browse Course Catalogue` is public. |
| **Protected Access** | `Enrol`, `Watch`, `Quiz`, `Assignment`, `Certificate` strictly require a logged-in student account. |
