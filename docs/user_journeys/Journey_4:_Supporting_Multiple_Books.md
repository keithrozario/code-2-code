
# Journey 4: Supporting Multiple Books

## 1. Detailed User Journeys and Flows

This document outlines the user journeys for managing multiple books within the moneynote-api.

### Journey 4.1: Creating a New Book

**Objective:** To allow a user to create a new book for organizing their financial records.

**Flow:**

1.  **Start:** The user initiates the creation of a new book.
2.  **User Action:** The user provides the following information:
    *   `name`: The name of the book (e.g., "Personal Finances", "Business Expenses").
    *   `defaultCurrencyCode`: The default currency for the book (e.g., "USD", "EUR").
    *   `notes`: Optional notes for the book.
    *   `sort`: An integer for sorting purposes.
    *   `defaultExpenseAccountId`: Optional default account for expenses.
    *   `defaultIncomeAccountId`: Optional default account for income.
    *   `defaultTransferFromAccountId`: Optional default account for transfers from.
    *   `defaultTransferToAccountId`: Optional default account for transfers to.
3.  **System Response:**
    *   The system validates the provided data.
    *   A new `Book` record is created in the database.
    *   The system returns a success message.
4.  **End:** The new book is created and available for use.

### Journey 4.2: Viewing a List of Books

**Objective:** To allow a user to view a list of all their books.

**Flow:**

1.  **Start:** The user navigates to the books list view.
2.  **System Response:**
    *   The system retrieves all books associated with the user's group.
    *   The system displays a list of books with their details.
3.  **End:** The user can see all their books.

### Journey 4.3: Updating a Book

**Objective:** To allow a user to update the details of an existing book.

**Flow:**

1.  **Start:** The user selects a book to update.
2.  **User Action:** The user modifies the book's details (name, notes, default accounts, etc.).
3.  **System Response:**
    *   The system validates the provided data.
    *   The corresponding `Book` record is updated in the database.
    *   The system returns a success message.
4.  **End:** The book's details are updated.

### Journey 4.4: Deleting a Book

**Objective:** To allow a user to delete a book.

**Flow:**

1.  **Start:** The user selects a book to delete.
2.  **System Response:**
    *   The system checks if the book has any associated transactions. If so, deletion is prevented.
    *   The system deletes the `Book` record from the database.
    *   The system returns a success message.
3.  **End:** The book is deleted.

### Journey 4.5: Creating a Book from a Template

**Objective:** To allow a user to create a new book based on a predefined template.

**Flow:**

1.  **Start:** The user chooses to create a new book from a template.
2.  **User Action:** The user selects a template and provides a name for the new book.
3.  **System Response:**
    *   The system creates a new book with the categories, tags, and payees from the selected template.
    *   The system returns a success message.
4.  **End:** A new book is created with pre-populated data.

### Journey 4.6: Copying a Book

**Objective:** To allow a user to create a new book by copying an existing one.

**Flow:**

1.  **Start:** The user chooses to copy an existing book.
2.  **User Action:** The user selects a source book and provides a name for the new book.
3.  **System Response:**
    *   The system creates a new book and copies the categories, tags, and payees from the source book.
    *   The system returns a success message.
4.  **End:** A new book is created as a copy of the source book.

## 2. Detailed Object Level Data Structures

### `Book` Entity

| Attribute                      | Data Type       | Constraints/Properties | Description                                      |
| ------------------------------ | --------------- | ---------------------- | ------------------------------------------------ |
| `id`                           | `Integer`       | `PRIMARY KEY`          | The unique identifier for the book.              |
| `name`                         | `String`        | `NOT NULL`             | The name of the book.                            |
| `group`                        | `Group`         | `ManyToOne`, `NOT NULL`| The group to which the book belongs.             |
| `notes`                        | `String`        | `length = 1024`        | Optional notes for the book.                     |
| `enable`                       | `Boolean`       | `NOT NULL`             | Whether the book is enabled or not.              |
| `defaultExpenseAccount`        | `Account`       | `ManyToOne`            | The default account for expenses.                |
| `defaultIncomeAccount`         | `Account`       | `ManyToOne`            | The default account for income.                  |
| `defaultTransferFromAccount`   | `Account`       | `ManyToOne`            | The default account for transfers from.          |
| `defaultTransferToAccount`     | `Account`       | `ManyToOne`            | The default account for transfers to.            |
| `defaultExpenseCategory`       | `Category`      | `OneToOne`             | The default category for expenses.               |
| `defaultIncomeCategory`        | `Category`      | `OneToOne`             | The default category for income.                 |
| `defaultCurrencyCode`          | `String`        | `NOT NULL`, `length = 8`| The default currency for the book.               |
| `exportAt`                     | `Long`          |                        | The timestamp of the last export operation.      |
| `sort`                         | `Integer`       |                        | The sort order of the book.                      |
| `tags`                         | `List<Tag>`     | `OneToMany`            | The tags associated with the book.               |
| `categories`                   | `List<Category>`| `OneToMany`            | The categories associated with the book.         |
| `payees`                       | `List<Payee>`   | `OneToMany`            | The payees associated with the book.             |

## 3. Database Tables to be Updated

*   `t_user_book`: This table is the primary table for storing book information. It is read from, written to, and updated during book management operations.
*   `t_category`: This table is updated when a book is created from a template or copied, as categories are created for the new book. It is also affected when a book is deleted.
*   `t_tag`: This table is updated when a book is created from a template or copied, as tags are created for the new book. It is also affected when a book is deleted.
*   `t_payee`: This table is updated when a book is created from a template or copied, as payees are created for the new book. It is also affected when a book is deleted.
*   `t_balance_flow`: This table is read from when checking if a book can be deleted.

## 4. Business Rules and Functionality (Detailed)

### Rule 1: Book Name Uniqueness

*   **Rule Name:** `UniqueBookName`
*   **Description:** Within the same group, each book must have a unique name.
*   **Triggering Event:** Creating or updating a book.
*   **Logic/Conditions:** Before creating or updating a book, the system checks if another book with the same name already exists in the same group.
*   **Outcome/Action:** If a book with the same name exists, the operation is blocked, and an error message is displayed.

### Rule 2: Maximum Number of Books

*   **Rule Name:** `MaxBookCount`
*   **Description:** A user's group can have a limited number of books.
*   **Triggering Event:** Creating a new book.
*   **Logic/Conditions:** Before creating a new book, the system checks if the number of existing books in the group has reached the maximum limit.
*   **Outcome/Action:** If the maximum limit is reached, the creation is blocked, and an error message is displayed.

### Rule 3: Deleting a Book with Transactions

*   **Rule Name:** `NoDeleteBookWithTransactions`
*   **Description:** A book cannot be deleted if it has associated financial transactions.
*   **Triggering Event:** Deleting a book.
*   **Logic/Conditions:** Before deleting a book, the system checks if there are any records in the `t_balance_flow` table associated with the book.
*   **Outcome/Action:** If transactions exist, the deletion is blocked, and an error message is displayed.

## 5. Detailed Test Cases

| Test Case ID | Feature Being Tested      | Preconditions                               | Test Steps                                                              | Test Data                               | Expected Result                                                              |
| ------------ | -------------------------- | ------------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------- |
| TC-BOOK-001  | Create a new book (Happy Path) | The user is logged in.                      | 1. Navigate to the "add book" page. 2. Fill in the required fields. 3. Click "Save". | `name`: "My New Book", `defaultCurrencyCode`: "USD" | The book is created successfully.                                            |
| TC-BOOK-002  | Create a new book (Negative Path) | A book with the name "Existing Book" already exists. | 1. Navigate to the "add book" page. 2. Fill in the name with "Existing Book". 3. Click "Save". | `name`: "Existing Book"                 | An error message is displayed, and the book is not created.                  |
| TC-BOOK-003  | Delete a book (Negative Path) | The book has associated transactions.       | 1. Navigate to the book list. 2. Select the book to delete. 3. Click "Delete". | -                                       | An error message is displayed, and the book is not deleted.                  |

## 6. State Any Assumptions

*   It is assumed that the `Limitation.book_max_count` constant defines the maximum number of books a group can have.
*   It is assumed that the front-end application correctly handles the display of error messages and user feedback.
*   It is assumed that the `BookTplDataLoader` correctly loads the book templates from an external source.
