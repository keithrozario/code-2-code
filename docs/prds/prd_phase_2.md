# PRD: Moneynote API - Phase 2

## 1. Goal & Scope

**Goal:** To implement the core user session initialization and account binding functionalities. This phase enables the application to load the essential user context after login and provides a mechanism for new users to bind a full account to their session.

**Scope:** This PRD covers the backend implementation of two critical endpoints: `GET /initState` for fetching the user's session data, and `PUT /bind` for associating a username and password with the current user.

---

## 2. Functional Specifications

*   **FS-01: Fetch Initial Application State:** The system must provide an endpoint that returns all necessary data for initializing the client-side application after a user logs in. This includes user details, the default group, and the default book.
*   **FS-02: Bind User Account:** The system must allow a currently authenticated user (potentially an anonymous or temporary user) to permanently register by binding a username, password, and invite code to their account.

---

## 3. UI / UX Flow

This PRD focuses on the backend API. The conceptual UI/UX flow is as follows:

1.  **Login & Initialization:**
    *   A user logs in successfully.
    *   The client application immediately calls `GET /initState`.
    *   The UI populates with the user's information, and the context is set to their default group and book (e.g., displaying the book name in the header).

2.  **Account Registration/Binding:**
    *   A user who has been using the application in a limited or anonymous capacity decides to create a permanent account.
    *   The user is presented with a registration form where they enter a new username, password, and an invitation code.
    *   The client application calls `PUT /bind` with these details.
    *   Upon success, the user is now fully registered, and their session is associated with the new credentials.

---

## 4. Technical Specifications

### 4.1 API Logic

#### **Endpoint: `PUT /bind`**

*   **Description:** Binds a new username and password to the currently authenticated user, effectively completing their registration. This is used to convert a temporary or anonymous user into a permanent, registered user.

*   **Business Logic:**
    1.  The system receives the request containing the new username, password, and an invite code.
    2.  It validates that the `inviteCode` is correct.
    3.  It checks if the requested `username` already exists in the database. If it does, the request is rejected.
    4.  The user's password is securely hashed (e.g., using bcrypt).
    5.  The current user's record in the database is updated with the new username and hashed password.

*   **Request:**
    *   **Headers:**
        | Name | Description | Data type | Optionality |
        |---|---|---|---|
        | `Authorization` | Bearer token | String | Mandatory |
    *   **Body:**
        | Name | Description | Data type | Optionality |
        |---|---|---|---|
        | `username` | Username | String | Mandatory |
        | `password` | Password | String | Mandatory |
        | `inviteCode` | Invitation code | String | Mandatory |

*   **Responses & Scenarios:**
    *   **200 OK (Success):** The user account is successfully updated with the new credentials.
    *   **400 Bad Request:** The `username` is already taken, the `inviteCode` is invalid, or the password does not meet complexity requirements.
    *   **401 Unauthorized:** The request is missing a valid JWT token.

*   **Database CRUD Operations:**
    *   `READ`: Check for the existence of the `username` in the `user` table.
    *   `UPDATE`: Update the `username` and `password` fields for the current user's record in the `user` table.

*   **Database SQL Statements:**
    ```sql
    -- Check for existing username
    SELECT COUNT(*) FROM t_user WHERE username = 'new_username';

    -- Update user record
    UPDATE t_user SET username = 'new_username', password = 'hashed_password' WHERE id = 'current_user_id';
    ```

---

#### **Endpoint: `GET /initState`**

*   **Description:** Fetches the essential session information for the currently logged-in user. This is the primary mechanism for the client to get the context it needs to render the user's environment.

*   **Business Logic:**
    1.  The system identifies the current user from the `Authorization` token.
    2.  It retrieves the user's details from the database.
    3.  It retrieves the user's default `Group` and default `Book` based on the `default_group_id` and `default_book_id` fields on the user record.
    4.  It packages the user, group, and book information into a consolidated response object.

*   **Request:**
    *   **Headers:**
        | Name | Description | Data type | Optionality |
        |---|---|---|---|
        | `Authorization` | Bearer token | String | Mandatory |

*   **Responses & Scenarios:**
    *   **200 OK (Success):** Returns the initial state object.
        *   **Response Body:**
            | Name | Description | Data type |
            |---|---|---|
            | `user` | User information | UserSessionVo |
            | `book` | Book information | BookSessionVo |
            | `group` | Group information| GroupSessionVo |
    *   **401 Unauthorized:** The request is missing a valid JWT token.
    *   **404 Not Found:** The user, default book, or default group associated with the token could not be found in the database.

*   **Database CRUD Operations:**
    *   `READ`: Fetch the user record from the `user` table.
    *   `READ`: Fetch the default book record from the `book` table.
    *   `READ`: Fetch the default group record from the `group` table.

*   **Database SQL Statements:**
    ```sql
    -- Fetch user
    SELECT id, username, default_book_id, default_group_id FROM t_user WHERE id = 'current_user_id';

    -- Fetch default group
    SELECT id, name FROM t_user_group WHERE id = 'user.default_group_id';

    -- Fetch default book
    SELECT id, name, default_currency_code FROM t_user_book WHERE id = 'user.default_book_id';
    ```

---

## 5. Data Model

This phase interacts with the following data models.

### `User` (`t_user`)
| Attribute | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | `PRIMARY KEY` | Unique identifier for the user. |
| `username` | `string` | `UNIQUE` | The user's login name. |
| `password` | `string` | `NOT NULL` | The user's hashed password. |
| `default_book_id` | `integer` | `FOREIGN KEY` | ID of the user's default book. |
| `default_group_id` | `integer` | `FOREIGN KEY` | ID of the user's default group. |

### `Group` (`t_user_group`)
| Attribute | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | `PRIMARY KEY` | Unique identifier for the group. |
| `name` | `string` | `NOT NULL` | The name of the group. |

### `Book` (`t_user_book`)
| Attribute | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `integer` | `PRIMARY KEY` | Unique identifier for the book. |
| `name` | `string` | `NOT NULL` | The name of the book. |
| `group_id` | `integer` | `FOREIGN KEY` | The group this book belongs to. |
| `default_currency_code` | `string` | `NOT NULL` | The default currency for this book. |

---

## 6. Test Cases

| Test Case ID | Endpoint | Feature Being Tested | Test Steps | Expected Result |
|---|---|---|---|---|
| **TC-P2-01** | `GET /initState` | Happy Path | 1. Log in as a user with a default book and group. <br> 2. Call `GET /initState`. | 200 OK. The response contains non-null `user`, `book`, and `group` objects with correct details. |
| **TC-P2-02** | `GET /initState` | Edge Case: No Default Book | 1. Log in as a user whose `default_book_id` is null. <br> 2. Call `GET /initState`. | 200 OK. The `book` field in the response is null. |
| **TC-P2-03** | `GET /initState` | Negative Path: Invalid Token | 1. Call `GET /initState` with an invalid or expired token. | 401 Unauthorized. |
| **TC-P2-04** | `PUT /bind` | Happy Path | 1. Authenticate as a temporary user. <br> 2. Call `PUT /bind` with a unique username, password, and valid invite code. | 200 OK. The user record is updated in the database. The user can now log in with the new credentials. |
| **TC-P2-05** | `PUT /bind` | Negative Path: Username Taken | 1. Authenticate as a temporary user. <br> 2. Call `PUT /bind` with a username that already exists. | 400 Bad Request with an error message indicating the username is unavailable. |
| **TC-P2-06** | `PUT /bind` | Negative Path: Invalid Invite Code | 1. Authenticate as a temporary user. <br> 2. Call `PUT /bind` with a valid username but an invalid `inviteCode`. | 400 Bad Request with an error message indicating the invite code is invalid. |

---

## 7. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Performance of `initState`:** The `initState` endpoint could become slow if more data is added to its payload over time. | Medium | Medium | Keep the `initState` payload strictly limited to essential session data. Create separate, dedicated endpoints for fetching non-essential or large datasets. |
| **Security of `bind`:** The `bind` endpoint modifies user credentials and could be a target for abuse. | Low | High | Enforce strong password policies, use a secure and non-guessable invite code system, and implement rate limiting to prevent brute-force attacks. |
| **Data Consistency:** If a user has a `default_book_id` that points to a deleted book, `initState` will fail. | Low | Medium | Implement foreign key constraints with cascading rules or cleanup jobs to ensure data integrity when entities like books or groups are deleted. |

---

## 8. Open Questions

1.  What is the specific validation logic for the `inviteCode` used in the `PUT /bind` endpoint? Is it a single global code, or are they unique and generated per user?
2.  What is the expected behavior of `GET /initState` if a user has no default book or group set? Should it return `null`, or should it attempt to select the first available book/group as a fallback?
3.  What are the password complexity requirements that should be enforced by the `PUT /bind` endpoint?

---

## 9. Task Seeds (for Agent Decomposition)

*   `task: backend - implement GET /initState endpoint logic`
*   `task: backend - implement PUT /bind endpoint logic`
*   `task: backend - add validation for username uniqueness in bind logic`
*   `task: backend - add validation for invite code in bind logic`
*   `task: tests - write unit tests for InitStateService`
*   `task: tests - write integration tests for GET /initState endpoint`
*   `task: tests - write unit tests for BindUserService`
*   `task: tests - write integration tests for PUT /bind endpoint`
*   `task: docs - update API documentation (e.g., Swagger/OpenAPI) for phase 2 endpoints`

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
- [✔] Register New Routers in Main Application


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