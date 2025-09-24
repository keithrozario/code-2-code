# Technical Design: Phase 2 - Foundational Structures (Accounts & Books)

This document provides a detailed technical design for the second phase of the MoneyNote API implementation. The goal of this phase is to build the core CRUD (Create, Read, Update, Delete) functionality for the foundational data structures: Accounts and Books.

**Prerequisite**: All components from Phase 1 must be completed and tested. This includes a working FastAPI application, database setup, and a robust authentication system (`get_current_user` dependency).

---

## Step 1: Implement Account Management (CRUD)

**Goal:** Enable authenticated users to manage their financial accounts.

### Dependencies

- All modules from Phase 1 (`main.py`, `database.py`, `models.py`, `schemas.py`, `security.py`, `crud.py`, `dependencies.py`).
- `Enum` from Python's standard library for Account Type.

### Implementation Steps

1.  **Update `models.py`**:
    - Add an `Account` class that inherits from `Base`.
    - Define columns based on `database_schema.md`: `id`, `name`, `type` (String), `balance` (Numeric), `currencyCode` (String), `notes` (String), `enable` (Boolean), `include` (Boolean), `initialBalance` (Numeric), `creditLimit` (Numeric).
    - Add `group_id = Column(Integer, ForeignKey("groups.id"))`.
    - In the `Group` model, add the back-populating relationship: `accounts = relationship("Account")`.

2.  **Update `schemas.py`**:
    - Create an `AccountType` enum: `class AccountType(str, Enum): ...` with values `CHECKING`, `CREDIT`, `ASSET`, `DEBT`.
    - Create `AccountBase(BaseModel)` with fields: `name: str`, `type: AccountType`, `currencyCode: str`, `initialBalance: float`.
    - Create `AccountCreate(AccountBase)`.
    - Create `AccountUpdate(BaseModel)` with all fields from `AccountBase` as optional.
    - Create `Account(AccountBase)` for response data, adding `id: int` and `balance: float`. Ensure `Config.orm_mode = True`.

3.  **Update `crud.py`**:
    - `create_account(db: Session, account: schemas.AccountCreate, group_id: int)`: Creates a new `models.Account` instance, sets the initial balance, associates it with the `group_id`, and saves it to the database.
    - `get_account(db: Session, account_id: int)`: Retrieves a single account by its ID.
    - `get_accounts_by_group(db: Session, group_id: int, skip: int = 0, limit: int = 100)`: Retrieves a list of accounts belonging to a specific group.
    - `update_account(...)`: Updates an existing account record.
    - `delete_account(...)`: Deletes an account record.

4.  **Create `api/accounts.py`**:
    - Create a new `APIRouter`.
    - **`POST /accounts`**: Depends on `get_current_user`. The endpoint will receive an `AccountCreate` schema, call `crud.create_account` with the current user's group ID, and return the new account details.
    - **`GET /accounts`**: Depends on `get_current_user`. Calls `crud.get_accounts_by_group` to return all accounts for the user's group.
    - **`GET /accounts/{account_id}`**: Depends on `get_current_user`. Calls `crud.get_account`. **Crucially**, it must verify that the returned account's `group_id` matches the current user's group ID to prevent unauthorized data access. If not, raise a 404 Not Found.
    - **`PUT /accounts/{account_id}`**: Implements update logic, with the same ownership verification as the GET endpoint.
    - **`DELETE /accounts/{account_id}`**: Implements delete logic, with ownership verification.

5.  **Update `main.py`**:
    - Import the new router from `api.accounts` and include it in the main FastAPI app.

### Unit Test Cases

- `test_create_account_unauthenticated`: Attempt to call `POST /accounts` without a token, assert 401 Unauthorized.
- `test_create_account_success`: As an authenticated user, create a new account and assert a 200 OK status and that the response matches the input data.
- `test_get_accounts_success`: Create multiple accounts for a user, call `GET /accounts`, and assert that the response contains the correct number of accounts.
- `test_get_another_users_account`: Create two users and an account for each. As User 1, attempt to `GET /accounts/{id}` for User 2's account. Assert a 404 Not Found status.
- `test_update_account_success`: Update an account's name and assert the change is reflected in a subsequent GET request.
- `test_delete_account_success`: Delete an account and assert that a subsequent GET request for that ID returns 404.

---

## Step 2: Implement Book Management (CRUD)

**Goal:** Enable authenticated users to create and manage Books, which are the primary containers for transactions.

### Dependencies

- All components from Phase 1 and the previous step.

### Implementation Steps

1.  **Update `models.py`**:
    - Add a `Book` class inheriting from `Base`.
    - Define columns: `id`, `name`, `defaultCurrencyCode`, `notes`, etc.
    - Add `group_id = Column(Integer, ForeignKey("groups.id"))`.
    - In the `Group` model, add the back-populating relationship: `books = relationship("Book")`.

2.  **Update `schemas.py`**:
    - Create `BookBase`, `BookCreate`, `BookUpdate`, and `Book` (response) Pydantic schemas, following the same pattern as for Accounts.

3.  **Update `crud.py`**:
    - Add CRUD functions for books: `create_book`, `get_books_by_group`, `get_book`, `update_book`, `delete_book`.
    - The `delete_book` function must first query the `BalanceFlow` table (which will be created in a later phase) to check for associated transactions. If any exist, it should raise an exception to prevent deletion.

4.  **Create `api/books.py`**:
    - Create a new `APIRouter`.
    - Implement the `POST`, `GET`, `PUT`, and `DELETE` endpoints for `/books` and `/books/{book_id}`.
    - All endpoints must depend on `get_current_user` and perform ownership checks to ensure a user can only manage books within their own group.

5.  **Update `main.py`**:
    - Import and include the new router from `api.books`.

### Unit Test Cases

- `test_create_book_success`: As an authenticated user, create a new book and assert a 200 OK status.
- `test_get_books_success`: Create multiple books and verify they are returned by `GET /books`.
- `test_delete_book_with_transactions_fails`: (To be written in a later phase) Create a book and a transaction within it. Attempt to delete the book and assert a 400 Bad Request status with an appropriate error message.
- `test_delete_empty_book_success`: Create a book with no transactions, delete it, and assert a 200 OK status.

---

## SKIPPING THIS STEP till after phase 3
## Step 3: Implement Advanced Book Creation

**Goal:** Add helper endpoints to speed up the creation of new books by using templates or copying existing books.

### Dependencies

- All components from the previous steps.
- `json` module for parsing templates.
- That the models for `Category`, `Tags`, and `Payee` exists. Because this is only done in phase 3, we will skip this step for now.

### Implementation Steps

1.  **Create Asset File**:
    - Create a directory `assets/`.
    - Inside, create `book_templates.json`. This file will contain a list of template objects, where each object has a name, ID, and lists of default categories, tags, and payees.

2.  **Update `crud.py`**:
    - **Note**: This step requires models for `Category`, `Tag`, and `Payee` to exist. The implementation should be written with the expectation that these models and their corresponding CRUD functions (`crud.create_category`, etc.) will be created in Phase 3.
    - `create_book_from_template(...)`: This function will:
        1. Load and parse `assets/book_templates.json`.
        2. Find the template matching the provided `template_id`.
        3. Call `crud.create_book` to create the main book record.
        4. Loop through the template's categories and call `crud.create_category` for each, associating them with the new book's ID.
        5. Repeat for tags and payees.
    - `create_book_from_copy(...)`: This function will:
        1. Call `crud.create_book` to create the main book record.
        2. Fetch all categories associated with the `source_book_id`.
        3. Loop through the fetched categories and call `crud.create_category` to create copies for the new book.
        4. Repeat for tags and payees.

3.  **Update `api/books.py`**:
    - Add a `POST /books/template` endpoint that takes a `name` and `template_id` and calls the corresponding CRUD function.
    - Add a `POST /books/copy` endpoint that takes a `name` and `source_id` and calls the corresponding CRUD function.

### Unit Test Cases

- `test_create_book_from_template_success`: Call `POST /books/template`. Assert that the book is created. Then, query the `/categories` endpoint (from Phase 3) for the new book's ID and assert that the returned categories match the ones in the JSON template.
- `test_create_book_from_copy_success`: Create a source book and add several unique categories to it. Call `POST /books/copy`. Assert that the new book is created. Query the categories for the new book and assert they are new records that match the names of the source book's categories.
