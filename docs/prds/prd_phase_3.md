# PRD - Phase 3: Group and Book Creation

## 1. Goal & Scope

**Goal:** To implement the foundational API endpoints required for creating core organizational structures: **Groups** and **Books**. This phase enables users to establish the primary containers for their financial data, allowing for the segregation of finances (e.g., personal vs. business) and collaboration.

**Scope:** This PRD covers the backend API implementation for four specific endpoints as defined in Phase 3 of the API Development Plan. The scope is limited to creating new Groups and Books. Management functionalities like updating, reading, and deleting are covered in subsequent phases.

---

## 2. Functional Specifications

The API will provide the following functionalities:

*   **FS-001: Create a New Group:** Authenticated users can create a new collaborative group. Creating a group also involves creating a default first book within it, based on a selected template.
*   **FS-002: Create a New Book:** Authenticated users can create a new, empty financial ledger (Book) within one of their existing groups.
*   **FS-003: Create a Book from a Template:** Authenticated users can create a new Book that is pre-populated with a standard set of `Categories`, `Tags`, and `Payees` from a predefined template.
*   **FS-004: Create a Book by Copying:** Authenticated users can create a new Book by duplicating an existing Book they have access to, including all its `Categories`, `Tags`, and `Payees`.

---

## 3. UI / UX Flow

While this document focuses on the backend API, the conceptual user flow is as follows:

1.  **Group Creation:**
    *   A new user, after registration, is prompted to create their first group.
    *   The user provides a group name (e.g., "My Household") and selects a book template (e.g., "Standard Personal Finance").
    *   Upon submission, the group and its first book are created.

2.  **Book Creation:**
    *   Within the application, a user navigates to a "Manage Books" section.
    *   The user clicks an "Add Book" button, which presents options: "New Empty Book", "New from Template", or "Copy Existing Book".
    *   The user fills out a form corresponding to their choice (e.g., providing a name, selecting a template or source book).
    *   Upon submission, the new book appears in their list of books.

---

## 4. Technical Specifications

Authentication: All endpoints in this phase require a valid JWT `Authorization: Bearer <token>` header.

### 4.1 API Logic

#### **1. `POST /groups`**

*   **Description:** Creates a new collaborative group for the user. A group acts as a container for users, books, and all associated financial data. This endpoint also creates the first book within the group based on a template.
*   **Business Logic:**
    *   Validates that the group name is provided.
    *   Validates that the template ID for the initial book exists.
    *   Creates a new `Group` entity, assigning the current user as the owner.
    *   Calls the book creation logic (equivalent to `POST /books/template`) to create the initial book within the new group.
    *   The entire operation should be transactional. If book creation fails, group creation should be rolled back.

*   **Request Parameters (`GroupAddForm`):**

| Name | Description | Data type | Optionality |
| :--- | :--- | :--- | :--- |
| `name` | Group name | String | Mandatory |
| `defaultCurrencyCode`| Default currency code| String | Mandatory |
| `notes` | Notes | String | Optional |
| `templateId` | Template ID for the first book | Integer | Mandatory |

*   **Responses and Scenarios:**
    *   **200 OK (Success):** Returns the details of the newly created `Group`.
    *   **400 Bad Request:**
        *   If `name` or `templateId` is missing.
        *   If the specified `templateId` does not exist.
    *   **401 Unauthorized:** If the JWT is missing or invalid.

*   **Database CRUD Operations:**
    *   `CREATE`: A new record in the `t_user_group` table.
    *   `CREATE`: A new record in the `t_user_book` table.
    *   `CREATE`: New records in `t_category`, `t_tag`, and `t_payee` for the new book based on the template.
    *   `READ`: The `book_template.json` file to get template details.

*   **Database SQL Statements (Pseudo-SQL):**
    ```sql
    -- Create the group
    INSERT INTO t_user_group (name, owner_id, default_currency_code, notes) VALUES (?, ?, ?, ?);

    -- Create the book (and its associated entities from template)
    INSERT INTO t_user_book (name, group_id, default_currency_code, ...) VALUES (?, ?, ?, ...);
    INSERT INTO t_category (book_id, name, type, ...) SELECT ?, name, type, ... FROM template_categories;
    INSERT INTO t_tag (book_id, name, ...) SELECT ?, name, ... FROM template_tags;
    INSERT INTO t_payee (book_id, name, ...) SELECT ?, name, ... FROM template_payees;
    ```

---

#### **2. `POST /books`**

*   **Description:** Creates a new, empty book within an existing group.
*   **Business Logic:**
    *   Validates that the book `name` and `defaultCurrencyCode` are provided.
    *   Checks for book name uniqueness within the user's current group (see `FR-001` in BRD).
    *   Checks if the user has reached the maximum number of books allowed in the group.
    *   Creates a new `Book` entity associated with the user's current `Group`.

*   **Request Parameters (`BookAddForm`):**

| Name | Description | Data type | Optionality |
| :--- | :--- | :--- | :--- |
| `name` | Book name | String | Mandatory |
| `defaultCurrencyCode` | Default currency code | String | Mandatory |
| `defaultExpenseAccountId` | Default expense account ID | Integer | Optional |
| `defaultIncomeAccountId` | Default income account ID | Integer | Optional |
| `defaultTransferFromAccountId` | Default transfer from account ID| Integer| Optional |
| `defaultTransferToAccountId` | Default transfer to account ID| Integer | Optional |
| `notes` | Notes | String | Optional |
| `sort` | Sort order | Integer | Optional |

*   **Responses and Scenarios:**
    *   **200 OK (Success):** Returns the details of the newly created `Book`.
    *   **400 Bad Request:**
        *   If `name` or `defaultCurrencyCode` is missing.
        *   If a book with the same `name` already exists in the group.
        *   If the group's book limit has been reached.
    *   **401 Unauthorized:** If the JWT is missing or invalid.

*   **Database CRUD Operations:**
    *   `READ`: The `t_user_group` to get the current group context.
    *   `READ`: The `t_user_book` table to check for name uniqueness and count.
    *   `CREATE`: A new record in the `t_user_book` table.

*   **Database SQL Statements (Pseudo-SQL):**
    ```sql
    -- Check for existing name
    SELECT COUNT(*) FROM t_user_book WHERE group_id = ? AND name = ?;

    -- Create the book
    INSERT INTO t_user_book (name, group_id, default_currency_code, notes, sort, ...) VALUES (?, ?, ?, ?, ?, ...);
    ```

---

#### **3. `POST /books/template`**

*   **Description:** Creates a new book pre-populated with entities from a predefined template.
*   **Business Logic:**
    *   This follows the same logic as `POST /books` for validation (name uniqueness, book limits).
    *   It additionally validates that the provided `templateId` is valid.
    *   After creating the `Book` record, it reads the specified template (from `book_tpl.json`).
    *   It iterates through the template's categories, tags, and payees, creating new records for each and associating them with the new book.
    *   This entire process must be transactional.

*   **Request Parameters (`BookAddByTemplateForm`):**

| Name | Description | Data type | Optionality |
| :--- | :--- | :--- | :--- |
| `templateId` | Template ID | Integer | Mandatory |
| `book` | Book details | BookAddForm | Mandatory |

*   **Responses and Scenarios:**
    *   **200 OK (Success):** Returns the details of the newly created `Book`.
    *   **400 Bad Request:**
        *   If `templateId` or `book` form is invalid.
        *   If the `templateId` does not exist.
        *   If the book name is a duplicate within the group.
    *   **401 Unauthorized:** If the JWT is missing or invalid.

*   **Database CRUD Operations:**
    *   `CREATE`: A new record in `t_user_book`.
    *   `READ`: The `book_tpl.json` file.
    *   `CREATE`: Multiple new records in `t_category`.
    *   `CREATE`: Multiple new records in `t_tag`.
    *   `CREATE`: Multiple new records in `t_payee`.

*   **Database SQL Statements (Pseudo-SQL):**
    ```sql
    -- Create the book
    INSERT INTO t_user_book (name, group_id, ...) VALUES (?, ?, ...);

    -- Get new book_id
    SET @new_book_id = LAST_INSERT_ID();

    -- Copy entities from template
    INSERT INTO t_category (book_id, name, type, parent_id, ...) VALUES (@new_book_id, ?, ?, ?, ...); -- Repeated for each category
    INSERT INTO t_tag (book_id, name, ...) VALUES (@new_book_id, ?, ...); -- Repeated for each tag
    INSERT INTO t_payee (book_id, name, ...) VALUES (@new_book_id, ?, ...); -- Repeated for each payee
    ```

---

#### **4. `POST /books/copy`**

*   **Description:** Creates a new book by duplicating an existing book, including its categories, tags, and payees.
*   **Business Logic:**
    *   Follows the same validation logic as `POST /books` (name uniqueness, book limits).
    *   Validates that the source `bookId` exists and the user has access to it (i.e., it's in the same group).
    *   After creating the new `Book` record, the service queries all `Category`, `Tag`, and `Payee` records associated with the source `bookId`.
    *   It then creates new records for each of these, associating them with the new book ID.
    *   This process must be transactional.

*   **Request Parameters (`BookAddByBookForm`):**

| Name | Description | Data type | Optionality |
| :--- | :--- | :--- | :--- |
| `bookId` | Book ID to copy | Integer | Mandatory |
| `book` | New book details | BookAddForm | Mandatory |

*   **Responses and Scenarios:**
    *   **200 OK (Success):** Returns the details of the newly created `Book`.
    *   **400 Bad Request:**
        *   If `bookId` or `book` form is invalid.
        *   If the book name is a duplicate within the group.
    *   **401 Unauthorized:** If the JWT is missing or invalid.
    *   **404 Not Found:** If the source `bookId` does not exist or the user cannot access it.

*   **Database CRUD Operations:**
    *   `CREATE`: A new record in `t_user_book`.
    *   `READ`: The source book from `t_user_book`.
    *   `READ`: All associated records from `t_category`, `t_tag`, `t_payee` for the source book.
    *   `CREATE`: Multiple new records in `t_category`.
    *   `CREATE`: Multiple new records in `t_tag`.
    *   `CREATE`: Multiple new records in `t_payee`.

*   **Database SQL Statements (Pseudo-SQL):**
    ```sql
    -- Create the new book
    INSERT INTO t_user_book (name, group_id, ...) VALUES (?, ?, ...);

    -- Get new book_id
    SET @new_book_id = LAST_INSERT_ID();
    SET @source_book_id = ?;

    -- Copy entities from source book
    INSERT INTO t_category (book_id, name, type, parent_id, ...) SELECT @new_book_id, name, type, parent_id, ... FROM t_category WHERE book_id = @source_book_id;
    INSERT INTO t_tag (book_id, name, ...) SELECT @new_book_id, name, ... FROM t_tag WHERE book_id = @source_book_id;
    INSERT INTO t_payee (book_id, name, ...) SELECT @new_book_id, name, ... FROM t_payee WHERE book_id = @source_book_id;
    ```

---

## 5. Data Model

This phase introduces or directly interacts with the following primary data models.

### `Group` Entity (`t_user_group`)

| Attribute | Data Type | Constraints/Properties | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `PRIMARY KEY` | Unique identifier for the group. |
| `name` | `String` | `NOT NULL` | The name of the group. |
| `owner` | `User` | `ManyToOne`, `NOT NULL` | The user who owns the group. |
| `notes` | `String` | `length = 1024` | Optional notes for the group. |
| `defaultCurrencyCode` | `String` | `NOT NULL`, `length = 8` | The default currency for the group. |
| `defaultBook` | `Book` | `OneToOne` | The default book for the group. |

### `Book` Entity (`t_user_book`)

| Attribute | Data Type | Constraints/Properties | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `PRIMARY KEY` | The unique identifier for the book. |
| `name` | `String` | `NOT NULL` | The name of the book. Must be unique per group. |
| `group` | `Group` | `ManyToOne`, `NOT NULL`| The group to which the book belongs. |
| `notes` | `String` | `length = 1024` | Optional notes for the book. |
| `enable` | `Boolean` | `NOT NULL` | Whether the book is enabled or not. |
| `defaultCurrencyCode` | `String` | `NOT NULL`, `length = 8`| The default currency for the book. |
| `sort` | `Integer` | | The sort order of the book. |

---

## 6. Test Cases

| Test Case ID | Feature Being Tested | Preconditions | Test Steps | Test Data | Expected Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-GRP-001** | Happy Path - Create Group | User is authenticated. Template ID `1` exists. | 1. `POST /groups` | `name`: "Family Finances", `templateId`: 1, `defaultCurrencyCode`: "USD" | 200 OK. New Group is created. A new Book is also created inside it. |
| **TC-GRP-002** | Negative Path - Invalid Template | User is authenticated. | 1. `POST /groups` | `name`: "My Group", `templateId`: 999 | 400 Bad Request. Error message indicating template not found. |
| **TC-BOOK-001**| Happy Path - Create Book | User is in a group. | 1. `POST /books` | `name`: "Vacation Fund", `defaultCurrencyCode`: "EUR" | 200 OK. New Book is created. |
| **TC-BOOK-002**| Negative Path - Duplicate Name | A book named "Work Expenses" exists in the group. | 1. `POST /books` | `name`: "Work Expenses", `defaultCurrencyCode`: "USD" | 400 Bad Request. Error message indicating name must be unique. |
| **TC-TPL-001** | Happy Path - Create from Template | Template ID `2` exists. | 1. `POST /books/template` | `templateId`: 2, `book`: { `name`: "New Store", `defaultCurrencyCode`: "USD" } | 200 OK. New Book is created with categories, tags, etc., from template 2. |
| **TC-COPY-001**| Happy Path - Copy Book | Book with ID `5` exists and has categories/tags. | 1. `POST /books/copy` | `bookId`: 5, `book`: { `name`: "Old Store Archive", `defaultCurrencyCode`: "CAD" } | 200 OK. New Book is created as a copy of Book 5. |
| **TC-COPY-002**| Negative Path - Copy Non-existent Book | Book with ID `99` does not exist. | 1. `POST /books/copy` | `bookId`: 99, `book`: { `name`: "Ghost Book" } | 404 Not Found. Error message indicating source book not found. |

---

## 7. Risks & Mitigations

*   **Risk 1: Performance of Copy/Template Creation:** Creating a book from a large template or copying a book with thousands of associated items (categories, tags) could be slow and time out.
    *   **Mitigation:** For the initial implementation, enforce limits on the number of items in templates. For a future version, this operation could be moved to an asynchronous background job.
*   **Risk 2: Race Conditions:** Two simultaneous requests to create a book with the same name in the same group could both pass the initial validation check before either is committed.
    *   **Mitigation:** Enforce a `UNIQUE` constraint on the `(group_id, name)` columns in the `t_user_book` database table to provide a definitive final check.
*   **Risk 3: Transaction Rollbacks:** A failure during the creation of associated items (e.g., categories) could leave an orphaned `Book` record if the process is not fully transactional.
    *   **Mitigation:** Ensure all service-layer methods that perform multiple database writes are annotated with `@Transactional` to guarantee that the entire operation succeeds or fails as a single unit.

---

## 8. Open Questions

1.  What are the performance expectations for the `POST /books/copy` and `POST /books/template` endpoints? Is a synchronous response acceptable if it takes 5+ seconds for a very large book/template?
2.  Should there be a limit on the number of categories, tags, or payees that can be created as part of a template or copy operation to prevent abuse?
3.  When a group is created, the first book's name is derived from the template. Should the user be able to specify a custom name for this first book during group creation?

---

## 9. Task Seeds (for Agent Decomposition)

1.  **Task:** Implement `POST /groups` endpoint.
    *   **Sub-task:** Create `GroupAddForm` validator.
    *   **Sub-task:** Implement `GroupService.createGroup` method with transactional logic to also create the first book from the specified template.
2.  **Task:** Implement `POST /books` endpoint.
    *   **Sub-task:** Add logic to `BookService.add` to check for name uniqueness and book count limits within the group.
3.  **Task:** Implement `POST /books/template` endpoint.
    *   **Sub-task:** Implement logic in `BookService.addByTpl` to read `book_tpl.json`.
    *   **Sub-task:** Implement logic to iterate and persist new `Category`, `Tag`, and `Payee` entities based on the template.
4.  **Task:** Implement `POST /books/copy` endpoint.
    *   **Sub-task:** Implement logic in `BookService.addByBook` to query all child entities of the source book.
    *   **Sub-task:** Implement logic to duplicate and persist these child entities for the new book.
5.  **Task:** Add database constraints.
    *   **Sub-task:** Create a migration to add a `UNIQUE` constraint on `(group_id, name)` in the `t_user_book` table.
6.  **Task:** Write integration tests for all four endpoints, covering all success and failure scenarios outlined in the test cases.

## 10. Completed Task so far

The following task have been executed and completed, do not repeat them, assume their output is ready for use for tasks in the future:
- [✔] Create Static Data Files for Currencies and Book Templates
- [✔] Define Pydantic Schemas for API Data Models
- [✔] Implement In-Memory Data Loading Service
- [✔] Implement Shared Authentication Dependency
- [✔] Implement Configuration Management for Application Version
- [✔] Implement `GET /version` Endpoint
- [✔] Implement `GET /test3` Endpoint
- [✔] Implement `GET /currencies/all` Endpoint
- [✔] Implement `GET /book-templates/all` Endpoint
- [✔] Define Pydantic Schemas for initState and bind Endpoints
- [✔] Implement CRUD Functions for initState Logic
- [✔] Implement Service and Endpoint for GET /initState
- [✔] Add Password Hashing Utility
- [✔] Implement CRUD Functions for User Binding
- [✔] Implement Service and Endpoint for PUT /bind
- [✔] Write Integration Tests for GET /initState
- [✔] Write Integration Tests for PUT /bind
- [✔] Clarify and Implement Invite Code Logic
- [✔] Update API Documentation for New Endpoints


# Appendix

# Moneynote API - Detailed Design Document

## 1. Introduction

This document provides a detailed design for the Moneynote backend API. It is based on the API definition, dependencies, development plan, and the established architecture principles. The goal is to create a scalable, secure, and maintainable API using Python, FastAPI, and Google Cloud Platform.

## 2. Overall Architecture

The API will be a monolithic backend service built with Python and the FastAPI framework, following the principles of a modern, stateless, API-driven application.

### 2.1. Application Architecture

The system is composed of three primary components:

1.  **Backend (This API):** A Python/FastAPI application responsible for all business logic, data processing, and validation. It serves data to the frontend and interacts with the database and file storage.
2.  **Database:** A single SQLite3 database file. The backend interacts with the database via the SQLAlchemy ORM. The database is treated as a pure data store, with no business logic (triggers, stored procedures).
3.  **File Storage:** Google Cloud Storage (GCS) will be used for storing all user-uploaded files, such as attachments to balance flow records.

### 2.2. Deployment and Infrastructure

The backend is designed to be deployed as a containerized application on **Google Cloud Run**.

-   **Scalability:** The application itself is stateless. However, due to the use of a single SQLite3 database file, the Cloud Run service will be configured to run as a **single instance**.
-   **Network:** The service will operate within a VPC, accessible only by the API Gateway.
-   **API Gateway:** An external-facing Load Balancer will route traffic to an API Gateway (e.g., Kong), which then routes requests to the Cloud Run backend.

### 2.3. Authentication and Authorization

Authentication is handled externally, promoting a decoupled and secure architecture.

-   **JWT Handling:** An external Identity Provider (e.g., Auth0, Google Identity Platform) is responsible for user authentication and issuing JSON Web Tokens (JWTs).
-   **Gateway Validation:** The API Gateway is responsible for validating the signature and expiration of the JWT on all incoming requests. The backend will **not** perform JWT validation.
-   **User Identification:** The backend will receive validated JWTs and extract the user's identity from the `sub` (subject) claim. This identity will be used for all resource-level access control.
-   **Implicit Registration:** If a request is received with a valid JWT for a user not yet in the database, a new user record will be created automatically.
-   **Access Control:** All endpoints (unless explicitly public, like `/login` or `/register`) will require a valid JWT. Business logic will ensure that users can only access resources they own or have been granted access to (e.g., through Group membership).

## 3. Design Considerations

### 3.1. RESTful Principles

The API will adhere to RESTful design principles:

-   **Resource-Based URLs:** Endpoints are structured around resources (e.g., `/books`, `/accounts`, `/balance-flows`).
-   **Standard HTTP Methods:** Correct use of HTTP verbs (GET, POST, PUT, PATCH, DELETE) for interacting with resources.
-   **Statelessness:** Each request from a client will contain all the information needed to service the request. The server will not store any client context between requests.

### 3.2. Data Modeling and Persistence

-   **ORM:** **SQLAlchemy** will be used as the Object-Relational Mapper to define database models and interact with the SQLite database.
-   **Models:** Each primary resource (User, Group, Book, Account, Category, Tag, Payee, BalanceFlow) will have a corresponding SQLAlchemy model class. These models will define the table structure and relationships.
-   **Database Migrations:** `Alembic` will be used to manage database schema migrations, allowing for version-controlled changes to the database structure.

### 3.3. Data Validation

-   **Pydantic Schemas:** FastAPI's native integration with Pydantic will be used for robust data validation. For each API endpoint that accepts a request body, a Pydantic schema will be defined to validate the incoming data's type, format, and constraints. This provides automatic request validation and clear error messages for invalid payloads.
-   **Backend Authority:** All validation will be performed on the backend, which will never trust data coming from the frontend, even if the frontend has its own validation.

### 3.4. File Handling

-   **Google Cloud Storage (GCS):** All file uploads (e.g., for `FlowFile`) will be handled by a dedicated service that interacts with the Google Cloud Storage Python SDK.
-   **Process:** When a file is uploaded to an endpoint like `POST /balance-flows/{id}/addFile`, the backend will stream the file directly to a designated GCS bucket. A reference to the file (e.g., its GCS path or a unique ID) will be stored in the `FlowFile` database table. File downloads will be served via signed URLs to ensure secure, temporary access.

### 3.5. Configuration

-   All external configurations will be managed via environment variables, as expected by the Cloud Run environment. This includes:
    -   `DATABASE_URL`: The connection string for the SQLite database.
    -   `GCS_BUCKET_NAME`: The name of the Google Cloud Storage bucket for file uploads.

## 4. Overall File Structure

The project will follow a standard FastAPI application structure to ensure modularity and maintainability. This structure separates concerns (API routing, business logic, data access, and data models).

```
/new_app/
├── alembic/                  # Database migration scripts
│   ├── versions/
│   └── env.py
├── moneynote/                # Main application source code
│   ├── __init__.py
│   ├── main.py               # FastAPI app instantiation, middleware, API router inclusion
│   ├── config.py             # Pydantic settings model to load env variables
│   ├── database.py           # SQLAlchemy engine, session management
│   ├── security.py           # JWT processing, user identity extraction
│   │
│   ├── crud/                 # Create, Read, Update, Delete database operations
│   │   ├── __init__.py
│   │   ├── crud_user.py
│   │   ├── crud_book.py
│   │   └── ... (one file per model)
│   │
│   ├── models/               # SQLAlchemy ORM models (database tables)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   └── ... (one file per resource)
│   │
│   ├── routers/              # API endpoint definitions (the "Controllers")
│   │   ├── __init__.py
│   │   ├── deps.py             # FastAPI dependencies (e.g., get_current_user)
│   │   ├── users.py
│   │   ├── books.py
│   │   ├── accounts.py
│   │   └── ... (one file per resource/controller)
│   │
│   ├── schemas/              # Pydantic models for data validation and serialization
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── token.py
│   │   └── ... (one file per resource)
│   │
│   └── services/             # Business logic layer
│       ├── __init__.py
│       ├── user_service.py
│       ├── book_service.py
│       └── gcs_service.py      # Logic for interacting with Google Cloud Storage
│
└── tests/                    # Pytest tests
    ├── __init__.py
    ├── conftest.py
    └── routers/
        └── test_users.py
        └── ... (tests mirroring the app structure)
```