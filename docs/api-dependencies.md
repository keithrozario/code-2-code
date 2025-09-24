# API Implementation Plan & Dependencies

This document outlines the logical dependencies between the API endpoints. It serves as a high-level plan for the order of implementation, ensuring that foundational APIs are built before the APIs that depend on them.

## Core Dependency Flow

The general flow of dependencies follows the user's natural journey through the application:

1.  **User & Group Setup**: A user must be created and authenticated. A group is established as the primary container for all data.
2.  **Book & Account Setup**: Within a group, the user creates financial `Books` (ledgers) and `Accounts` (e.g., bank accounts, credit cards).
3.  **Transaction Recording**: With books and accounts in place, the user can record `BalanceFlows` (transactions).
4.  **Reporting & Analysis**: Once transactions exist, the user can run `Reports` to analyze their financial data.

---

## 1. User and Authentication Flow

This is the entry point for any user. All other API calls are dependent on successful authentication.

- **`POST /register`**
  - **Description**: Creates a new user.
  - **Dependencies**: None.
  - **Is a dependency for**: `POST /login`.

- **`POST /login`**
  - **Description**: Authenticates a user and provides a JWT.
  - **Dependencies**: `POST /register` (a user must exist).
  - **Is a dependency for**: **All other authenticated endpoints.** The returned JWT must be included in the `Authorization` header for subsequent calls.

---

## 2. Core Financial Structure Setup

After a user is created, they need to set up the basic structure for their bookkeeping: Groups, Books, and Accounts.

- **`POST /groups`** (Implied)
  - **Description**: Creates a new user group. In the current design, a group is created automatically during user registration.
  - **Dependencies**: `POST /register`.
  - **Is a dependency for**: `POST /books`, `POST /accounts`.

- **`POST /books`**
  - **Description**: Creates a new financial ledger (book).
  - **Dependencies**: `POST /login` (must be authenticated), `POST /groups` (a group must exist to contain the book).
  - **Is a dependency for**: `POST /categories`, `POST /tags`, `POST /payees`, `POST /balance-flows`.

- **`POST /accounts`**
  - **Description**: Creates a new financial account.
  - **Dependencies**: `POST /login`, `POST /groups`.
  - **Is a dependency for**: `POST /balance-flows` (transactions need accounts).

- **`GET /accounts`**
  - **Description**: Lists existing accounts.
  - **Dependencies**: `POST /accounts` (at least one account must be created to be listed).

---

## 3. Transaction Management (Balance Flows)

This is the primary data entry part of the application. Creating transactions depends on the core structure being in place.

- **`POST /balance-flows`**
  - **Description**: Creates a new transaction.
  - **Dependencies**:
    - `POST /login` (must be authenticated).
    - `POST /books` (a book must exist to assign the transaction to).
    - `POST /accounts` (at least one account must exist to be the source/destination of funds).
    - `POST /categories` (at least one category must exist to classify the transaction).
    - (Optional) `POST /payees`, `POST /tags`.
  - **Is a dependency for**: `PUT /balance-flows/{id}`, `DELETE /balance-flows/{id}`, `PATCH /balance-flows/{id}/confirm`, `POST /balance-flows/{id}/addFile`, and all `GET /reports/*` endpoints.

- **`PUT /balance-flows/{id}`**
  - **Description**: Updates a transaction.
  - **Dependencies**: `POST /balance-flows` (a transaction must exist to be updated).

- **`DELETE /balance-flows/{id}`**
  - **Description**: Deletes a transaction.
  - **Dependencies**: `POST /balance-flows` (a transaction must exist to be deleted).

- **`PATCH /balance-flows/{id}/confirm`**
  - **Description**: Confirms a pending transaction.
  - **Dependencies**: `POST /balance-flows` (a transaction must have been created with `confirm: false`).

---

## 4. Supporting Entities (Categories, Tags, Payees)

These entities provide classification and context for transactions. They must be created before they can be linked.

- **`POST /categories`**
  - **Description**: Creates a new category.
  - **Dependencies**: `POST /books` (a category must belong to a book).
  - **Is a dependency for**: `POST /balance-flows`.

- **`POST /tags`** (Implied)
  - **Description**: Creates a new tag.
  - **Dependencies**: `POST /books` (a tag must belong to a book).
  - **Is a dependency for**: `POST /balance-flows`.

- **`POST /payees`** (Implied)
  - **Description**: Creates a new payee.
  - **Dependencies**: `POST /books` (a payee must belong to a book).
  - **Is a dependency for**: `POST /balance-flows`.

---

## 5. File Attachments

File attachments are directly linked to transactions.

- **`POST /balance-flows/{id}/addFile`**
  - **Description**: Attaches a file to a transaction.
  - **Dependencies**: `POST /balance-flows` (a transaction must exist to attach a file to).
  - **Is a dependency for**: `GET /flow-files/view`, `DELETE /flow-files/{id}`.

- **`GET /flow-files/view`**
  - **Description**: Views an attached file.
  - **Dependencies**: `POST /balance-flows/{id}/addFile` (a file must have been uploaded).

- **`DELETE /flow-files/{id}`**
  - **Description**: Deletes an attached file.
  - **Dependencies**: `POST /balance-flows/{id}/addFile` (a file must have been uploaded).

---

## 6. Reporting

All reporting endpoints are read-only and depend on the existence of transactional data.

- **`GET /accounts/overview`**
  - **Description**: Gets the net worth summary.
  - **Dependencies**: `POST /accounts` (requires accounts to calculate totals).

- **`GET /reports/balance`**
  - **Description**: Gets data for asset/debt charts.
  - **Dependencies**: `POST /accounts`.

- **`GET /reports/expense-category`**
  - **Description**: Gets expenses aggregated by category.
  - **Dependencies**: `POST /balance-flows` (requires transactions with categories to exist).
