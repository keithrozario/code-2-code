# Journey 4: Supporting Multiple Books

## 1. Detailed User Journeys and Flows

This journey describes how a user can create and manage separate financial ledgers, called "Books," to segregate different areas of their financial life, such as personal expenses, a side business, or a specific project.

### User Story

As a user with diverse financial activities, I want to maintain separate "books" for different areas of my life (e.g., personal, business, vacation) so that I can keep my financial records organized, avoid mixing personal and business expenses, and generate reports for each area independently.

### Flow 1: Creating a New Book from a Template

This flow describes how a user creates a new book using a predefined template.

*   **Start:** The user is logged into the application and is on any page.
*   **Step 1: Navigate to Book Management:** The user navigates to the "Settings" or "Manage Books" section of the application.
*   **Step 2: Initiate Book Creation:** The user clicks the "Add Book" or "Create New Book" button.
*   **Step 3: Choose Creation Method:** The system presents options for creating a book. The user selects "Create from Template."
*   **Step 4: Select a Template:** The user is shown a list of available templates (e.g., "Daily Life," "Restaurant Business," "Travel"). The user selects a template that fits their needs.
*   **Step 5: Configure the New Book:** A form appears where the user enters a **Name** for the new book (e.g., "My Side Hustle") and selects a **Default Currency** (e.g., "USD").
*   **Step 6: Finalize Creation:** The user clicks "Create" or "Save."
*   **System Response:** The system creates the new book, pre-populated with the categories, tags, and payees defined in the selected template.
*   **End:** The new book appears in the user's list of available books. The user can now switch to it to start recording transactions.

### Flow 2: Creating a New Book by Copying an Existing One

This flow describes how a user creates a new book by duplicating the structure of one of their existing books.

*   **Start:** The user is in the "Manage Books" section.
*   **Step 1: Initiate Book Creation:** The user clicks "Add Book."
*   **Step 2: Choose Creation Method:** The user selects "Copy Existing Book."
*   **Step 3: Select Source Book:** The user is shown a list of their existing books. They select the one they want to copy (e.g., "Personal Finances").
*   **Step 4: Configure the New Book:** The user provides a **Name** for the new book (e.g., "Vacation 2025") and can override the **Default Currency**.
*   **Step 5: Finalize Creation:** The user clicks "Create."
*   **System Response:** The system creates the new book and copies all categories, tags, and payees from the source book into the new one. No transactions are copied.
*   **End:** The new book is ready for use with the same organizational structure as the source book.

### Flow 3: Switching Between Books

This flow describes how a user changes their active context from one book to another.

*   **Start:** The user is actively using the application, with one book currently active (e.g., "Personal Finances").
*   **Step 1: Access Book Switcher:** The user clicks on a dropdown menu or navigation item that lists all their available books.
*   **Step 2: Select New Book:** The user selects a different book from the list (e.g., "My Side Hustle").
*   **System Response:** The application's entire context switches to the selected book. The dashboard, transaction lists, reports, and data entry forms now exclusively show and operate on the data within "My Side Hustle." The user's session is updated to reflect this new active book.
*   **End:** The user can now record and view transactions within the newly selected book.

## 2. Detailed Object Level Data Structures

The core data entity for this journey is the `Book`.

### `Book` (`t_user_book` table)

Represents a single, self-contained financial ledger.

| Attribute Name | Data Type | Constraints & Properties | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | Unique identifier for the book. |
| `name` | `VARCHAR(64)` | `NOT NULL` | The user-defined name of the book (e.g., "Personal Finances"). |
| `group_id` | `INTEGER` | `NOT NULL`, `FOREIGN KEY` -> `t_user_group(id)` | The group this book belongs to. |
| `notes` | `VARCHAR(1024)` | `NULLABLE` | Optional descriptive notes for the book. |
| `enable` | `BOOLEAN` | `NOT NULL`, `defaultValue: true` | Flag to enable or disable the book. |
| `default_expense_account_id` | `INTEGER` | `FOREIGN KEY` -> `t_user_account(id)` | Default account to use for new expense transactions. |
| `default_income_account_id` | `INTEGER` | `FOREIGN KEY` -> `t_user_account(id)` | Default account to use for new income transactions. |
| `default_transfer_from_account_id` | `INTEGER` | `FOREIGN KEY` -> `t_user_account(id)` | Default source account for transfers. |
| `default_transfer_to_account_id` | `INTEGER` | `FOREIGN KEY` -> `t_user_account(id)` | Default destination account for transfers. |
| `default_expense_category_id` | `INTEGER` | `FOREIGN KEY` -> `t_user_category(id)` | Default category for new expenses. |
| `default_income_category_id` | `INTEGER` | `FOREIGN KEY` -> `t_user_category(id)` | Default category for new incomes. |
| `default_currency_code` | `VARCHAR(8)` | `NOT NULL` | The default currency for reporting and data entry in this book. |
| `export_at` | `BIGINT` | `NULLABLE` | Timestamp of the last time the book's data was exported. |
| `sort` | `INTEGER` | `NULLABLE` | A number used for custom sorting of the book list. |

**Relationships:**

*   **One-to-Many:** A `Book` has many `Tag`s, `Category`s, and `Payee`s.
*   **Many-to-One:** A `Book` belongs to one `Group`.

## 3. Database Tables to be Updated

| User Journey / Flow | Table Name | Operations | Description |
| :--- | :--- | :--- | :--- |
| **Create New Book** | `t_user_book` | `INSERT` | A new record is inserted into the book table. |
| | `t_user_category` | `INSERT` | If creating from a template or copying, new category records are inserted and linked to the new book's ID. |
| | `t_user_tag` | `INSERT` | If creating from a template or copying, new tag records are inserted and linked to the new book's ID. |
| | `t_user_payee` | `INSERT` | If creating from a template or copying, new payee records are inserted and linked to the new book's ID. |
| **Update Book** | `t_user_book` | `UPDATE` | The name, notes, or default accounts/categories of an existing book are updated. |
| **Delete Book** | `t_user_book` | `DELETE` | The book record is deleted. This is only allowed if no transactions are linked to it. |
| | `t_user_category` | `DELETE` | All categories associated with the book are deleted. |
| | `t_user_tag` | `DELETE` | All tags associated with the book are deleted. |
| | `t_user_payee` | `DELETE` | All payees associated with the book are deleted. |
| **Switch Active Book** | `t_user_user` | `UPDATE` | The `default_book_id` for the current user is updated to the ID of the newly selected book. |
| **Read Book List** | `t_user_book` | `SELECT` | The system reads all books belonging to the user's current group to display them in a list. |

## 4. Business Rules and Functionality (Detailed)

### Business Rules

| Rule Name/Identifier | Description | Triggering Event | Logic/Conditions | Outcome/Action |
| :--- | :--- | :--- | :--- | :--- |
| **Max Book Limit** | A user's group cannot have more than a predefined number of books. | User attempts to create a new book. | `bookRepository.countByGroup(group) >= Limitation.book_max_count` | The creation is blocked, and an error message ("book.max.count") is displayed. |
| **Unique Book Name** | Within the same group, all book names must be unique. | User creates or renames a book. | `bookRepository.existsByGroupAndName(group, newName)` | The operation fails with an "ItemExistsException". |
| **Deletion Constraint** | A book cannot be deleted if it contains any transaction records (`BalanceFlow`). | User attempts to delete a book. | `balanceFlowRepository.existsByBook(book)` | The deletion is blocked, and an error message ("book.delete.has.flow") is displayed. |
| **Default Book Deletion** | The default book of a group cannot be deleted. | User attempts to delete a book. | The book's ID matches the group's `default_book_id`. | The operation is blocked. (Note: The code for this appears to be commented out, but it is a standard business rule). |
| **Template Not Found** | A book cannot be created from a template that does not exist. | User attempts to create a book from a template. | The provided `templateId` does not match any ID in the loaded `book_tpl.json`. | The operation fails with an "ItemNotFoundException". |

### Validations

*   **Backend Validations:**
    *   When creating a book, the `name` and `defaultCurrencyCode` are mandatory.
    *   The `defaultCurrencyCode` must be a valid, known currency code.
    *   When creating from a template or copying, the source book/template must exist.
    *   When updating a book, if the name is changed, it is checked for uniqueness within the group.

## 5. Test Cases

| Test Case ID | Feature Being Tested | Preconditions | Test Steps | Test Data | Expected Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-BOOK-01** | Create New Book (Happy Path) | User is logged in. | 1. Navigate to "Manage Books". <br> 2. Click "Add Book". <br> 3. Fill in the form. <br> 4. Click "Save". | Name: "Test Book", Default Currency: "JPY" | The book "Test Book" is created successfully and appears in the book list. |
| **TC-BOOK-02** | Create Book with Duplicate Name (Negative Path) | User has an existing book named "Test Book". | 1. Navigate to "Manage Books". <br> 2. Click "Add Book". <br> 3. Fill in the form with the same name. <br> 4. Click "Save". | Name: "Test Book", Default Currency: "JPY" | An error message is displayed indicating the book name already exists. The book is not created. |
| **TC-BOOK-03** | Create Book from Template | User is logged in. | 1. Navigate to "Manage Books". <br> 2. Click "Add Book" and select "From Template". <br> 3. Choose the "Daily Life" template. <br> 4. Name the book "My Life". <br> 5. Click "Create". | Template: "Daily Life", Name: "My Life" | A new book "My Life" is created, populated with all categories and tags from the "Daily Life" template. |
| **TC-BOOK-04** | Delete Book with Transactions (Negative Path) | A book named "Project X" exists and has at least one transaction recorded in it. | 1. Navigate to "Manage Books". <br> 2. Find "Project X" in the list. <br> 3. Click the "Delete" button. | N/A | An error message is displayed, stating that a book with transactions cannot be deleted. The book remains. |
| **TC-BOOK-05** | Delete Empty Book (Happy Path) | A book named "Empty Book" exists and has no transactions. | 1. Navigate to "Manage Books". <br> 2. Find "Empty Book" in the list. <br> 3. Click the "Delete" button. | N/A | The book "Empty Book" is successfully deleted from the list. |
| **TC-BOOK-06** | Switch Active Book | User has at least two books: "Personal" (default) and "Business". | 1. Click on the book switcher dropdown. <br> 2. Select "Business". | N/A | The application view refreshes. The dashboard and transaction list now show data only from the "Business" book. The book switcher now indicates "Business" is active. |

## 6. Assumptions

*   It is assumed that the `Limitation.book_max_count` constant is configured to a reasonable number to prevent performance degradation from an excessive number of books.
*   It is assumed that the `book_tpl.json` file is always present in the application's classpath and is well-formed.
*   It is assumed that when a user's default book is disabled, the logic to revert their default to the group's default book is sufficient to prevent them from being locked into an unusable context.
*   It is assumed that the frontend UI correctly disables the "Delete" button for a book that is set as the group's default, as the backend logic for this check is present but commented out in the `remove` method.
