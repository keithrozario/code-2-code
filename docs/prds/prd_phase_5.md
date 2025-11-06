# Product Requirements Document: Moneynote API - Phase 5

## 1. Goal & Scope

**Goal:** To implement advanced management and reporting features for the "Book" entity. This phase will empower users with full lifecycle control over their financial ledgers, including updating, deleting, and toggling their state, as well as providing comprehensive data access through listing and exporting functionalities.

**Scope:** This PRD covers the backend API implementation for five key endpoints related to "Advanced Book Management" as defined in the API development plan. The work is confined to the server-side logic, database interactions, and business rule enforcement for these specific endpoints. UI/UX implementation is out of scope.

---

## 2. Functional Specifications

*   **FS-001: Update Book Details:** Users must be able to modify the attributes of an existing book, such as its name, notes, and default accounts/categories.
*   **FS-002: Delete Book:** Users must be able to permanently delete a book, with a critical safety check to prevent deletion if it contains any financial transactions.
*   **FS-003: Toggle Book State:** Users must be able to enable or disable a book, allowing them to hide it from active use without permanent deletion.
*   **FS-004: List All Books:** Users must be able to retrieve a complete and filterable list of all books they have access to within their group.
*   **FS-005: Export Book Data:** Users must be able to export all transaction data from a specific book into an Excel file for offline analysis or backup.

---

## 3. UI / UX Flow

While the backend is the focus, it will support the following user flow:

1.  A user navigates to a "Manage Books" section in the client application.
2.  The application calls `GET /books/all` to display a list of the user's books. Each item in the list has controls for editing, toggling, and deleting.
3.  **To Update:** The user clicks "Edit" on a book, which opens a form pre-filled with the book's current data. After making changes, they save, triggering a `PUT /books/{id}` call.
4.  **To Toggle:** The user clicks an "Enable/Disable" switch next to a book, triggering a `PATCH /books/{id}/toggle` call. The book's visual state changes in the list.
5.  **To Delete:** The user clicks "Delete" on a book. The application asks for confirmation. Upon confirming, a `DELETE /books/{id}` call is made. If the book has transactions, the API will return an error which the UI will display. Otherwise, the book is removed from the list.
6.  **To Export:** The user clicks an "Export" button for a specific book, triggering a `GET /books/{id}/export` call, which initiates a file download in the browser.

---

## 4. Technical Specifications

### 4.1 API Logic

#### **1. `PUT /books/{id}` - Updates a book**

*   **Business Logic:** This endpoint modifies the properties of an existing book. It must enforce that the new book name is unique within the user's group to prevent confusion. All associated entities like default accounts and categories are updated via their IDs.
*   **Request Parameters:**
    *   Path: `id` (Integer) - The ID of the book to update.
    *   Body: `BookUpdateForm`
        *   `name` (String, Optional)
        *   `notes` (String, Optional)
        *   `defaultExpenseAccountId` (Integer, Optional)
        *   `defaultIncomeAccountId` (Integer, Optional)
        *   `defaultTransferFromAccountId` (Integer, Optional)
        *   `defaultTransferToAccountId` (Integer, Optional)
        *   `defaultExpenseCategoryId` (Integer, Optional)
        *   `defaultIncomeCategoryId` (Integer, Optional)
        *   `sort` (Integer, Optional)
*   **Responses & Scenarios:**
    *   **200 OK:** The book was successfully updated. Returns the updated `BookDetails` object.
    *   **404 Not Found:** No book with the given `id` exists for the user.
    *   **409 Conflict:** The chosen `name` already exists in another book within the same group.
    *   **401 Unauthorized:** The user is not authenticated.
*   **Database CRUD:** `UPDATE`
*   **SQL Statements:**
    ```sql
    -- Check for name collision before updating
    SELECT id FROM t_user_book WHERE name = ? AND group_id = ? AND id != ?;

    -- Perform the update
    UPDATE t_user_book
    SET name = ?, notes = ?, default_expense_account_id = ?, default_income_account_id = ?, default_transfer_from_account_id = ?, default_transfer_to_account_id = ?, default_expense_category_id = ?, default_income_category_id = ?, sort = ?
    WHERE id = ?;
    ```

#### **2. `DELETE /books/{id}` - Deletes a book**

*   **Business Logic:** This endpoint permanently deletes a book. The most critical business rule is that a book with existing transactions (`BalanceFlow` records) cannot be deleted. If the book is empty, the service must first delete all associated child entities (Categories, Tags, Payees) before deleting the book itself to maintain data integrity.
*   **Request Parameters:**
    *   Path: `id` (Integer) - The ID of the book to delete.
*   **Responses & Scenarios:**
    *   **204 No Content:** The book and its associated data were successfully deleted.
    *   **404 Not Found:** No book with the given `id` exists.
    *   **400 Bad Request:** The deletion failed because the book contains transaction records.
    *   **401 Unauthorized:** The user is not authenticated.
*   **Database CRUD:** `DELETE`
*   **SQL Statements:**
    ```sql
    -- Check for existing transactions
    SELECT COUNT(*) FROM t_user_balance_flow WHERE book_id = ?;

    -- If count is 0, proceed with deletion
    DELETE FROM t_user_category WHERE book_id = ?;
    DELETE FROM t_user_tag WHERE book_id = ?;
    DELETE FROM t_user_payee WHERE book_id = ?;
    DELETE FROM t_user_book WHERE id = ?;
    ```

#### **3. `PATCH /books/{id}/toggle` - Toggles the enabled state of a book**

*   **Business Logic:** This endpoint provides a lightweight way to enable or disable a book. A disabled book should be filtered out from most views and selections (e.g., when creating new transactions) but is not deleted.
*   **Request Parameters:**
    *   Path: `id` (Integer) - The ID of the book to toggle.
*   **Responses & Scenarios:**
    *   **200 OK:** The toggle was successful. Returns the updated `BookDetails` object.
    *   **404 Not Found:** No book with the given `id` exists.
    *   **401 Unauthorized:** The user is not authenticated.
*   **Database CRUD:** `UPDATE`
*   **SQL Statements:**
    ```sql
    -- Atomically toggle the boolean 'enable' field
    UPDATE t_user_book SET enable = NOT enable WHERE id = ?;
    ```

#### **4. `GET /books/all` - Gets all books for the user**

*   **Business Logic:** Retrieves a list of all books associated with the user's current group. This endpoint supports filtering based on the `BookQueryForm`, allowing clients to request enabled or disabled books.
*   **Request Parameters:**
    *   Query: `BookQueryForm`
        *   `enable` (Boolean, Optional) - Filter by the enabled status.
        *   `name` (String, Optional) - Filter by book name (exact or partial match).
*   **Responses & Scenarios:**
    *   **200 OK:** Returns a list of `BookDetails` objects. The list may be empty if no books match the criteria.
    *   **401 Unauthorized:** The user is not authenticated.
*   **Database CRUD:** `SELECT`
*   **SQL Statements:**
    ```sql
    -- Base query, WHERE clauses are added dynamically based on query params
    SELECT * FROM t_user_book WHERE group_id = ?;

    -- Example with filter
    SELECT * FROM t_user_book WHERE group_id = ? AND enable = ?;
    ```

#### **5. `GET /books/{id}/export` - Exports a book's data**

*   **Business Logic:** Generates and returns an Excel file containing all transaction data for a given book. The data should be comprehensive, including related entities like categories, tags, and payees for each transaction. The `timeZoneOffset` is used to ensure dates and times in the export are adjusted correctly for the user's local time.
*   **Request Parameters:**
    *   Path: `id` (Integer) - The ID of the book to export.
    *   Query: `timeZoneOffset` (Integer) - The user's timezone offset in minutes from UTC.
*   **Responses & Scenarios:**
    *   **200 OK:** Returns a file stream with `Content-Type: application/vnd.ms-excel`.
    *   **404 Not Found:** No book with the given `id` exists.
    *   **401 Unauthorized:** The user is not authenticated.
*   **Database CRUD:** `SELECT`
*   **SQL Statements:**
    ```sql
    -- A comprehensive query to gather all data for the export
    SELECT
        bf.create_time,
        bf.type,
        bf.title,
        bf.amount,
        acc.name AS account_name,
        (SELECT GROUP_CONCAT(c.name) FROM t_user_category c JOIN t_user_category_relation cr ON c.id = cr.category_id WHERE cr.balance_flow_id = bf.id) AS categories,
        p.name AS payee_name,
        (SELECT GROUP_CONCAT(t.name) FROM t_user_tag t JOIN t_user_tag_relation tr ON t.id = tr.tag_id WHERE tr.balance_flow_id = bf.id) AS tags,
        bf.notes
    FROM
        t_user_balance_flow bf
    LEFT JOIN
        t_user_account acc ON bf.account_id = acc.id
    LEFT JOIN
        t_user_payee p ON bf.payee_id = p.id
    WHERE
        bf.book_id = ?
    ORDER BY
        bf.create_time DESC;
    ```

---

## 5. Data Model

This phase primarily affects the `t_user_book` table.

**Table: `t_user_book`**

| Attribute | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | **Primary Key** | Unique identifier for the book. |
| `name` | `VARCHAR(64)` | `NOT NULL` | The user-defined name of the book. Must be unique per group. |
| `group_id` | `INTEGER` | `NOT NULL`, **FK** -> `t_user_group(id)` | The group this book belongs to. |
| `notes` | `VARCHAR(1024)` | `NULLABLE` | Descriptive notes about the book. |
| `enable` | `BOOLEAN` | `NOT NULL`, Default: `true` | Flag to enable or disable the book. |
| `default_currency_code` | `VARCHAR(8)` | `NOT NULL` | The default currency for the book. |
| `default_expense_account_id` | `INTEGER` | `NULLABLE`, **FK** -> `t_user_account(id)` | Default account for new expense transactions. |
| `default_income_account_id` | `INTEGER` | `NULLABLE`, **FK** -> `t_user_account(id)` | Default account for new income transactions. |
| `default_expense_category_id` | `INTEGER` | `NULLABLE`, **FK** -> `t_user_category(id)` | Default category for new expense transactions. |
| `default_income_category_id` | `INTEGER` | `NULLABLE`, **FK** -> `t_user_category(id)` | Default category for new income transactions. |
| `sort` | `INTEGER` | `NULLABLE` | An integer value used for sorting the list of books. |

---

## 6. Test Cases

| Test Case ID | Feature Tested | Preconditions | Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-P5-01** | Update Book Name | A book with ID `10` and name "Old Name" exists. | 1. Make a `PUT` request to `/books/10`. <br> 2. Provide a JSON body with `{"name": "New Name"}`. | The book's name is successfully updated to "New Name". A 200 OK response is returned. |
| **TC-P5-02** | **(Negative)** Update with Duplicate Name | Two books exist: "Book A" (ID 1) and "Book B" (ID 2). | 1. Make a `PUT` request to `/books/2`. <br> 2. Provide a JSON body with `{"name": "Book A"}`. | The API returns a 409 Conflict error. The name of "Book B" is not changed. |
| **TC-P5-03** | Delete Empty Book | A book with ID `11` exists and has no associated transaction records. | 1. Make a `DELETE` request to `/books/11`. | The API returns a 204 No Content status. The book is permanently deleted. |
| **TC-P5-04** | **(Negative)** Delete Book with Transactions | A book with ID `12` exists and has at least one transaction record. | 1. Make a `DELETE` request to `/books/12`. | The API returns a 400 Bad Request error with a message indicating deletion is not allowed. |
| **TC-P5-05** | Toggle Book State | A book with ID `13` exists and has `enable = true`. | 1. Make a `PATCH` request to `/books/13/toggle`. | The book's `enable` field is updated to `false`. The API returns a 200 OK. |
| **TC-P5-06** | Get All Books | Three books exist in the user's group. | 1. Make a `GET` request to `/books/all`. | The API returns a 200 OK with a JSON array containing the details of all three books. |
| **TC-P5-07** | Export Book | A book with ID `14` exists and contains several transactions. | 1. Make a `GET` request to `/books/14/export?timeZoneOffset=0`. | The API returns a 200 OK with an Excel file download containing the transaction data. |

---

## 7. Risks & Mitigations

*   **Risk:** Accidental deletion of a book that the user wanted to keep.
    *   **Mitigation:** The UI should implement a confirmation dialog. The backend already prevents deletion of books with data, which is the primary safeguard against major data loss.
*   **Risk:** Performance degradation when exporting a book with a very large number of transactions.
    *   **Mitigation:** The export process should be implemented using streaming to avoid loading the entire dataset into memory. For a future version, consider a background job system that notifies the user when the export is ready for download.
*   **Risk:** Inconsistent data if deletion of associated entities (categories, tags) fails.
    *   **Mitigation:** Wrap the entire deletion process in a single database transaction to ensure that either all records are deleted or none are.

---

## 8. Open Questions

1.  What is the precise column structure and formatting required for the Excel export? (e.g., column headers, date format, number format).
2.  Should the `GET /books/all` endpoint include pagination by default? The API definition suggests it does (`page`, `size`), and this should be enforced to prevent performance issues.

---

## 9. Task Seeds (for Agent Decomposition)

1.  **Task 5.1:** Implement `PUT /books/{id}` endpoint, including logic for name uniqueness validation.
2.  **Task 5.2:** Implement `DELETE /books/{id}` endpoint, including the safety check for existing transactions and transactional deletion of associated entities.
3.  **Task 5.3:** Implement `PATCH /books/{id}/toggle` endpoint for state change.
4.  **Task 5.4:** Implement `GET /books/all` endpoint with support for filtering by `name` and `enable` status.
5.  **Task 5.5:** Implement `GET /books/{id}/export` endpoint, including logic for querying all related transaction data and generating an Excel file stream.
6.  **Task 5.6:** Write comprehensive unit and integration tests for all five endpoints, covering all success and failure scenarios outlined in the test cases.

## Completed Task so far

The following task have been executed and completed, do not repeat them, assume their output is ready for use for tasks in the future:
- [✔] Configure Version and Base URL Settings
- [✔] Create Static Data Files and Pydantic Schemas
- [✔] Implement Data Loading Service for Static Files
- [✔] Integrate Data Loading Service at Application Startup
- [✔] Implement `GET /version` and `GET /test3` Endpoints
- [✔] Implement `GET /currencies/all` Endpoint
- [✔] Implement `GET /book-templates/all` Endpoint
- [✔] Apply JWT Authentication to All Phase 1 Endpoints
- [✔] Write Integration Tests for System and Currency Endpoints
- [✔] Write Integration Tests for Book Templates Endpoint- [✔] Define Schema and Router for `PUT /bind`
- [✔] Implement CRUD Functions for User Binding
- [✔] Implement Core Service Logic for `PUT /bind`
- [✔] Create Invitation Model, CRUD, and Migration
- [✔] Integrate Invite Code Validation and Password Hashing
- [✔] Write Integration Tests for `PUT /bind` Endpoint
- [✔] Define Pydantic Schemas for `GET /initState`
- [✔] Implement `GET /initState` Endpoint and Service Logic
- [✔] Verify and Add CRUD Functions for `initState`
- [✔] Write Integration Tests for `GET /initState` Endpoint- [✔] Define SQLAlchemy Models and Migration for Group and Book
- [✔] Define Pydantic Schemas for Group and Book Operations
- [✔] Implement Basic CRUD Functions for Group and Book
- [✔] Implement Bulk/Copy CRUD Functions for Book Entities
- [✔] Implement `POST /books` Endpoint (Create from Scratch)
- [✔] Implement `POST /books/template` Endpoint
- [✔] Implement `POST /groups` Endpoint
- [✔] Implement `POST /books/copy` Endpoint
- [✔] Write Integration Tests for Group and Basic Book Creation
- [✔] Write Integration Tests for Advanced Book Creation
- [✔] Implement GET /groups Endpoint with Pagination
- [✔] Implement PUT /groups/{id} Endpoint for Group Updates
- [✔] Implement DELETE /groups/{id} Endpoint with Validation
- [✔] Create Pydantic Schemas and CRUD functions for Book Management
- [✔] Implement GET /books Endpoint with Filtering and Pagination
- [✔] Implement GET /books/{id} Endpoint for Book Details
- [✔] Implement Centralized Exception Handling
- [✔] Documentation Update for Phase 4 Endpoints# Moneynote API - Detailed Design Document

## 1. Introduction

This document provides a detailed design for the new Moneynote backend API. It is based on the API definition, dependencies, development plan, and the overarching architecture principles provided for the project. The goal is to create a robust, scalable, and maintainable API that serves as the backbone for the Moneynote application.

## 2. Overall Architecture

The API will be built using Python and the FastAPI framework, following a layered architecture pattern to ensure a clean separation of concerns.

### 2.1. Tech Stack

*   **Backend Framework**: FastAPI
*   **Programming Language**: Python
*   **Database**: SQLite3
*   **ORM**: SQLAlchemy
*   **File/Object Storage**: Google Cloud Storage (GCS)
*   **Package Management**: `uv`

### 2.2. Layered Architecture

The application will be structured into three main layers:

1.  **API/Presentation Layer (`routers`)**: This layer is responsible for handling HTTP requests and responses. It defines the API endpoints, receives incoming data, and uses the service layer to perform actions. It relies on Pydantic schemas for data validation and serialization.

2.  **Business Logic Layer (`services`)**: This layer contains the core application logic. It orchestrates operations, enforces business rules, and coordinates between the data access layer and other services. It is completely decoupled from the HTTP transport layer.

3.  **Data Access Layer (`crud`)**: This layer is responsible for all communication with the database. It contains functions for creating, reading, updating, and deleting records (CRUD), using SQLAlchemy as the ORM. This isolates the rest of the application from the specifics of the database implementation.

### 2.3. API and Deployment

*   All API endpoints will be prefixed with `/api/v1`.
*   The application will be deployed as a Google Cloud Run App within a VPC, fronted by an API Gateway and an external load balancer.
*   Due to the use of a single SQLite3 database file, the application is limited to a single running instance and cannot be scaled horizontally.

## 3. Design Considerations

### 3.1. Statelessness

Following the architecture principles, the backend API will be stateless. No application state or user session data will be held in memory on the server. This is crucial for reliability and simplifies deployment.

### 3.2. Authentication and Authorization

*   **Authentication**: The API will not handle user authentication (e.g., password validation or JWT issuance). It will rely on an external Identity Provider and an API Gateway to validate JWTs.
*   **User Identity**: The backend will receive the user's identity from the `sub` claim within the validated JWT, passed in the `Authorization: Bearer <token>` header.
*   **Auto-Registration**: If a request is received with a `sub` claim for a user that does not exist in the database, a new user record will be created automatically.
*   **Authorization**: The API will implement resource-level authorization. Business logic in the service layer will check if the authenticated user (from the JWT) has the necessary permissions to access or modify a given resource (e.g., can User A access Book B?).
*   **403 Response**: If a required JWT is missing, the API will return a `403 Forbidden` status code.

### 3.3. Data Validation

*   All incoming data will be rigorously validated on the backend. No trust will be placed in frontend validation.
*   FastAPI's integration with Pydantic will be used to define schemas for request bodies and query parameters, ensuring that all incoming data conforms to the required types and constraints before being processed by the application logic.

### 3.4. Configuration

*   Application configuration, especially for external services, will be managed through environment variables.
*   This includes the SQLAlchemy database connection string and the names of Google Cloud Storage buckets for file storage.

### 3.5. Error Handling

The API will use a standardized JSON format for error responses to provide consistent and predictable error information to clients. A middleware component will be implemented to catch exceptions and format them into this standard structure.

Example Error Response:
```json
{
  "detail": "A specific error message explaining what went wrong."
}
```

## 4. API Endpoints

The API exposes a comprehensive set of endpoints for managing all aspects of the Moneynote application. The endpoints are grouped by resource controllers. For a complete and detailed list of all endpoints, request/response models, and parameters, please refer to the **[Moneynote API Definition](./api_definition.md)**.

The primary resource controllers include:
*   **User API**: User login, registration, and session state.
*   **Account API**: Management of financial accounts.
*   **Balance Flow API**: Handling of transactions (income, expense, transfer).
*   **Book API**: Management of accounting books.
*   **Category API**: Management of transaction categories.
*   **Tag API**: Management of transaction tags.
*   **Payee API**: Management of payees.
*   **Group API**: Management of user groups for shared books.
*   **Report API**: Data aggregation and reporting.
*   And others as defined in the API documentation.

## 5. Implementation Plan

The development of the API will follow the phased approach detailed in the **[Moneynote API Development Plan](./api_plan.md)**. This plan organizes the implementation into logical, dependency-aware phases to ensure a smooth development process, starting with foundational endpoints and progressively building more complex features.

## 6. Project and File Structure

The backend project will be organized into a modular structure that reflects the layered architecture described above. This promotes maintainability, testability, and a clear separation of concerns. The proposed structure is as follows:

```
moneynote_api/
├── alembic/                  # Alembic migrations for database schema changes
│   ├── versions/             # Directory for migration script versions
│   └── env.py                # Alembic environment configuration
├── moneynote/
│   ├── __init__.py
│   ├── core/                 # Core application settings and configuration
│   │   ├── __init__.py
│   │   └── config.py         # Pydantic-based settings management (loads from env vars)
│   ├── crud/                 # Data Access Layer: Functions for database CRUD operations
│   │   ├── __init__.py
│   │   ├── crud_user.py
│   │   ├── crud_book.py
│   │   └── ...               # One file per model
│   ├── data/                 # Static data files (e.g., currency lists)
│   ├── models/               # Data Model Layer: SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   └── ...               # One file per database table
│   ├── routers/              # API/Presentation Layer: FastAPI routers
│   │   ├── __init__.py
│   │   ├── deps.py           # Common dependencies (e.g., get_current_user)
│   │   ├── users.py
│   │   ├── books.py
│   │   └── ...               # One file per resource/controller
│   ├── schemas/              # Pydantic models for validation and serialization
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   └── ...               # One file per model, with schemas for Create, Update, InDB, etc.
│   ├── services/             # Business Logic Layer: Core application logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── book_service.py
│   │   └── gcs_service.py    # Service for interacting with Google Cloud Storage
│   └── security.py           # Security-related functions (e.g., handling JWT claims)
├── tests/                    # Pytest tests for all layers
│   ├── __init__.py
│   ├── test_main.py
│   └── ...
├── .gitignore
├── database.py               # Database engine and session setup
├── main.py                   # Main FastAPI application entry point and router inclusion
├── pyproject.toml            # Project metadata and dependencies for `uv`
└── README.md                 # Project README
```
