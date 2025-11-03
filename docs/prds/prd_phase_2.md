# Product Requirements Document: Moneynote API - Phase 2

## 1. Goal & Scope

**Goal:** To implement the core user session and identity management functionalities required after the initial login.

**Scope:** This phase focuses on building on the foundational APIs from Phase 1. It introduces two key endpoints: one to allow a user to bind a full username/password to their account, and another to fetch the essential initial state (user, group, and book context) required to bootstrap the frontend application after a successful login. This phase is critical for establishing the user's context for all subsequent financial operations.

## 2. Functional Specifications

The API will provide the following functions:

*   **FS-01: Bind Username:** An authenticated user can associate a permanent username and password to their current account, typically for upgrading a guest or socially-authenticated account.
*   **FS-02: Fetch Initial State:** Upon loading the application, the system can retrieve a consolidated object containing the user's session information, their default group, and their default financial book.

## 3. UI / UX Flow

This PRD is for the backend API, so no UI will be built. However, the expected user flow is as follows:

1.  A user logs in (via a mechanism established outside this phase, e.g., social login or a temporary token).
2.  The frontend application, now authenticated, makes a call to `GET /initState`.
3.  The API returns the user's details, their default group, and their default book.
4.  The frontend uses this data to render the main dashboard, displaying the correct financial data for the active book and user.

**Bind Flow:**
1.  A user who has not yet set a username/password is prompted to secure their account.
2.  The user provides a desired username, password, and an invitation code.
3.  The frontend sends this information to the `PUT /bind` endpoint.
4.  Upon success, the user can subsequently log in with these new credentials.

## 4. Technical Specifications

### 4.1 API Logic

---

#### **API Endpoint: `PUT /bind`**

Binds a username and password to the currently authenticated user, upgrading their account.

*   **Business Logic:**
    This endpoint is used to finalize a user's account by attaching a permanent username and password. It takes the user-provided credentials, validates them, and updates the user record in the database. The `inviteCode` is used to ensure that only authorized users can perform this binding action. The password should be securely hashed before being stored.

*   **Request:**
    *   **Method:** `PUT`
    *   **Path:** `/bind`
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)
    *   **Body (`application/json`):**
        ```json
        {
          "username": "string",
          "password": "string",
          "inviteCode": "string"
        }
        ```

*   **Responses & Scenarios:**
    *   **200 OK (Success):** The binding was successful. The response body should be empty or contain a success message.
    *   **400 Bad Request:** Validation fails.
        *   The `username` is already taken.
        *   The `password` is too weak.
        *   The `inviteCode` is invalid or expired.
    *   **401 Unauthorized:** The request is missing a valid JWT token.
    *   **409 Conflict:** The current user account already has a username and password bound.

*   **Database CRUD Operations:**
    *   **READ:** Fetch the current user from the `t_user_user` table based on the ID in the JWT.
    *   **READ:** Check if the provided `username` already exists in the `t_user_user` table.
    *   **READ:** Validate the `inviteCode` against a `t_invitations` table (assumed).
    *   **UPDATE:** Update the `username` and `password_hash` fields for the current user's record in the `t_user_user` table.

*   **Database SQL Statements:**
    ```sql
    -- Fetch current user (pseudo-SQL, uses user_id from token)
    SELECT id, username FROM t_user_user WHERE id = ?;

    -- Check for existing username
    SELECT id FROM t_user_user WHERE username = ?;

    -- Update user record with new credentials
    UPDATE t_user_user SET username = ?, password_hash = ? WHERE id = ?;
    ```

---

#### **API Endpoint: `GET /initState`**

Retrieves the initial session state for the logged-in user.

*   **Business Logic:**
    This is a critical endpoint called by the frontend immediately after login. It gathers all the necessary contextual information for the user's session in a single call. It fetches the user's own data, their currently active group, and their currently active book within that group. This allows the UI to display the correct data set without making multiple, sequential API calls.

*   **Request:**
    *   **Method:** `GET`
    *   **Path:** `/initState`
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)

*   **Responses & Scenarios:**
    *   **200 OK (Success):** Returns the initial state object.
        ```json
        {
          "user": { /* UserSessionVo */ },
          "book": { /* BookSessionVo */ },
          "group": { /* GroupSessionVo */ }
        }
        ```
    *   **401 Unauthorized:** The request is missing a valid JWT token.
    *   **404 Not Found:**
        *   The user's default group or book is not set or points to a non-existent record. The API should handle this gracefully, possibly by returning `null` for the missing context.

*   **Database CRUD Operations:**
    *   **READ:** Fetch the current user from `t_user_user` using the ID from the JWT. This record contains `default_group_id` and `default_book_id`.
    *   **READ:** Fetch the default group's details from `t_user_group` using the `default_group_id`.
    *   **READ:** Fetch the default book's details from `t_user_book` using the `default_book_id`.

*   **Database SQL Statements:**
    ```sql
    -- Fetch the user and their default IDs
    SELECT id, username, default_group_id, default_book_id FROM t_user_user WHERE id = ?;

    -- Fetch the default group details
    SELECT id, name, default_currency_code FROM t_user_group WHERE id = ?;

    -- Fetch the default book details
    SELECT id, name, default_currency_code FROM t_user_book WHERE id = ?;
    ```

---

## 5. Data Model

This phase primarily reads from existing data models and updates the user record.

*   **`t_user_user`**
    *   `id` (PK): User's unique identifier.
    *   `username` (VARCHAR): The user's chosen login name. **Updated by `PUT /bind`**.
    *   `password_hash` (VARCHAR): The securely hashed password. **Updated by `PUT /bind`**.
    *   `default_group_id` (FK): The ID of the user's active group. **Read by `GET /initState`**.
    *   `default_book_id` (FK): The ID of the user's active book. **Read by `GET /initState`**.

*   **`t_user_group`**
    *   `id` (PK): Group's unique identifier.
    *   `name` (VARCHAR): The name of the group.
    *   `default_currency_code` (VARCHAR): The default currency for the group.
    *   **Read by `GET /initState`**.

*   **`t_user_book`**
    *   `id` (PK): Book's unique identifier.
    *   `name` (VARCHAR): The name of the book.
    *   `default_currency_code` (VARCHAR): The default currency for the book.
    *   **Read by `GET /initState`**.

## 6. Test Cases

| Test Case ID | Endpoint | Feature Being Tested | Test Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-P2-01** | `PUT /bind` | Happy Path - Successful binding | 1. Authenticate as a user without a username. <br> 2. Call `PUT /bind` with a unique username, valid password, and valid invite code. | API returns 200 OK. The user's record in `t_user_user` is updated with the new username and hashed password. |
| **TC-P2-02** | `PUT /bind` | Negative - Username already exists | 1. Authenticate. <br> 2. Call `PUT /bind` with a username that is already in use. | API returns 409 Conflict. No changes are made to the database. |
| **TC-P2-03** | `PUT /bind` | Negative - Invalid invite code | 1. Authenticate. <br> 2. Call `PUT /bind` with an invalid or expired `inviteCode`. | API returns 400 Bad Request. No changes are made to the database. |
| **TC-P2-04** | `GET /initState` | Happy Path - User has all defaults | 1. Authenticate as a user with a valid `default_group_id` and `default_book_id`. <br> 2. Call `GET /initState`. | API returns 200 OK with the full `user`, `group`, and `book` objects populated with data from the database. |
| **TC-P2-05** | `GET /initState` | Boundary - User has no default book | 1. Authenticate as a user with a `default_group_id` but `default_book_id` is NULL. <br> 2. Call `GET /initState`. | API returns 200 OK. The `user` and `group` objects are populated, but the `book` object is `null`. |
| **TC-P2-06** | `GET /initState` | Negative - Unauthenticated access | 1. Call `GET /initState` without a valid `Authorization` header. | API returns 401 Unauthorized. |

## 7. Risks & Mitigations

*   **Risk:** Insecure password handling in the `PUT /bind` endpoint.
    *   **Mitigation:** Ensure a strong, industry-standard hashing algorithm (e.g., bcrypt, Argon2) is used to hash passwords before they are stored. Enforce password complexity rules.
*   **Risk:** Slow performance on `GET /initState` if database queries are not optimized.
    *   **Mitigation:** Ensure that `default_group_id` and `default_book_id` on the `t_user_user` table are indexed for fast lookups. Consider caching the `initState` response for short periods.
*   **Risk:** Race conditions where two users attempt to claim the same username simultaneously.
    *   **Mitigation:** Enforce a `UNIQUE` constraint on the `username` column in the `t_user_user` database table.

## 8. Open Questions

1.  What is the exact structure of the `UserSessionVo`, `BookSessionVo`, and `GroupSessionVo` objects returned by `GET /initState`? (To be defined in collaboration with the frontend team).
2.  What is the specific success and error response body format for `PUT /bind`?
3.  What is the mechanism for generating and validating `inviteCode`s? Is there a separate table and expiration logic?

## 9. Task Seeds (for Agent Decomposition)

*   **Task 2.1:** Implement `PUT /bind` endpoint structure in the `UserController`.
*   **Task 2.2:** Add service-layer logic (`UserService`) to handle the business rules for binding a username: check for uniqueness, validate invite code, hash password.
*   **Task 2.3:** Write repository queries to update the user record in the database.
*   **Task 2.4:** Write unit and integration tests for the `PUT /bind` endpoint, covering success and failure scenarios.
*   **Task 2.5:** Implement `GET /initState` endpoint structure in the `UserController`.
*   **Task 2.6:** Add service-layer logic (`UserService`) to fetch the user, their default group, and their default book.
*   **Task 2.7:** Write repository queries to fetch the required data from `t_user_user`, `t_user_group`, and `t_user_book`.
*   **Task 2.8:** Write unit and integration tests for the `GET /initState` endpoint.

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
- [✔] Write Integration Tests for Book Templates Endpoint# Moneynote API - Detailed Design Document

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
