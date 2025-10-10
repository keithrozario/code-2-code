# Product Requirements Document: Moneynote API - Phase 2

## 1) Goal & Scope

The goal of Phase 2 is to establish the core user session and initialization capabilities of the Moneynote API. This phase focuses on endpoints that enable the front-end application to load a user's essential context after login. The scope covers two key functions: binding a permanent user identity to a session and retrieving a consolidated initial state (user, default book, and default group) required for the application to render its main interface.

## 2) Functional Specifications

*   **FS-P2-01: Bind User Account:** The API shall provide a mechanism for an authenticated user to bind a permanent username and password to their current session, typically for finalizing a registration process that may have started with an invitation or as a guest.
*   **FS-P2-02: Retrieve Initial State:** The API shall provide a single endpoint to retrieve a collection of essential data needed for the application to initialize its state post-login. This includes user information, the user's default financial "Book," and the user's default "Group."

## 3) UI / UX Flow

While this PRD is for the backend API, it is informed by the following expected user flow:

*   **User Account Binding (`PUT /bind`):**
    1.  A user, potentially using the application with a temporary account or an invite, decides to create a permanent account.
    2.  The UI presents a form asking for a `username`, `password`, and an `inviteCode`.
    3.  The user submits the form.
    4.  The backend processes the request. On success, the user's session is now fully associated with the new credentials. The UI redirects them to the main dashboard or login screen.

*   **Initial State Loading (`GET /initState`):**
    1.  A user successfully logs in.
    2.  The UI transitions to a loading state (e.g., displays a spinner).
    3.  The front-end application makes a call to the `GET /initState` endpoint.
    4.  Upon receiving a successful response, the UI populates with the user-specific context. For example, the user's name is displayed in the header, and the dashboard shows data corresponding to the default financial "Book" that was returned.

## 4) Technical Specifications

This section details the technical implementation of the API endpoints in this phase.

### 4.1) API Logic

---

#### **Endpoint: `PUT /bind`**

Binds a username and password to the current authenticated user, finalizing their account setup.

*   **Business Logic:**
    This endpoint is designed to convert a temporary or invited user into a permanent one. It takes a new username and password and associates them with the user record identified by the JWT token. The `inviteCode` is used for validation to ensure the user is authorized to perform this binding action. The service logic must securely hash the provided password using a strong algorithm (e.g., bcrypt) before persisting it.

*   **Request Parameters:**

| Name | Description | Data type | Optionality |
|---|---|---|---|
| `username` | The desired username for the account. | String | Mandatory |
| `password` | The desired password for the account. | String | Mandatory |
| `inviteCode` | An invitation code to authorize the binding. | String | Mandatory |

*   **Responses & Scenarios:**

    *   **`200 OK` (Success):** The account has been successfully bound. The response body will be empty.
    *   **`400 Bad Request`:** The input is invalid. This could be due to the `username` being already taken, the `password` not meeting complexity requirements, or a missing parameter.
    *   **`401 Unauthorized`:** The provided JWT token is invalid or expired.
    *   **`403 Forbidden`:** The provided `inviteCode` is invalid or has already been used.

*   **Database CRUD Operations:**
    *   **READ:** From the `t_user` table to retrieve the current user based on the session's JWT token.
    *   **READ:** To check if the desired `username` already exists in the `t_user` table.
    *   **UPDATE:** The `t_user` table to set the `username` and `hashed_password` for the current user's record.

*   **Database SQL Statements (Illustrative):**
    ```sql
    -- 1. Check for existing username
    SELECT id FROM t_user WHERE username = :username;

    -- 2. Find the current user and validate invite code
    SELECT id FROM t_user WHERE id = :current_user_id AND invite_code = :inviteCode;

    -- 3. Update the user record
    UPDATE t_user SET username = :username, hashed_password = :hashed_password WHERE id = :current_user_id;
    ```

---

#### **Endpoint: `GET /initState`**

Retrieves the essential user, book, and group information to initialize the application's UI.

*   **Business Logic:**
    This endpoint acts as a one-stop-shop for the front end to gather initial context after login. It fetches the currently authenticated user's details, their default group, and their default book. This avoids multiple, separate API calls on page load, improving front-end performance and simplifying state management.

*   **Request Parameters:**
    None. Requires a valid `Authorization` header with a Bearer token.

*   **Responses & Scenarios:**

    *   **`200 OK` (Success):** Returns a JSON object containing the user, book, and group details.
        ```json
        {
          "user": { /* UserSessionVo */ },
          "book": { /* BookSessionVo */ },
          "group": { /* GroupSessionVo */ }
        }
        ```
    *   **`401 Unauthorized`:** The provided JWT token is invalid or expired.
    *   **`404 Not Found`:** Returned if the user, or their specified default book/group, cannot be found. The system should handle this gracefully, potentially returning `null` for the missing objects.

*   **Database CRUD Operations:**
    *   **READ:** From the `t_user` table to get the current user and their default book/group IDs.
    *   **READ:** From the `t_user_book` table to get the details of the default book.
    *   **READ:** From the `t_user_group` table to get the details of the default group.

*   **Database SQL Statements (Illustrative):**
    ```sql
    -- 1. Get the current user's details and default IDs
    SELECT id, username, email, default_book_id, default_group_id FROM t_user WHERE id = :current_user_id;

    -- 2. Get the default book's details
    SELECT id, name, default_currency_code FROM t_user_book WHERE id = :default_book_id;

    -- 3. Get the default group's details
    SELECT id, name FROM t_user_group WHERE id = :default_group_id;
    ```

## 5) Data Model

The following data models are affected by the endpoints in this phase. Fields are illustrative based on the API definitions and common practice.

*   **`User` (`t_user` table):**
    *   `id`: Integer (Primary Key)
    *   `username`: String
    *   `hashed_password`: String
    *   `email`: String
    *   `default_book_id`: Integer (Foreign Key to `t_user_book`)
    *   `default_group_id`: Integer (Foreign Key to `t_user_group`)
    *   `invite_code`: String

*   **`Book` (`t_user_book` table):**
    *   `id`: Integer (Primary Key)
    *   `name`: String
    *   `group_id`: Integer (Foreign Key to `t_user_group`)
    *   `default_currency_code`: String

*   **`Group` (`t_user_group` table):**
    *   `id`: Integer (Primary Key)
    *   `name`: String

## 6) Test Cases

| Test Case ID | Endpoint | Feature Being Tested | Test Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-P2-01** | `PUT /bind` | Happy Path | Provide a valid JWT, a unique username, a strong password, and a correct invite code. | `200 OK`. The user record is updated in the database. |
| **TC-P2-02** | `PUT /bind` | Username Conflict | Provide a username that is already registered in the system. | `400 Bad Request` with an error message indicating the username is taken. |
| **TC-P2-03** | `PUT /bind` | Invalid Invite Code | Provide an invite code that is incorrect or has expired. | `403 Forbidden` with an error message. |
| **TC-P2-04** | `GET /initState` | Happy Path | Provide a valid JWT for a user with a default book and group set. | `200 OK` with a response body containing non-null `user`, `book`, and `group` objects. |
| **TC-P2-05** | `GET /initState` | Boundary: No Defaults | Provide a valid JWT for a user that does not have a `default_book_id` or `default_group_id` set. | `200 OK`. The response body should contain a `user` object, but the `book` and `group` objects should be `null`. |
| **TC-P2-06** | `GET /initState` | Negative: Invalid Token | Provide a JWT that is expired, malformed, or invalid. | `401 Unauthorized`. |

## 7) Risks & Mitigations

*   **Risk:** The `PUT /bind` endpoint could be a vector for account modification attacks.
    *   **Mitigation:** Enforce strong validation on the `inviteCode`. The code should be single-use and expire after a short period. Implement rate limiting on the endpoint to prevent brute-force attacks.
*   **Risk:** The `GET /initState` endpoint could become slow if it aggregates too much data, leading to a poor user experience on login.
    *   **Mitigation:** Strictly limit the scope of `initState` to only the data needed for the *initial* screen render. Defer loading of other data (e.g., transaction lists, detailed reports) to subsequent, user-initiated actions. Ensure all database lookups are on indexed columns.

## 8) Open Questions

*   What is the precise generation and validation logic for the `inviteCode` used in the `/bind` endpoint? Is it tied to a group invitation, a user registration, or both?
*   What is the expected behavior of `GET /initState` if a user is part of a group but has no default book set? Should it return the group's default book, the first book in the list, or null?
*   *Note:* The database interactions and SQL statements are inferred from the API documentation. The actual implementation in the source code could not be accessed and may differ.

## 9) Task Seeds (for Agent Decomposition)

1.  **Task 1: Implement `PUT /bind` Endpoint**
    *   Create the route `/bind` in the `users` router.
    *   Implement the `bind_user` method in the `user_service`, including password hashing and `inviteCode` validation.
    *   Add unit tests for the `bind_user` service logic.
    *   Add an integration test for the `PUT /bind` endpoint.
2.  **Task 2: Implement `GET /initState` Endpoint**
    *   Create the route `/initState` in the `users` router.
    *   Implement the `get_initial_state` method in the `user_service` to fetch the user, default book, and default group.
    *   Add unit tests for the `get_initial_state` service logic, covering cases where defaults are present or null.
    *   Add an integration test for the `GET /initState` endpoint.
3.  **Task 3: Documentation**
    *   Update the API documentation (e.g., Swagger/OpenAPI) to reflect the implementation details of both endpoints.

## Completed Task so far

The following task have been executed and completed, do not repeat them, assume their output is ready for use for tasks in the future:
- [✔] Create Static Data Source Files
- [✔] Implement Configuration for Version and URL
- [✔] Implement JWT Authentication Dependency
- [✔] Implement System Endpoints: /version and /test3
- [✔] Create Data Loaders for In-Memory Caching
- [✔] Define Schemas for Currency and Book Templates
- [✔] Implement Endpoint GET /currencies/all
- [✔] Implement Endpoint GET /book-templates/all
- [✔] Integrate New Routers and Startup Logic
- [✔] Write Comprehensive Test Suite# Moneynote API - Detailed Design Document

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
