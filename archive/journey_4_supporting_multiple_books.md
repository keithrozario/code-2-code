# Journey 4: Supporting Multiple Books

This document details the user journey for managing separate financial ledgers, called "Books," to segregate different areas of a user's financial life.

## 1. Detailed User Journey and Flows

This journey covers the creation, management, and use of multiple Books.

### Journey 1: Creating a New Book

A user can create a new Book in one of three ways to start a new, independent ledger.

**User Flow (From Scratch):**
1.  The user navigates to the "Manage Books" section.
2.  They select "Add Book" and choose to create a new, empty book.
3.  A form prompts for a **Name** and a **Default Currency**.
4.  The user fills in the details and saves. A new, blank Book is created.

**User Flow (From Template):**
1.  In the "Add Book" section, the user chooses "Create from Template".
2.  They are presented with a list of predefined templates (e.g., "Daily Life", "Restaurant Business").
3.  The user selects a template, provides a new **Name** for their book, and confirms.
4.  A new Book is created, pre-populated with all the categories, tags, and payees defined in the chosen template.

**User Flow (By Copying):**
1.  In the "Add Book" section, the user chooses "Copy Existing Book".
2.  They select one of their existing Books as a source.
3.  They provide a new **Name** for the copied book.
4.  A new Book is created with an identical structure (all categories, tags, and payees) as the source book, but with no transaction data.

### Journey 2: Switching Between Books

This flow describes how a user changes their active context from one Book to another.

**User Flow:**
1.  The user clicks on a dropdown menu or navigation element that lists all their available Books.
2.  They select the Book they wish to work with (e.g., switching from "Personal Finances" to "Business").
3.  The application reloads, and the entire view (dashboard, transaction lists, reports) is now scoped to the newly selected Book. All subsequent actions will be recorded in this active Book.

### Journey 3: Exporting Book Data

This flow allows a user to get a full data dump of a specific Book's transactions.

**User Flow:**
1.  The user navigates to the settings for a specific Book.
2.  They click the "Export" button.
3.  The system generates an Excel (`.xlsx`) file containing all the transaction data for that Book.
4.  The file is downloaded to the user's device.

## 2. Detailed Object-Level Data Structures

### `Book` Entity (`t_user_book` table)

Represents a single, self-contained financial ledger.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary Key. |
| `group` | `Group` | (FK) The group this book belongs to. |
| `name` | `String` | The name of the book. |
| `notes` | `String` | Optional descriptive notes. |
| `enable` | `Boolean` | Flag to enable or disable the book. |
| `defaultExpenseAccount` | `Account` | (FK) Default account for new expenses. |
| `defaultIncomeAccount` | `Account` | (FK) Default account for new incomes. |
| `defaultTransferFromAccount` | `Account` | (FK) Default source account for new transfers. |
| `defaultTransferToAccount` | `Account` | (FK) Default destination account for new transfers. |
| `defaultExpenseCategory` | `Category` | (FK) Default category for new expenses. |
| `defaultIncomeCategory` | `Category` | (FK) Default category for new incomes. |
| `defaultCurrencyCode` | `String` | The default currency for reporting within this book. |
| `sort` | `Integer` | A number used for sorting the list of books. |
| `tags` | `List<Tag>` | (Relation) All tags belonging to this book. |
| `categories` | `List<Category>` | (Relation) All categories belonging to this book. |
| `payees` | `List<Payee>` | (Relation) All payees belonging to this book. |

### `BookAddForm` Data Structure

DTO for creating a new Book from scratch.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `name` | `String` | The name for the new book. |
| `defaultCurrencyCode` | `String` | The default currency for the new book. |
| `notes` | `String` | Optional notes. |
| `sort` | `Integer` | Optional sort order. |

### `BookAddByTemplateForm` Data Structure

DTO for creating a new Book from a template.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `templateId` | `Integer` | The ID of the `BookTemplate` to use. |
| `book` | `BookAddForm` | The basic details (name, currency) for the new book. |

### `BookAddByBookForm` Data Structure

DTO for creating a new Book by copying an existing one.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `bookId` | `Integer` | The ID of the source Book to copy from. |
| `book` | `BookAddForm` | The basic details (name, currency) for the new book. |

## 3. Database Tables to be Updated

-   **`t_user_book`**: A new record is **inserted** when any new book is created. Records are **updated** when a book's details are changed, and **deleted** when a book is removed.
-   **`t_user_category`**: Records are **inserted** when a book is created from a template or by copying.
-   **`t_user_tag`**: Records are **inserted** when a book is created from a template or by copying.
-   **`t_user_payee`**: Records are **inserted** when a book is created from a template or by copying.
-   **`t_user_user`**: The `default_book_id` column is **updated** when a user changes their active book.

## 4. API Calls

The primary API endpoints for this journey are in `BookController` and `UserController`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/books` | Creates a new, empty book from scratch. |
| `POST` | `/books/template` | Creates a new book from a predefined template. |
| `POST` | `/books/copy` | Creates a new book by copying an existing book's structure. |
| `GET` | `/books` | Retrieves a paginated list of all books for the current user's group. |
| `GET` | `/books/all` | Retrieves a non-paginated list of all enabled books (for dropdowns). |
| `PUT` | `/books/{id}` | Updates the details of a specific book. |
| `DELETE` | `/books/{id}` | Deletes a book. |
| `PATCH` | `/users/setDefaultBook/{id}` | Sets the specified book as the user's active book for the session. |
| `GET` | `/books/{id}/export` | Exports all transaction data for a specific book to an Excel file. |

## 5. Business Rules and Functionality

The core logic is handled by `BookService`.

-   **Data Isolation**: The `Book` is the primary container for financial data. `Category`, `Tag`, and `Payee` entities have a direct, non-nullable relationship to a `Book`, ensuring that data from one book does not leak into another.

-   **Creation from Template**: The `addByTemplate` method loads a `BookTemplate` object from a list that was initialized at startup from `book_tpl.json`. It then recursively traverses the template's categories and tags to create new database entities for the new book.

    ```java
    // In BookService.java
    public boolean addByTemplate(BookAddByTemplateForm form) {
        // ... find bookTemplate from a list loaded at startup
        Book book = add(form.getBook());
        setBookByBookTemplate(bookTemplate, group, book);
        // ... 
    }

    public void setBookByBookTemplate(BookTemplate bookTemplate, Group group, Book book) {
        // ... saves book details
        saveTag(TreeUtils.buildTree(bookTemplate.getTags()), book);
        saveCategory(TreeUtils.buildTree(bookTemplate.getCategories()), book);
        // ... saves payees
    }
    ```

-   **Creation by Copying**: The `addByBook` method works similarly. It first creates the new book, then fetches all categories, tags, and payees from the source book and creates new entities for the destination book.

    ```java
    // In BookService.java
    public boolean addByBook(BookAddByBookForm form) {
        Book book = add(form.getBook());
        Book bookSrc = baseService.getBookInGroup(form.getBookId());
        // ... copy tags, categories, and payees from bookSrc to book
        return true;
    }
    ```

-   **Deletion Constraint**: A book cannot be deleted if it has any associated `BalanceFlow` (transaction) records. This is a critical data integrity rule to prevent orphaned transactions and accidental data loss.

    ```java
    // In BookService.java
    public boolean remove(Integer id) {
        Book entity = baseService.getBookInGroup(id);
        if (balanceFlowRepository.existsByBook(entity)) {
            throw new FailureMessageException("book.delete.has.flow");
        }
        // ... proceed with deletion of book and its categories, etc.
        return true;
    }
    ```

-   **Switching Active Book**: When a user sets a new default book via the `/users/setDefaultBook/{id}` endpoint, the `UserService` updates the `defaultBook` foreign key on the `User` entity and also updates the book object stored in the current session.

## 6. Detailed Test Cases

| Test Case ID | Description | Expected Result |
| :--- | :--- | :--- |
| **TC-BOOK-01** | Create a new book from scratch named "Test Book". | A new record is created in `t_user_book`. The book has no categories, tags, or payees. |
| **TC-BOOK-02** | Create a new book from the "Daily Life" template. | A new book is created. It is populated with all the categories and tags defined in the "Daily Life" template in `book_tpl.json`. |
| **TC-BOOK-03** | Create a new book by copying an existing book "Book A" which has 10 categories. | A new book is created. It has its own 10 category records that are identical in name and structure to those in "Book A". |
| **TC-BOOK-04** | Attempt to delete a book that has at least one transaction record. | The API should return an error with the message "book.delete.has.flow". The book should not be deleted. |
| **TC-BOOK-05** | Delete an empty book (no transactions). | The API should return a success response. The book and all its associated categories, tags, and payees are deleted from the database. |
| **TC-BOOK-06** | User's active book is "Book A". User calls the API to set "Book B" as the default. | The `default_book_id` on the user's record in `t_user_user` is updated to the ID of "Book B". Subsequent API calls are scoped to "Book B". |
| **TC-BOOK-07** | Attempt to create a book with a name that already exists within the same group. | The API should return an `ItemExistsException`. |

## 7. State any Assumptions

*   The user is authenticated and has a valid session, which provides the necessary `Group` context for all operations.
*   The `book_tpl.json` file is present in the application's resources, is well-formed, and is successfully loaded into the `ApplicationScopeBean` at startup.
*   The frontend is responsible for managing the user's active book context and sending the correct book ID in transaction-related API calls.
*   When a book is created, it is associated with the user's currently active `Group`.

