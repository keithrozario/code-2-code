# User Journey Analysis: Journey 4: Supporting Multiple Books

### 1.0 Detailed User Journeys and Flows
(Capture the step-by-step interactions a user has with the system to achieve the specific business goal of this journey. Document each distinct flow, including user actions, system responses, decision points, alternative paths, and error handling. Clearly identify start and end points.)

This journey enables users to segregate their financial records into distinct containers called "Books." This is essential for managing different financial contexts, such as personal finances, a side business, or a specific project, within a single user account.

**Flow 1: Creating a New Book**

*   **Start Point:** The user navigates to the "Manage Books" section of the application.
*   **User Action:** The user initiates the creation of a new book.
*   **Decision Point:** The user chooses one of three creation methods:
    1.  **From Scratch:** Create a new, empty book.
    2.  **From Template:** Create a book pre-populated with a structure from a predefined template (e.g., "Daily Life", "Restaurant Business").
    3.  **By Copying:** Create a new book by duplicating the structure (categories, tags, payees) of an existing book.

*   **Sub-Flow 1.1: Create From Scratch**
    1.  **User Action:** The user selects "Create From Scratch," provides a name (e.g., "Vacation Fund") and a default currency (e.g., "EUR").
    2.  **System Response:** The system validates that the book name is unique within the current user group.
    3.  **System Action:** A new `Book` record is created and saved to the `t_user_book` table.
    4.  **End Point:** The new book appears in the user's list of available books.

*   **Sub-Flow 1.2: Create From Template**
    1.  **User Action:** The user selects "Create From Template," chooses a template (e.g., "Daily Life"), provides a name, and sets a default currency.
    2.  **System Response:** The system validates the name and finds the selected template in the `book_tpl.json` file.
    3.  **System Action:** A new `Book` record is created. The system then iterates through the template's categories, tags, and payees, creating new records for each and associating them with the new book.
    4.  **End Point:** The new, pre-configured book appears in the user's list.

*   **Sub-Flow 1.3: Create by Copying**
    1.  **User Action:** The user selects "Create by Copying," chooses an existing book to copy from, provides a new name, and sets a default currency.
    2.  **System Response:** The system validates the new name and retrieves the structure of the source book.
    3.  **System Action:** A new `Book` record is created. The system then copies all categories, tags, and payees from the source book to the new book.
    4.  **End Point:** The new, duplicated book appears in the user's list.

*   **Error Handling:**
    *   If the book name already exists within the group, the system throws an `ItemExistsException` and displays an error.
    *   If the user attempts to create more books than the system limit (defined in `Limitation.book_max_count`), a `FailureMessageException` is thrown.

**Flow 2: Switching the Active Book**

*   **Start Point:** The user is operating within one book (e.g., "Personal Finances").
*   **User Action:** The user selects a different book (e.g., "Business") from a dropdown menu or navigation list.
*   **System Action:** The application calls the endpoint to set the default book for the user's session. The `UserService.setDefaultBook()` method updates the `default_book_id` on the `t_user_user` record for the current user.
*   **System Response:** The application interface refreshes, now showing the transactions, accounts, and reports scoped exclusively to the newly selected book.
*   **End Point:** The user is now operating within the context of the new active book.

**Flow 3: Deleting a Book**

*   **Start Point:** The user is in the "Manage Books" section.
*   **User Action:** The user selects a book and clicks the "Delete" button.
*   **System Response:** The system checks if the selected book has any associated `BalanceFlow` (transaction) records.
*   **Decision Point:**
    *   **If transactions exist:** The system throws a `FailureMessageException` with the message "book.delete.has.flow," preventing deletion.
    *   **If no transactions exist:** The system proceeds with deletion.
*   **System Action:** The system deletes all `Category`, `Payee`, and `Tag` records associated with the book. Finally, it deletes the `Book` record itself.
*   **End Point:** The book is removed from the user's list of books.

---

### 2.0 Detailed Object Level Data Structures
(Document the structure and attributes of key data entities involved in this journey. For each entity, list its attributes, data types, constraints (e.g., `NOT NULL`, `FOREIGN KEY`), and a brief description. Indicate relationships between entities.)

**Entity: `Book` (Table: `t_user_book`)**

Represents a single, self-contained ledger for financial records.

| Attribute | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | **Primary Key** | Unique identifier for the book. |
| `name` | `VARCHAR(64)` | `NOT NULL` | The user-defined name of the book. |
| `group_id` | `INTEGER` | `NOT NULL`, **FK** -> `t_user_group(id)` | The group this book belongs to. Establishes the ownership and multi-user context. |
| `notes` | `VARCHAR(1024)` | `NULLABLE` | Descriptive notes about the book. |
| `enable` | `BOOLEAN` | `NOT NULL`, Default: `true` | Flag to enable or disable the book. |
| `default_expense_account_id` | `INTEGER` | `NULLABLE`, **FK** -> `t_user_account(id)` | Default account to use for new expense transactions. |
| `default_income_account_id` | `INTEGER` | `NULLABLE`, **FK** -> `t_user_account(id)` | Default account for new income transactions. |
| `default_currency_code` | `VARCHAR(8)` | `NOT NULL` | The default currency for reporting and new transactions within this book. |
| `sort` | `INTEGER` | `NULLABLE` | An integer value used for sorting the list of books. |

**Relationships:**

*   **`Group` (Many-to-One):** A `Book` must belong to exactly one `Group`. A `Group` can have many `Book`s.
*   **`User` (Many-to-One via `defaultBook`):** A `User` has one default `Book`.
*   **`Category` (One-to-Many):** A `Book` has its own set of `Category` records.
*   **`Tag` (One-to-Many):** A `Book` has its own set of `Tag` records.
*   **`Payee` (One-to-Many):** A `Book` has its own set of `Payee` records.
*   **`BalanceFlow` (One-to-Many):** A `Book` contains many transaction records.

---

### 3.0 Database Tables to be Updated
(Identify which database tables are directly impacted by this user journey. List the tables that are read from and written to (`INSERT`, `UPDATE`, `DELETE`). Specify the operations performed on each table within the context of the journey.)

| Table Name | Operations | Context / Reason |
| :--- | :--- | :--- |
| **`t_user_book`** | `INSERT`, `UPDATE`, `DELETE`, `SELECT` | **Primary table for this journey.** Records are created when a new book is added, updated when its details are changed, deleted when a book is removed, and selected when listing or switching books. |
| **`t_user_user`** | `UPDATE`, `SELECT` | The `default_book_id` column is updated when a user switches their active book. The record is read to get the user's current context. |
| **`t_user_group`** | `SELECT` | Read to verify the user's group context and to enforce that a book name is unique within the group. |
| **`t_user_category`** | `INSERT`, `DELETE`, `SELECT` | Records are inserted when creating a book from a template or by copying. They are deleted when a book is removed. They are selected when copying a book. |
| **`t_user_tag`** | `INSERT`, `DELETE`, `SELECT` | Records are inserted when creating a book from a template or by copying. They are deleted when a book is removed. They are selected when copying a book. |
| **`t_user_payee`** | `INSERT`, `DELETE`, `SELECT` | Records are inserted when creating a book from a template or by copying. They are deleted when a book is removed. They are selected when copying a book. |
| **`t_user_balance_flow`**| `SELECT` | Read to check if any transactions exist for a book before allowing its deletion. |

---

### 4.0 Business Rules and Functionality (Detailed)
(Capture the explicit and implicit logic governing the system's behavior for this journey. For each rule, specify its name, description, trigger, logic, and outcome. Detail both front-end and back-end validations.)

| Rule Name | Description | Trigger | Logic | Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **Book Name Uniqueness** | A book's name must be unique within its parent `Group`. | Creating or updating a book. | The system queries the `t_user_book` table for an existing book with the same name and `group_id`. | If a book with the same name exists, an `ItemExistsException` is thrown, and the operation fails. |
| **Book Creation Limit** | A `Group` cannot have more than a predefined maximum number of books. | Creating a new book. | The system counts the number of existing books for the current `Group` and compares it to `Limitation.book_max_count`. | If the limit is reached, a `FailureMessageException` is thrown. |
| **Data Isolation** | `Category`, `Tag`, and `Payee` entities are strictly scoped to a single `Book`. | Creating a book from a template or by copying. | When a new book is created via template/copy, the system creates *new* `Category`, `Tag`, and `Payee` records and links them to the new book, rather than sharing them. | Ensures that changes to categories in one book do not affect another, providing complete financial segregation. |
| **Deletion Constraint** | A `Book` cannot be deleted if it contains any financial transactions (`BalanceFlow` records). | Attempting to delete a book. | The system queries the `t_user_balance_flow` table to check for any records where `book_id` matches the ID of the book being deleted. | If one or more transactions exist, a `FailureMessageException` is thrown, preventing deletion and data loss. |
| **Default Book Management** | Each user has a default book that determines their active context. | User logs in or manually switches their active book. | The `default_book_id` field on the `t_user_user` table is used to store and retrieve the user's active book. | The application's context is always scoped to the user's default book, ensuring they see the correct data. |
| **Template-Based Creation** | Users can create a book from a predefined structure. | User chooses "Create from Template". | The `BookService` loads `book_tpl.json`, finds the selected template, and programmatically creates all associated categories, tags, and payees for the new book. | A new book is created with a ready-to-use structure, saving the user manual setup time. |
| **Copy-Based Creation** | Users can duplicate an existing book's structure. | User chooses "Create by Copying". | The `BookService` reads all categories, tags, and payees from the source book and creates new, identical records linked to the new book. | A new book is created that is an exact structural replica of another book, useful for starting a new period (e.g., a new year). |

---

### 5.0 Test Cases
(Create a comprehensive set of test cases to verify the correct implementation of the user journey and its business rules. Each test case should include an ID, the feature being tested, preconditions, steps, test data, and expected results. Cover happy paths, negative paths, boundary conditions, and error handling.)

| Test Case ID | Feature Tested | Preconditions | Steps | Test Data | Expected Results |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-BOOK-01** | Create Book from Template | User is logged in. At least one book template exists in `book_tpl.json`. | 1. Navigate to "Manage Books". <br> 2. Select "Create from Template". <br> 3. Choose a template. <br> 4. Enter a unique name and select a currency. <br> 5. Save. | Name: "My Test Book", Template: "Daily Life", Currency: "USD" | A new book named "My Test Book" is created. It contains all the categories, tags, and payees defined in the "Daily Life" template. |
| **TC-BOOK-02** | Create Book by Copying | User is logged in. An existing book named "Source Book" exists with 5 categories and 3 tags. | 1. Navigate to "Manage Books". <br> 2. Select "Create by Copying". <br> 3. Choose "Source Book". <br> 4. Enter a new unique name. <br> 5. Save. | New Name: "Copied Book" | A new book named "Copied Book" is created. It has its own set of 5 categories and 3 tags that are identical in name and structure to those in "Source Book". |
| **TC-BOOK-03** | **(Negative)** Delete Book with Transactions | A book named "Active Book" exists and has at least one transaction record associated with it. | 1. Navigate to "Manage Books". <br> 2. Select "Active Book". <br> 3. Click "Delete". | Book ID for "Active Book" | The operation fails. The system displays an error message: "This book cannot be deleted because it has transaction records." |
| **TC-BOOK-04** | **(Negative)** Create Book with Duplicate Name | A book named "Existing Book" already exists in the user's current group. | 1. Navigate to "Manage Books". <br> 2. Select "Create Book". <br> 3. Enter the name "Existing Book". <br> 4. Save. | Name: "Existing Book" | The operation fails. The system displays an error message indicating that a book with this name already exists. |
| **TC-BOOK-05** | Switch Active Book | User has two books: "Book A" (default) and "Book B". | 1. From the main navigation, select "Book B". | Book ID for "Book B" | The application reloads. The displayed transactions, accounts, and reports are now scoped to "Book B". The user's `default_book_id` in the database is updated to the ID of "Book B". |
| **TC-BOOK-06** | Delete an Empty Book | A book named "Empty Book" exists and has no transactions. | 1. Navigate to "Manage Books". <br> 2. Select "Empty Book". <br> 3. Click "Delete". | Book ID for "Empty Book" | The book "Empty Book" and all its associated categories, tags, and payees are successfully deleted from the database. |

---

### 6.0 Assumptions
(Document any assumptions made during the analysis due to ambiguity or lack of definitive information. Explain the reasoning for each assumption.)

*   **User Authentication:** It is assumed that the user is already authenticated and their session (`CurrentSession`) is properly populated with their user and group context. The journey focuses on book management, not the login process.
*   **UI Implementation:** This analysis is based on the backend API and service logic. It is assumed that a corresponding frontend exists to expose these functionalities to the user through a graphical interface (e.g., forms, buttons, dropdowns).
*   **Template File Availability:** It is assumed that the `book_tpl.json` file is always present in the application's classpath and is correctly formatted. The `BookTplDataLoader` handles loading this file, but the analysis assumes it succeeds.
*   **Permissions:** It is assumed that the user has the necessary permissions within their group to create, edit, and delete books. The code does not show explicit role checks for book management, implying that any member of a group can manage books.
*   **Single-Tenancy Model:** The logic is scoped to a `Group`. It is assumed that a user operates within one active group at a time, and all book operations are confined to that group.
