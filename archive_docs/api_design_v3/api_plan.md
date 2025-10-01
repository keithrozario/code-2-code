# API Endpoint Dependency Plan

This document outlines the dependencies between the MoneyNote API endpoints. Understanding these dependencies is crucial for implementation and testing.

---

## Core Principle

The general flow of operations is:
1. **User Registration & Login**: A user must exist and be authenticated.
2. **Group & Book Setup**: A user has groups, and each group contains books. Financial data is scoped to a book.
3. **Entity Creation**: Before creating transactions (Balance Flows), entities like Accounts, Categories, Payees, and Tags must be created within a book.
4. **Transaction Recording**: Balance Flows are created, linking all the previously created entities.

---

## Endpoint Dependencies

### User API

- **`POST /register`**
  - **Dependencies**: None. This is the entry point for a new user.

- **`POST /login`**
  - **Dependencies**: `POST /register` (A user must exist to be able to log in).

- **`POST /logout`**
  - **Dependencies**: `POST /login` (A user must be logged in to log out).

- **`GET /initState`**
  - **Dependencies**: `POST /login` (A user must be logged in).

- **`PATCH /changePassword`**
  - **Dependencies**: `POST /login` (A user must be logged in).

- **`GET /bookSelect/all`**
  - **Dependencies**: `POST /login` (A user must be logged in).

- **`PATCH /setDefaultGroup/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /groups` (The group to be set as default must exist).

- **`PATCH /setDefaultBook/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /books` (The book to be set as default must exist).

- **`PATCH /setDefaultGroupAndBook/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /groups` (The group must exist).
    - `POST /books` (The book must exist).

### Group API

- **`POST /groups`**
  - **Dependencies**: `POST /login` (A user must be logged in to create a group).

- **`GET /groups`**
  - **Dependencies**: `POST /login` (A user must be logged in).

- **`PUT /groups/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /groups` (The group to be updated must exist).

- **`DELETE /groups/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /groups` (The group to be deleted must exist).

### Book API

- **`POST /books`**
  - **Dependencies**: `POST /login` (A user must be logged in to create a book).

- **`GET /books` / `GET /books/all`**
  - **Dependencies**: `POST /login` (A user must be logged in).

- **`GET /books/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /books` (The book must exist).

- **`PUT /books/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /books` (The book to be updated must exist).

- **`DELETE /books/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /books` (The book to be deleted must exist).

- **`PATCH /books/{id}/toggle`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /books` (The book must exist).

### Account API

- **`POST /accounts`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - A book must be selected in the user's session.

- **`GET /accounts` / `GET /accounts/all`**
  - **Dependencies**: `POST /login` (A user must be logged in).

- **`GET /accounts/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /accounts` (The account must exist).

- **`PUT /accounts/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /accounts` (The account to be updated must exist).

- **`DELETE /accounts/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /accounts` (The account to be deleted must exist).

- **`PATCH /accounts/{id}/toggle`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /accounts` (The account must exist).

### Category, Payee, and Tag APIs (CRUD Operations)

These entities are all scoped to a book. Their creation and management depend on a logged-in user and a selected book.

- **`POST /categories`**, **`POST /payees`**, **`POST /tags`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - A book must be selected in the user's session.

- **`GET /categories`**, **`GET /payees`**, **`GET /tags`**
  - **Dependencies**: `POST /login` (A user must be logged in).

- **`PUT /categories/{id}`**, **`PUT /payees/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - The respective entity (Category, Payee) must exist.

- **`DELETE /categories/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - The category must exist.

- **`PATCH /categories/{id}/toggle`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - The category must exist.

### Balance Flow API (Transactions)

- **`POST /balance-flows`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /books` (A book must be selected).
    - `POST /accounts` (The associated account(s) must exist).
    - `POST /categories` (If categories are used, they must exist).
    - `POST /payees` (If a payee is used, it must exist).
    - `POST /tags` (If tags are used, they must exist).

- **`GET /balance-flows`**
  - **Dependencies**: `POST /login` (A user must be logged in).

- **`GET /balance-flows/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /balance-flows` (The balance flow must exist).

- **`PUT /balance-flows/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /balance-flows` (The balance flow to be updated must exist).
    - All associated entities (accounts, categories, etc.) must also exist.

- **`DELETE /balance-flows/{id}`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /balance-flows` (The balance flow to be deleted must exist).

- **`PATCH /balance-flows/{id}/confirm`**
  - **Dependencies**:
    - `POST /login` (A user must be logged in).
    - `POST /balance-flows` (The balance flow must exist).

### Other APIs

- **`GET /reports/*`**
  - **Dependencies**: `POST /balance-flows` (Requires transaction data to generate reports).

- **`POST /note-days`**, **`GET /note-days`**
  - **Dependencies**: `POST /login` (A user must be logged in).

- **`GET /flow-files/view`**, **`DELETE /flow-files/{id}`**
  - **Dependencies**: A file must have been previously uploaded and associated with a balance flow.

- **Currency, Book Template, and Test APIs**
  - These endpoints (`/currencies/*`, `/book-templates/*`, `/version`) generally have no dependencies on other API calls and can be considered self-contained or reliant on system-level configuration.
