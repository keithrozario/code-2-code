# Product Requirements Document: Moneynote API - Phase 4

## 1) Goal & Scope

**Goal:** To provide users with the essential tools to manage their financial ledgers ("Books") and collaborative spaces ("Groups").

**Scope:** This phase focuses on the management (reading, updating, deleting) of existing Groups and Books. It provides the foundational API endpoints for users to view, modify, and remove these core organizational structures, building upon the creation functionalities established in Phase 3.

## 2) Functional Specifications

*   **FS-001: Query Groups:** Users must be able to retrieve a paginated list of all groups they are a member of.
*   **FS-002: Update Group:** Users must be able to update the details of a group they own, such as its name, notes, and default book.
*   **FS-003: Delete Group:** Users must be able to delete a group, with validation to prevent the deletion of groups that still contain books.
*   **FS-004: Query Books:** Users must be able to retrieve a paginated and filterable list of all books within their currently active group.
*   **FS-005: View Book Details:** Users must be able to retrieve the complete details of a single, specific book.

## 3) UI / UX Flow

While this PRD is for the backend API, a hypothetical UI flow provides context:

1.  A user navigates to a "Settings" or "Management" area in the application.
2.  They see two sections: "Manage Groups" and "Manage Books".
3.  **Group Management:**
    *   The user sees a list of their groups.
    *   Clicking on a group allows them to edit its name and other properties in a form. A "Save" button triggers the `PUT /groups/{id}` API.
    *   A "Delete" button is present, which, when clicked, prompts for confirmation before calling the `DELETE /groups/{id}` API.
4.  **Book Management:**
    *   The user sees a list of books belonging to their currently active group. A search bar allows filtering this list (`GET /books`).
    *   Clicking on a book takes them to a detailed view (`GET /books/{id}`).
    *   From the detailed view, an "Edit" button allows them to modify the book's properties.

## 4) Technical Specifications

### 4.1) API Logic

---

#### **Endpoint: `GET /groups`**

*   **Description:** Retrieves a paginated list of groups the current user is a member of.
*   **Business Logic:** This endpoint is used to populate lists where a user can see all the collaborative spaces they've joined or created. It's fundamental for navigation between different shared financial environments.
*   **Request Parameters:**
    *   `page` (Query, Integer, Optional): The page number to retrieve.
    *   `size` (Query, Integer, Optional): The number of items per page.
*   **Responses and Scenarios:**
    *   **200 OK:** Successfully returns a paginated list of `Group` objects. The list may be empty if the user is not part of any groups.
    *   **401 Unauthorized:** If the user's JWT is invalid or missing.
*   **Database CRUD Operations:** `SELECT`
*   **Database SQL Statements:**
    ```sql
    -- Find all groups associated with the current user
    SELECT g.*
    FROM t_user_group g
    JOIN t_user_group_user gu ON g.id = gu.group_id
    WHERE gu.user_id = :current_user_id
    LIMIT :size OFFSET :offset;
    ```

---

#### **Endpoint: `PUT /groups/{id}`**

*   **Description:** Updates the properties of a specific group.
*   **Business Logic:** Allows a group owner to change administrative details, such as renaming the group, adding notes, or setting a new default book for members.
*   **Request Parameters:**
    *   `id` (Path, Integer, Mandatory): The ID of the group to update.
    *   `GroupUpdateForm` (Body, JSON, Mandatory):
        *   `name` (String, Mandatory)
        *   `notes` (String, Optional)
        *   `defaultCurrencyCode` (String, Mandatory)
        *   `defaultBookId` (Integer, Mandatory)
*   **Responses and Scenarios:**
    *   **200 OK:** The group was successfully updated.
    *   **401 Unauthorized:** If the user's JWT is invalid or missing.
    *   **403 Forbidden:** If the user is not an owner/admin of the group.
    *   **404 Not Found:** If no group with the given `id` exists.
    *   **409 Conflict:** If the new `name` already exists within the user's other groups.
*   **Database CRUD Operations:** `SELECT`, `UPDATE`
*   **Database SQL Statements:**
    ```sql
    -- 1. Check for name conflict (run before update)
    SELECT COUNT(*) FROM t_user_group WHERE name = :new_name AND id != :group_id AND owner_id = :current_user_id;

    -- 2. Perform the update
    UPDATE t_user_group
    SET name = :name,
        notes = :notes,
        default_currency_code = :defaultCurrencyCode,
        default_book_id = :defaultBookId
    WHERE id = :group_id AND owner_id = :current_user_id;
    ```

---

#### **Endpoint: `DELETE /groups/{id}`**

*   **Description:** Deletes a group.
*   **Business Logic:** Allows a group owner to permanently remove a collaborative space. The system must prevent deletion if the group still contains financial ledgers (books) to avoid orphaning data.
*   **Request Parameters:**
    *   `id` (Path, Integer, Mandatory): The ID of the group to delete.
*   **Responses and Scenarios:**
    *   **204 No Content:** The group was successfully deleted.
    *   **401 Unauthorized:** If the user's JWT is invalid or missing.
    *   **403 Forbidden:** If the user is not the owner of the group.
    *   **404 Not Found:** If no group with the given `id` exists.
    *   **409 Conflict:** If the group still contains one or more books.
*   **Database CRUD Operations:** `SELECT`, `DELETE`
*   **Database SQL Statements:**
    ```sql
    -- 1. Check for existing books in the group
    SELECT COUNT(*) FROM t_user_book WHERE group_id = :group_id;

    -- 2. If count is 0, proceed with deletion
    -- (Also delete user-group associations)
    DELETE FROM t_user_group_user WHERE group_id = :group_id;
    DELETE FROM t_user_group WHERE id = :group_id AND owner_id = :current_user_id;
    ```

---

#### **Endpoint: `GET /books`**

*   **Description:** Retrieves a paginated and filterable list of books within the user's current active group.
*   **Business Logic:** This is the primary endpoint for listing the financial ledgers available to a user in their current context. It powers any UI where a user needs to select or view their books.
*   **Request Parameters:**
    *   `enable` (Query, Boolean, Optional): Filter by the book's enabled status.
    *   `name` (Query, String, Optional): Filter by a search term in the book's name.
    *   `page` (Query, Integer, Optional): The page number.
    *   `size` (Query, Integer, Optional): The page size.
    *   `sort` (Query, String, Optional): The sorting criteria.
*   **Responses and Scenarios:**
    *   **200 OK:** Successfully returns a paginated list of `BookDetails` objects.
    *   **401 Unauthorized:** If the user's JWT is invalid or missing.
*   **Database CRUD Operations:** `SELECT`
*   **Database SQL Statements:**
    ```sql
    -- Retrieve books for the user's active group, with filtering
    SELECT * FROM t_user_book
    WHERE group_id = :current_group_id
      AND (:enable IS NULL OR enable = :enable)
      AND (:name IS NULL OR name LIKE CONCAT('%', :name, '%'))
    ORDER BY :sort
    LIMIT :size OFFSET :offset;
    ```

---

#### **Endpoint: `GET /books/{id}`**

*   **Description:** Retrieves all details for a single book.
*   **Business Logic:** Used to fetch detailed information for a specific book, often for displaying a "Book Details" page or pre-filling an "Edit Book" form.
*   **Request Parameters:**
    *   `id` (Path, Integer, Mandatory): The ID of the book to retrieve.
*   **Responses and Scenarios:**
    *   **200 OK:** Successfully returns the `BookDetails` object.
    *   **401 Unauthorized:** If the user's JWT is invalid or missing.
    *   **404 Not Found:** If no book with the given `id` exists within the user's active group.
*   **Database CRUD Operations:** `SELECT`
*   **Database SQL Statements:**
    ```sql
    -- Retrieve a specific book, ensuring it belongs to the user's active group
    SELECT * FROM t_user_book
    WHERE id = :book_id AND group_id = :current_group_id;
    ```

## 5) Data Model

This phase affects the `Group` and `Book` data models.

**Table: `t_user_group`**

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY` | Unique identifier for the group. |
| `name` | `VARCHAR(64)` | `NOT NULL` | Name of the group. |
| `owner_id` | `INTEGER` | `NOT NULL, FK` | The user ID of the group's owner. |
| `notes` | `VARCHAR(1024)`| | Optional descriptive notes. |
| `default_currency_code`| `VARCHAR(8)` | `NOT NULL` | Default currency for the group. |
| `default_book_id` | `INTEGER` | `FK` | The default book for users in this group. |

**Table: `t_user_book`**

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY` | Unique identifier for the book. |
| `name` | `VARCHAR(64)` | `NOT NULL` | Name of the book. |
| `group_id` | `INTEGER` | `NOT NULL, FK` | The group this book belongs to. |
| `notes` | `VARCHAR(1024)`| | Optional descriptive notes. |
| `enable` | `BOOLEAN` | `NOT NULL` | Whether the book is active. |
| `default_currency_code`| `VARCHAR(8)` | `NOT NULL` | Default currency for this book. |

## 6) Test Cases

| Test Case ID | Endpoint | Feature | Test Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-P4-01** | `GET /groups` | Happy Path | 1. Log in as a user who is a member of 3 groups. <br> 2. Call `GET /groups?page=0&size=10`. | **200 OK**. Response body contains an array of 3 group objects. |
| **TC-P4-02** | `PUT /groups/{id}` | Happy Path | 1. Log in as the owner of group `123`. <br> 2. Call `PUT /groups/123` with a new name. | **200 OK**. The group's name is updated in the database. |
| **TC-P4-03** | `PUT /groups/{id}` | Negative Path (Not Owner) | 1. Log in as a user who is a member, but not owner, of group `123`. <br> 2. Call `PUT /groups/123`. | **403 Forbidden**. |
| **TC-P4-04** | `DELETE /groups/{id}`| Negative Path (Contains Books) | 1. Log in as owner of group `123`, which contains at least one book. <br> 2. Call `DELETE /groups/123`. | **409 Conflict**. The group is not deleted. |
| **TC-P4-05** | `DELETE /groups/{id}`| Happy Path | 1. Log in as owner of group `456`, which contains no books. <br> 2. Call `DELETE /groups/456`. | **204 No Content**. The group is deleted from the database. |
| **TC-P4-06** | `GET /books` | Happy Path (Filtering) | 1. Log in and set active group. <br> 2. Call `GET /books?name=Personal`. | **200 OK**. The response contains only books with "Personal" in their name. |
| **TC-P4-07** | `GET /books/{id}` | Happy Path | 1. Log in and set active group. <br> 2. Call `GET /books/789` for a book that exists in the group. | **200 OK**. The response contains the full details for book `789`. |
| **TC-P4-08** | `GET /books/{id}` | Negative Path (Wrong Group) | 1. Log in and set active group `A`. <br> 2. Call `GET /books/999`, where book `999` exists but belongs to group `B`. | **404 Not Found**. |

## 7) Risks & Mitigations

*   **Risk:** Deleting a group could have cascading consequences if not handled carefully.
    *   **Mitigation:** The API enforces a strict rule preventing the deletion of groups that contain books. All associations (like user memberships) must be cleaned up atomically.
*   **Risk:** Performance degradation on `GET /books` or `GET /groups` for users with a very large number of items.
    *   **Mitigation:** Pagination is mandatory. Database queries should be optimized with appropriate indexes on foreign keys (`group_id`, `user_id`) and filterable columns (`name`).
*   **Risk:** Race conditions when updating group or book names, leading to duplicate names.
    *   **Mitigation:** The `UPDATE` logic should be wrapped in a database transaction that first checks for name conflicts before committing the update.

## 8) Open Questions

1.  What should be the behavior when a group's `defaultBookId` is updated? Should this change be pushed to all users of the group, or only affect new users?
2.  Is there a limit to the number of groups a user can join or own?
3.  When deleting a group, should we also delete the books within it if the user confirms a "hard delete"? (Current spec says no, but this is a potential future feature).

## 9) Task Seeds (for Agent Decomposition)

*   Implement `GET /groups` endpoint with pagination.
*   Implement `GroupService.query()` method with repository call.
*   Add test cases for `GET /groups`.
*   Implement `PUT /groups/{id}` endpoint.
*   Implement `GroupService.update()` method with validation for ownership and name conflicts.
*   Add test cases for `PUT /groups/{id}` (happy path, not owner, name conflict).
*   Implement `DELETE /groups/{id}` endpoint.
*   Implement `GroupService.remove()` method with validation to check for existing books.
*   Add test cases for `DELETE /groups/{id}` (happy path, with books).
*   Implement `GET /books` endpoint with pagination and filtering.
*   Implement `BookService.query()` method with dynamic query based on filters.
*   Add test cases for `GET /books`.
*   Implement `GET /books/{id}` endpoint.
*   Implement `BookService.get()` method ensuring book belongs to the active group.
*   Add test cases for `GET /books/{id}` (happy path, not found, wrong group).

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
- [✔] Write Integration Tests for Advanced Book Creation# Moneynote API - Detailed Design Document

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
