# Product Requirements Document: Moneynote API - Phase 2

**Author:** Gemini
**Date:** 28/10/2025
**Version:** 1.0

---

## 1. Goal & Scope

### 1.1. Goal

This document outlines the requirements for Phase 2 of the Moneynote API. The primary goal of this phase is to establish the user's session and context after they have authenticated. This involves providing the client application with the essential initial data (user, book, group) required for operation and allowing a user to bind a permanent username and password to their account, upgrading it from a temporary or guest status.

### 1.2. In Scope

*   **`GET /initState`**: An endpoint to retrieve the essential user, default book, and default group information needed to initialize the application state on the client-side.
*   **`PUT /bind`**: An endpoint to allow a user to associate a username, password, and invite code with their existing account.

### 1.3. Out of Scope

*   The user login and registration process (`POST /login`, `POST /register`), which are prerequisites for this phase.
*   The management of Books, Groups, Accounts, or any other entities beyond the scope of session initialization.

---

## 2. Functional Specifications

### 2.1. FS-01: Fetch Initial Application State

The system must provide an endpoint that returns the core contextual data for the currently authenticated user. This allows the client application to load the correct user-specific workspace, including their default financial book and group.

### 2.2. FS-02: Bind Username to Account

The system must provide an endpoint that allows a user to convert a temporary or guest account into a permanent, credentialed account by binding a username and password to it, validated by an invitation code.

---

## 3. UI / UX Flow

While this PRD is for a backend API, the endpoints support the following user experience flows.

### 3.1. Application Loading Flow (`GET /initState`)

1.  A user successfully logs into the application.
2.  The client application, having received a JWT, immediately calls the `GET /initState` endpoint.
3.  A loading indicator is displayed to the user.
4.  Upon receiving the response, the client application populates the user's profile information, sets the active financial book and group, and displays the main dashboard.

### 3.2. Account Registration/Binding Flow (`PUT /bind`)

1.  A user is using the application with a temporary or guest account.
2.  The user is prompted to secure their account or complete their registration.
3.  The user navigates to a form where they must enter their desired **username**, a **password**, and a valid **invitation code**.
4.  The user submits the form.
5.  The backend validates the information and binds it to their account.
6.  The user can now log in using their new username and password.

---

## 4. Technical Specifications

### 4.1. API Logic

#### 4.1.1. `GET /initState`

*   **Description:** Gets the initial state for the current user, providing the necessary context to bootstrap the client application.
*   **Business Logic:**
    1.  The endpoint is protected and requires a valid JWT token.
    2.  The system extracts the `user_id` from the token.
    3.  It fetches the user's record from the database.
    4.  It retrieves the user's default book and default group, which are stored as foreign keys on the user's record.
    5.  The system assembles the user, book, and group information into dedicated View Objects (VOs) and returns them.

*   **Request Parameters:**
    *   **Headers:**
        *   `Authorization`: `Bearer <JWT_TOKEN>` (Mandatory)

*   **Responses and Scenarios:**
    *   **200 OK (Success):**
        ```json
        {
          "user": {
            "id": 1,
            "username": "krozario",
            "email": "krozario@example.com"
          },
          "book": {
            "id": 101,
            "name": "Personal Finances"
          },
          "group": {
            "id": 201,
            "name": "My Group"
          }
        }
        ```
    *   **401 Unauthorized:** Returned if the JWT token is missing, invalid, or expired.
    *   **404 Not Found:** Returned if the user ID in the JWT token does not correspond to any user in the database.

*   **Database CRUD Operations:**
    *   `READ`: From `t_user_user` to get user details.
    *   `READ`: From `t_user_book` to get the default book details.
    *   `READ`: From `t_user_group` to get the default group details.

*   **Database SQL Statements:**
    ```sql
    -- Get user from token user_id
    SELECT id, username, email, default_book_id, group_id FROM t_user_user WHERE id = ?;

    -- Get default book from user.default_book_id
    SELECT id, name FROM t_user_book WHERE id = ?;

    -- Get default group from user.group_id
    SELECT id, name FROM t_user_group WHERE id = ?;
    ```

#### 4.1.2. `PUT /bind`

*   **Description:** Binds a username and password to the current user's account, typically for upgrading a guest account.
*   **Business Logic:**
    1.  The endpoint requires a valid JWT for the user whose account is to be updated.
    2.  The system first validates the provided `inviteCode`. If the code is invalid or already used, the request is rejected.
    3.  The system checks if the desired `username` is already taken by another user. If it is, the request is rejected.
    4.  The system hashes the provided `password` using a secure hashing algorithm (e.g., bcrypt).
    5.  The `username` and hashed password are saved to the user's record in the `t_user_user` table.

*   **Request Parameters:**
    *   **Headers:**
        *   `Authorization`: `Bearer <JWT_TOKEN>` (Mandatory)
    *   **Body:**
        | Name | Data type | Optionality |
        |---|---|---|
        | `username` | String | Mandatory |
        | `password` | String | Mandatory |
        | `inviteCode` | String | Mandatory |

*   **Responses and Scenarios:**
    *   **200 OK (Success):** An empty body or a simple success message is returned.
    *   **400 Bad Request:**
        *   If the `username` is already in use. (Error code: `bind.username.exists`)
        *   If the `inviteCode` is invalid. (Error code: `bind.invite.code.invalid`)
        *   If the password does not meet security requirements (e.g., too short). (Error code: `bind.password.weak`)
    *   **401 Unauthorized:** Returned if the JWT token is missing, invalid, or expired.

*   **Database CRUD Operations:**
    *   `READ`: From `t_invite_code` (hypothetical table) to validate the invite code.
    *   `READ`: From `t_user_user` to check for username uniqueness.
    *   `UPDATE`: On `t_user_user` to set the username and password hash.

*   **Database SQL Statements:**
    ```sql
    -- Check if username is already taken
    SELECT COUNT(id) FROM t_user_user WHERE username = ?;

    -- Validate invite code (conceptual)
    SELECT is_valid FROM t_invite_code WHERE code = ?;

    -- Update the user record with new credentials
    UPDATE t_user_user SET username = ?, password_hash = ? WHERE id = ?;
    ```

---

## 5. Data Model

This phase primarily interacts with the following data models.

### 5.1. `User` (t_user_user)

| Attribute | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY` | Unique identifier for the user. |
| `username` | `VARCHAR` | `UNIQUE` | The user's chosen username. |
| `password_hash` | `VARCHAR` | | The securely hashed password. |
| `email` | `VARCHAR` | `UNIQUE` | The user's email address. |
| `default_book_id` | `INTEGER` | `FOREIGN KEY` -> `t_user_book(id)` | The ID of the book to load by default. |
| `group_id` | `INTEGER` | `FOREIGN KEY` -> `t_user_group(id)` | The ID of the group the user belongs to. |

### 5.2. `Book` (t_user_book)

| Attribute | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY` | Unique identifier for the book. |
| `name` | `VARCHAR` | `NOT NULL` | The user-defined name of the book. |
| `group_id` | `INTEGER` | `FOREIGN KEY` -> `t_user_group(id)` | The group this book belongs to. |

### 5.3. `Group` (t_user_group)

| Attribute | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY` | Unique identifier for the group. |
| `name` | `VARCHAR` | `NOT NULL` | The name of the group. |

---

## 6. Test Cases

| Test Case ID | Endpoint | Feature Being Tested | Test Steps | Expected Result |
|---|---|---|---|---|
| **TC-P2-01** | `GET /initState` | **Happy Path** - Successful retrieval | 1. Log in with a valid user. <br> 2. Make a GET request to `/initState`. | **200 OK** with a JSON body containing the correct user, book, and group info. |
| **TC-P2-02** | `GET /initState` | **Negative Path** - Invalid Token | 1. Make a GET request to `/initState` with a malformed or expired token. | **401 Unauthorized**. |
| **TC-P2-03** | `GET /initState` | **Boundary** - User with no default book | 1. Log in with a user where `default_book_id` is NULL. <br> 2. Make a GET request to `/initState`. | **200 OK**, with the `book` field in the JSON response being `null`. |
| **TC-P2-04** | `PUT /bind` | **Happy Path** - Successful binding | 1. Log in with a temporary user. <br> 2. Make a PUT request to `/bind` with a unique username, valid password, and valid invite code. | **200 OK**. The user record in the database is updated with the new username and password hash. |
| **TC-P2-05** | `PUT /bind` | **Negative Path** - Username taken | 1. Log in with a temporary user. <br> 2. Make a PUT request to `/bind` with a username that already exists. | **400 Bad Request** with an appropriate error code (`bind.username.exists`). |
| **TC-P2-06** | `PUT /bind` | **Negative Path** - Invalid Invite Code | 1. Log in with a temporary user. <br> 2. Make a PUT request to `/bind` with an invalid or expired invite code. | **400 Bad Request** with an appropriate error code (`bind.invite.code.invalid`). |
| **TC-P2-07** | `PUT /bind` | **Security** - Password Hashing | 1. Successfully execute the `/bind` endpoint. <br> 2. Inspect the `t_user_user` table in the database. | The `password_hash` column for the user should contain a long, salted hash, not the plaintext password. |

---

## 7. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **`initState` payload bloat** | Medium | Medium | Over time, more "initial state" might be added, slowing down app startup. **Mitigation:** Strictly govern what is included in this response. Keep it limited to only the data needed to bootstrap the UI. Defer loading of non-essential data to other dedicated endpoints. |
| **Insecure `bind` process** | Low | High | If the password is not handled securely, user credentials could be compromised. **Mitigation:** Enforce strong password policies and use a modern, salted hashing algorithm (like bcrypt) for storing passwords. Never log plaintext passwords. |
| **Race conditions on username** | Low | Medium | Two users could attempt to bind the same username at nearly the same time. **Mitigation:** Enforce a `UNIQUE` constraint on the `username` column in the `t_user_user` database table. This provides the ultimate guarantee of uniqueness. |

---

## 8. Open Questions

1.  What are the exact fields required for the `UserSessionVo`, `BookSessionVo`, and `GroupSessionVo` objects? (Assumption: For this PRD, we assume they contain `id` and `name` as a minimum).
2.  What is the source and validation logic for `inviteCode`? Is there a dedicated `t_invite_code` table? (Assumption: Yes, a table exists to manage valid codes).
3.  Are there specific password strength requirements (length, complexity) that need to be enforced by the API?

---

## 9. Task Seeds (for Agent Decomposition)

*   **Backend:**
    *   Create router and controller for `GET /initState`.
    *   Implement `UserService.get_initial_state()` to fetch user, book, and group data.
    *   Create router and controller for `PUT /bind`.
    *   Implement `UserService.bind_user()` to handle validation and updating of user credentials.
    *   Add validation logic for username uniqueness.
    *   Add validation logic for the invitation code.
    *   Implement secure password hashing using bcrypt.
*   **Testing:**
    *   Write unit tests for `UserService.get_initial_state()`.
    *   Write unit tests for `UserService.bind_user()`, covering all success and failure cases.
    *   Write integration tests for the `GET /initState` endpoint.
    *   Write integration tests for the `PUT /bind` endpoint, simulating API calls.
*   **Documentation:**
    *   Update the API documentation (e.g., Swagger/OpenAPI) for the two new endpoints.

## Completed Task so far

The following task have been executed and completed, do not repeat them, assume their output is ready for use for tasks in the future:
- [✔] Define Pydantic Schemas and Create Static Data Files
- [✔] Add Version and Base URL to Application Configuration
- [✔] Create Data Loader Service for Caching Static JSON
- [✔] Integrate Data Loader into Application Startup
- [✔] Implement `GET /version` Endpoint
- [✔] Implement `GET /test3` Endpoint
- [✔] Implement `GET /currencies/all` Endpoint
- [✔] Implement `GET /book-templates/all` Endpoint
- [✔] Include New Routers in Main Application
- [✔] Write Integration Tests for All Phase 1 Endpoints# Moneynote API - Detailed Design Document

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
