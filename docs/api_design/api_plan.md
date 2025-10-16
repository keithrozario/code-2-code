# Moneynote API Development Plan

This document outlines the phased development plan for building the Moneynote backend API endpoints. The plan is structured to ensure that API endpoints are built in a logical order, respecting their dependencies. Each phase consists of a set of related endpoints, with no more than five endpoints per phase.

---

## Phase 1: Foundational APIs (No Dependencies)

This phase establishes the most basic and independent endpoints.

- **`GET /version`**: Returns the application version.
- **`GET /test3`**: Returns the base URL of the application for testing.
- **`GET /currencies/all`**: Gets all supported currencies.
- **`GET /book-templates/all`**: Gets all available book templates.

---

## Phase 2: User Authentication and Session

This phase focuses on user login and session management.

- **`PUT /bind`**: Binds a username to the current user.
- **`GET /initState`**: Gets the initial state for the current user.

---

## Phase 3: Group and Book Creation

This phase deals with the creation of core data structures: Groups and Books.

- **`POST /groups`**: Adds a new group.
- **`POST /books`**: Adds a new book.
- **`POST /books/template`**: Adds a new book from a template.
- **`POST /books/copy`**: Adds a new book by copying an existing one.

---

## Phase 4: Group and Book Management

This phase covers the management (reading, updating, deleting) of Groups and Books.

- **`GET /groups`**: Queries groups.
- **`PUT /groups/{id}`**: Updates a group.
- **`DELETE /groups/{id}`**: Deletes a group.
- **`GET /books`**: Queries books.
- **`GET /books/{id}`**: Gets a book by ID.

---

## Phase 5: Advanced Book Management

This phase continues with more specific book management functionalities.

- **`PUT /books/{id}`**: Updates a book.
- **`DELETE /books/{id}`**: Deletes a book.
- **`PATCH /books/{id}/toggle`**: Toggles the enabled state of a book.
- **`GET /books/all`**: Gets all books for the user.
- **`GET /books/{id}/export`**: Exports a book's data.

---

## Phase 6: User-Group and User-Book Relations

This phase focuses on linking users to groups and books.

- **`PATCH /setDefaultGroup/{id}`**: Sets the default group for the current user.
- **`PATCH /setDefaultBook/{id}`**: Sets the default book for the current user.
- **`PATCH /setDefaultGroupAndBook/{id}`**: Sets the default group and book.
- **`GET /bookSelect/all`**: Gets all books for the current user for selection.
- **`GET /groups/{id}/users`**: Gets all users in a group.

---

## Phase 7: Group Invitations

This phase implements the group invitation workflow.

- **`POST /groups/{id}/inviteUser`**: Invites a user to a group.
- **`POST /groups/{id}/removeUser`**: Removes a user from a group.
- **`POST /groups/{id}/agree`**: Agrees to a group invitation.
- **`POST /groups/{id}/reject`**: Rejects a group invitation.

---

## Phase 8: Account Foundation

This phase establishes the core functionality for managing accounts.

- **`POST /accounts`**: Adds a new account.
- **`GET /accounts`**: Queries accounts.
- **`GET /accounts/{id}`**: Gets an account by ID.
- **`GET /accounts/all`**: Gets all accounts.
- **`GET /accounts/overview`**: Gets an overview of all accounts.

---

## Phase 9: Account Management

This phase covers updating and deleting accounts.

- **`PUT /accounts/{id}`**: Updates an account.
- **`DELETE /accounts/{id}`**: Deletes an account.
- **`PUT /accounts/{id}/updateNotes`**: Updates the notes of an account.
- **`POST /accounts/{id}/adjust`**: Adjusts the balance of an account.
- **`PUT /accounts/{id}/adjust`**: Updates a balance adjustment.

---

## Phase 10: Account Toggles and Stats

This phase implements various toggleable flags for accounts and statistics.

- **`PATCH /accounts/{id}/toggle`**: Toggles the enabled state of an account.
- **`PATCH /accounts/{id}/toggleInclude`**: Toggles the `include` property of an account.
- **`PATCH /accounts/{id}/toggleCanExpense`**: Toggles the `canExpense` property.
- **`PATCH /accounts/{id}/toggleCanIncome`**: Toggles the `canIncome` property.
- **`GET /accounts/statistics`**: Gets account statistics.

---

## Phase 11: Categories

This phase implements CRUD operations for categories.

- **`POST /categories`**: Adds a new category.
- **`GET /categories`**: Queries categories.
- **`GET /categories/all`**: Gets all categories.
- **`PUT /categories/{id}`**: Updates a category.
- **`DELETE /categories/{id}`**: Deletes a category.

---

## Phase 12: Payees

This phase implements CRUD operations for payees.

- **`POST /payees`**: Adds a new payee.
- **`GET /payees`**: Queries payees.
- **`GET /payees/all`**: Gets all payees.
- **`PUT /payees/{id}`**: Updates a payee.
- **`DELETE /payees/{id}`**: Deletes a payee.

---

## Phase 13: Tags

This phase implements CRUD operations for tags.

- **`POST /tags`**: Adds a new tag.
- **`GET /tags`**: Queries tags.
- **`GET /tags/all`**: Gets all tags.
- **`PUT /tags/{id}`**: Updates a tag.
- **`DELETE /tags/{id}`**: Deletes a tag.

---

## Phase 14: Balance Flow Core

This phase implements the core CRUD operations for balance flow records (transactions).

- **`POST /balance-flows`**: Adds a new balance flow record.
- **`GET /balance-flows`**: Queries balance flow records.
- **`GET /balance-flows/{id}`**: Gets a balance flow record by ID.
- **`PUT /balance-flows/{id}`**: Updates a balance flow record.
- **`DELETE /balance-flows/{id}`**: Deletes a balance flow record.

---

## Phase 15: Balance Flow Features and Files

This phase adds extra functionalities to balance flows, including file attachments.

- **`GET /balance-flows/statistics`**: Gets balance flow statistics.
- **`PATCH /balance-flows/{id}/confirm`**: Confirms a balance flow record.
- **`POST /balance-flows/{id}/addFile`**: Adds a file to a balance flow record.
- **`GET /balance-flows/{id}/files`**: Gets files for a balance flow record.
- **`DELETE /flow-files/{id}`**: Deletes a flow file.

---

## Phase 16: Reporting

This phase focuses on building the reporting endpoints for data analysis.

- **`GET /reports/expense-category`**: Gets a report of expense by category.
- **`GET /reports/income-category`**: Gets a report of income by category.
- **`GET /reports/expense-tag`**: Gets a report of expense by tag.
- **`GET /reports/income-tag`**: Gets a report of income by tag.
- **`GET /reports/balance`**: Gets a balance report.

---

## Phase 17: Additional Reporting and Note Days

This phase completes the reporting and introduces the "Note Day" feature.

- **`GET /reports/expense-payee`**: Gets a report of expense by payee.
- **`GET /reports/income-payee`**: Gets a report of income by payee.
- **`POST /note-days`**: Adds a new note day.
- **`GET /note-days`**: Queries note days.
- **`PUT /note-days/{id}`**: Updates a note day.

---

## Phase 18: Currency and Note Day Management

This final phase covers currency rate management and completes the Note Day functionality.

- **`POST /currencies/refresh`**: Refreshes currency rates.
- **`PUT /currencies/{id}/rate`**: Updates the exchange rate of a currency.
- **`DELETE /note-days/{id}`**: Deletes a note day.
- **`PATCH /note-days/{id}/run`**: Runs a note day.
- **`PATCH /note-days/{id}/recall`**: Recalls a note day.
