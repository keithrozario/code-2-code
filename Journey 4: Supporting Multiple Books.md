# Journey 4: Supporting Multiple Books

This document details the user journey for managing multiple books within the MoneyNote application. A "Book" acts as a separate ledger, allowing users to segregate different financial areas (e.g., "Personal Finances," "Business," "Vacation Fund").

## 1. Detailed User Journey and Flows

This journey covers the creation, management, and utilization of multiple books.

### Journey 1: Creating a New Book

Users can create a new, empty book, create one from a predefined template, or clone the structure of an existing book.

**User Flow (Create from Template):**
1.  The user navigates to the "Settings" or "Manage Books" section.
2.  They click "Add Book" and choose the "From Template" option.
3.  The UI displays a list of available templates (e.g., "Default Personal Finance," "Small Business").
4.  The user selects a template and provides a **Name** for the new book. They can also add optional **Notes**.
5.  Upon saving, the system creates a new `Book` record.
6.  Crucially, the system also populates the new book with a default set of `Categories`, `Tags`, and `Payees` as defined in the selected `BookTemplate`.

**User Flow (Clone Existing Book):**
1.  The user follows steps 1-2 above but chooses the "Clone Existing Book" option.
2.  They select one of their existing books as the source.
3.  They provide a new **Name** for the cloned book.
4.  The system creates the new `Book` and copies over all `Categories`, `Tags`, and `Payees` from the source book. Financial transactions (`BalanceFlow` records) are **not** copied.

### Journey 2: Switching the Active Book

The application has a concept of a "current" or "active" book. All new transactions and data entries are recorded in the currently active book.

**User Flow:**
1.  The user clicks on a book switcher UI element, which might be a dropdown in the header or a dedicated menu.
2.  A list of all their available books is displayed.
3.  The user selects a different book from the list.
4.  The application's session is updated to set the selected book as the new "current book".
5.  The UI refreshes, displaying the dashboard, accounts, and transactions associated with the newly selected book. The user's `defaultBook` is also updated.

### Journey 3: Managing and Updating a Book

Users can modify the details of a book or disable it.

**User Flow:**
1.  The user navigates to the "Manage Books" section, which lists all their books.
2.  They select a book to edit.
3.  A form appears, allowing them to change:
    *   **Name**
    *   **Notes**
    *   **Default Currency**
    *   **Default accounts** for expenses, incomes, and transfers.
    *   **Default categories** for expenses and incomes.
    *   **Enable/Disable** status.
4.  The user saves the changes. The system updates the corresponding `Book` record in the database.

### Journey 4: Deleting a Book

A book can only be deleted if it contains no financial transactions.

**User Flow:**
1.  From the "Manage Books" list, the user selects the "Delete" option for a book.
2.  The system checks if any `BalanceFlow` records are associated with the book.
3.  **If transactions exist**, the API returns an error message (e.g., "Cannot delete a book with existing transactions").
4.  **If no transactions exist**, the system proceeds to delete all related `Categories`, `Tags`, and `Payees` for that book, and finally deletes the `Book` record itself.
5.  If the deleted book was the default for the user or group, the system intelligently resets the default to another available book.

## 2. Detailed Object-Level Data Structures

### `Book` Entity (`t_user_book` table)

This is the central entity for this journey.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary Key. |
| `group` | `Group` | (FK) The group this book belongs to. |
| `name` | `String` | The name of the book (e.g., "Personal Finances"). |
| `notes` | `String` | Optional descriptive notes. |
| `enable` | `Boolean` | Whether the book is active and can be used. |
| `defaultCurrencyCode` | `String` | The default currency for this book (e.g., "USD"). |
| `defaultExpenseAccount` | `Account` | (FK, Optional) Default account for new expenses. |
| `defaultIncomeAccount` | `Account` | (FK, Optional) Default account for new incomes. |
| `defaultTransferFromAccount`| `Account` | (FK, Optional) Default source account for transfers. |
| `defaultTransferToAccount` | `Account` | (FK, Optional) Default destination account for transfers. |
| `defaultExpenseCategory` | `Category`| (FK, Optional) Default category for new expenses. |
| `defaultIncomeCategory` | `Category`| (FK, Optional) Default category for new incomes. |
| `exportAt` | `Long` | Timestamp of the last transaction export. |
| `sort` | `Integer` | A number for sorting the list of books. |
| `tags` | `List<Tag>` | (Relation) All tags belonging to this book. |
| `categories`| `List<Category>`| (Relation) All categories belonging to this book. |
| `payees` | `List<Payee>` | (Relation) All payees belonging to this book. |

### `BookAddForm` Data Structure

This DTO is used when creating a new book.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `name` | `String` | The name for the new book. |
| `notes` | `String` | Optional notes. |
| `defaultCurrencyCode` | `String` | The currency code (e.g., "USD"). |
| `sort` | `Integer` | Sort order. |

### `BookUpdateForm` Data Structure

This DTO is used when updating an existing book's settings.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `name` | `String` | The new name for the book. |
| `notes` | `String` | New notes. |
| `defaultCurrencyCode` | `String` | New default currency. |
| `defaultExpenseAccountId` | `Integer` | ID of the default expense account. |
| `defaultIncomeAccountId` | `Integer` | ID of the default income account. |
| `defaultTransferFromAccountId`| `Integer` | ID of the default transfer-from account. |
| `defaultTransferToAccountId` | `Integer` | ID of the default transfer-to account. |
| `defaultExpenseCategoryId` | `Integer` | ID of the default expense category. |
| `defaultIncomeCategoryId` | `Integer` | ID of the default income category. |
| `sort` | `Integer` | New sort order. |

## 3. Database Tables to be Updated

-   **`t_user_book`**: A new record is **inserted** when a book is created. The record is **updated** when its details are changed, and **deleted** upon removal.
-   **`t_user`**: The `default_book_id` column is **updated** when a user switches their active book or when their default book is deleted.
-   **`t_user_group`**: The `default_book_id` column is **updated** if the deleted book was the group's default.
-   **`t_user_category`**, **`t_user_tag`**, **`t_user_payee`**: Records are **inserted** when a book is created from a template or cloned. Records are **deleted** when a book is deleted.

## 4. API Calls

The primary controller for these operations is `BookController`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/books` | Creates a new, empty book using `BookAddForm`. |
| `POST` | `/books/add-by-template` | Creates a new book from a `BookTemplate`. |
| `POST` | `/books/add-by-book` | Creates a new book by cloning an existing one. |
| `GET` | `/books` | Queries and lists all books for the current user's group. |
| `GET` | `/books/{id}` | Retrieves the details of a single book. |
| `PUT` | `/books/{id}` | Updates an existing book using `BookUpdateForm`. |
| `DELETE`| `/books/{id}` | Deletes a book. |
| `PATCH` | `/books/{id}/toggle` | Enables or disables a book. |
| `PATCH` | `/users/setDefaultBook/{id}` | (In `UserController`) Sets the user's active/default book. |

## 5. Business Rules and Functionality

The core logic resides in `BookService`.

-   **Deletion Constraint**: A book cannot be deleted if it has associated financial transactions. This is a critical data integrity rule.

    ```java
    // In BookService.java
    public boolean remove(Integer id) {
        // ... (permission checks)
        Book entity = baseService.getBookInGroup(id);
        if (balanceFlowRepository.existsByBook(entity)) {
            throw new FailureMessageException("book.delete.has.flow");
        }
        // ... (deletion logic for categories, tags, etc.)
        bookRepository.delete(entity);
        return true;
    }
    ```

-   **Creation from Template**: When creating from a template, the service iterates through the template's items and creates new entities associated with the new book.

    ```java
    // In BookService.java
    public void setBookByBookTemplate(BookTemplate bookTemplate, Group group, Book book) {
        // ... (set book properties)
        bookRepository.save(book);
        saveTag(TreeUtils.buildTree(bookTemplate.getTags()), book);
        saveCategory(TreeUtils.buildTree(bookTemplate.getCategories()), book);
        bookTemplate.getPayees().forEach(i -> {
            Payee payee = new Payee();
            payee.setName(i.getName());
            payee.setBook(book);
            payeeRepository.save(payee);
        });
    }
    ```

-   **Default Book Management**: When a book is deleted, the system checks if it was the default for any users and, if so, reassigns their default to the group's default book.

    ```java
    // In BookService.java (within the disable logic, which is related to deletion)
    private void checkDefault(Integer id) {
        Group group = sessionUtil.getCurrentGroup();
        if (group.getDefaultBook().getId().equals(id)) {
            throw new FailureMessageException("book.disable.is.group.default");
        }
        Book entity = baseService.getBookInGroup(id);
        List<User> users = userRepository.findByDefaultBook(entity);
        users.forEach(user -> {
            user.setDefaultBook(group.getDefaultBook());
            userRepository.save(user);
        });
    }
    ```

## 6. Detailed Test Cases

| Test Case ID | Description | Expected Result |
| :--- | :--- | :--- |
| **TC-BOOK-ADD-01**| Create a new book named "Business" from a template. | A new `Book` record is created. The book is populated with categories, tags, and payees from the template. |
| **TC-BOOK-ADD-02**| Clone an existing book "Personal" to a new book "Archive". | A new `Book` record "Archive" is created. It has the same categories, tags, and payees as "Personal". No transactions are copied. |
| **TC-BOOK-ADD-03**| Attempt to create a book with a name that already exists in the group. | The API should return a validation error (e.g., 400 Bad Request). |
| **TC-BOOK-SWITCH-01**| User switches the active book from "Personal" to "Business". | The user's session is updated. Subsequent API calls for transactions are scoped to the "Business" book. The user's `default_book_id` is updated. |
| **TC-BOOK-UPD-01**| Update a book's name and default currency. | The corresponding `t_user_book` record is updated with the new values. |
| **TC-BOOK-DEL-01**| Attempt to delete a book that contains transactions. | The API returns an error, and the book is not deleted. |
| **TC-BOOK-DEL-02**| Delete a book that has no transactions. | The `Book` record and all its associated categories, tags, and payees are deleted from the database. |
| **TC-BOOK-DEL-03**| Delete a book that is set as the user's default. | The book is deleted. The user's default book is reset to the group's default book. |

## 7. State any Assumptions

*   The user is authenticated and belongs to a `Group`. All book operations are scoped within that group.
*   The frontend is responsible for providing valid IDs for templates, source books, and other entities when creating or updating books.
*   The application maintains a "current book" in the user's session (`CurrentSession`), which is used as the default context for most financial operations.
*   The `book_tpl.json` file, which contains the book templates, is a static resource available in the application's classpath.
