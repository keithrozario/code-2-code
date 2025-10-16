# Business Requirement Document: Supporting Multiple Books

## 1.0 Summary
This document outlines the business requirements for the "Supporting Multiple Books" feature in the MoneyNote API. The purpose of this feature is to provide users with the ability to create and manage multiple, independent financial ledgers (referred to as "Books"). This allows users to segregate their finances for different purposes, such as personal, family, or small business accounting, within a single user account. The solution involves providing functionalities to create, view, update, delete, and copy books, as well as create them from predefined templates. The expected business value is increased user engagement and flexibility, catering to a wider range of financial tracking needs.

---

## 2.0 Project Scope
### 2.1 In-Scope
*   Creating a new, empty book.
*   Creating a new book from a predefined template.
*   Creating a new book by copying an existing book.
*   Viewing a list of all available books within the user's group.
*   Updating the details of an existing book.
*   Deleting an existing book, with validation to prevent deletion if it contains transactions.

### 2.2 Out-of-Scope
*   Management of financial records (transactions, balance flows) within a book.
*   Management of categories, tags, or payees outside the context of book creation (from template/copy) or deletion.
*   Definition or management of book templates.
*   User interface (UI) implementation for managing books.

---

## 3.0 Business Requirements

**BR-001: Book Creation**
The system must allow an authenticated user to create a new financial book within their active group. The user must provide a unique name and a default currency. The creation process must be completed within 2 seconds, with a 99.9% success rate. This is implemented in the `BookService.add` method, which takes a `BookAddForm` and persists a new `Book` entity.

**BR-002: Book Listing**
The system must provide a paginated list of all books associated with the user's currently active group. The API response must include the book's name, currency, and unique identifier. The response time for this operation must be under 1 second for up to 1,000 books. This is implemented in the `BookController.handleQuery` endpoint, which utilizes `BookService.query` to retrieve the data.

**BR-003: Book Update**
The system must allow a user to modify the attributes of an existing book, including its name, notes, and default accounts. The update must be reflected across the system immediately upon successful completion. The success rate for this operation must be 99.9%. This functionality is handled by the `BookService.update` method, using data from a `BookUpdateForm`.

**BR-004: Book Deletion**
The system must allow a user to permanently delete a book, provided it contains no associated financial transactions (`BalanceFlow` records). The system must validate this condition before proceeding with the deletion. The operation must complete within 2 seconds. This is enforced by the `BookService.remove` method, which checks for related `BalanceFlow` entries before deleting the `Book`.

**BR-005: Book Creation from Template**
The system must allow a user to create a new book from a predefined template. This action must pre-populate the new book with the categories, tags, and payees defined in the selected template. The creation must have a 99.5% success rate. This is implemented in the `BookService.addByTpl` method, which uses `BookTplDataLoader` to access templates.

**BR-006: Book Copy**
The system must allow a user to create a new book by copying an existing book within the same group. The new book must be an exact replica of the source book in terms of its categories, tags, and payees. This operation must complete within 3 seconds. This is implemented by the `BookService.addByBook` method.

### 3.1 Functional Requirements

**FR-001: Unique Book Name**
The system must enforce that all books within the same user group have a unique name. An attempt to create or update a book with a name that already exists in the same group must be rejected with an error message. This validation is performed within the `BookService.add` and `BookService.update` methods before persisting the entity.

**FR-002: Deletion Constraint for Books with Transactions**
The system must prevent the deletion of any book that has one or more `BalanceFlow` records associated with it. The user must be notified with an error message explaining why the deletion was blocked. This check is performed in the `BookService.remove` method by querying the `BalanceFlowRepository`.

**FR-003: Template-Based Book Initialization**
When a book is created from a template, the system shall automatically create new `Category`, `Tag`, and `Payee` entities for the new book, based on the structure of the selected template. This process is orchestrated by the `BookService.addByTpl` method.

**FR-004: Book Duplication**
When a book is copied, the system shall create new `Category`, `Tag`, and `Payee` entities for the new book that mirror those of the source book. This process is orchestrated by the `BookService.addByBook` method.

---
## 4.0 Assumptions, Constraints, and Dependencies
### 4.1 Assumptions
*   A mechanism exists for pre-loading book templates (e.g., `BookTplDataLoader` loading from `book_tpl.json`).
*   The maximum number of books allowed per group is defined and enforced elsewhere in the application logic.
*   The client-side application is responsible for rendering user-friendly error messages and feedback based on the API responses.

### 4.2 Dependencies
*   **Group Entity:** All books are scoped to a `Group`. The `Group` context is required for all book management operations to ensure data isolation and security.
*   **Account Entity:** The `Account` entity is required to set the optional default accounts (`defaultExpenseAccount`, `defaultIncomeAccount`, etc.) for a book.
*   **BalanceFlow Entity:** The `BalanceFlow` entity is checked during deletion to enforce the rule that books with transactions cannot be deleted.
*   **Category, Tag, Payee Entities:** These entities are created and associated with a new book when it is created from a template or copied from another book.
