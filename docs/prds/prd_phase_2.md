# Product Requirements Document: Moneynote API - Phase 2

## 1. Goal & Scope

**Goal:** To implement the core user session initialization endpoints for the Moneynote API. 

**Scope:** This phase focuses on providing the necessary data for the frontend to initialize after a user logs in. This includes fetching the user's profile, their default book and group settings, and providing a mechanism to bind a username and password to an existing account. This phase is critical for establishing the user's context within the application.

## 2. Functional Specifications

This phase will implement the following API endpoints:

*   **`GET /initState`**: Retrieves a comprehensive initial state object for the logged-in user, including user details, and their default group and book settings. This is the primary endpoint called by the frontend after login.
*   **`PUT /bind`**: Allows an authenticated user to associate a username, password, and invitation code with their account. This is typically for users who may have registered through an alternative method and need to set up standard credentials.

## 3. UI / UX Flow

While this document specifies the backend API, the intended UI/UX flow is as follows:

1.  A user successfully logs in using their credentials (or a third-party provider).
2.  The frontend application, having received an authentication token, immediately calls the `GET /initState` endpoint.
3.  The data returned from `/initState` is used to populate the user's session, including their name, default currency, and the currently active financial "Book" and "Group". The UI then renders the main dashboard, scoped to the user's default book.
4.  If a user's account does not have a username/password (e.g., created via a social login), the UI may prompt them to "secure their account" or "set a password". This flow would lead to a form that collects a username, password, and potentially an invite code, which is then submitted to the `PUT /bind` endpoint.

## 4. Technical Specifications

### 4.1 API Logic

---

#### **Endpoint: `GET /initState`**

Retrieves the essential session information for the currently authenticated user.

*   **Business Logic:**
    This endpoint serves as the primary data source for the client application upon startup. It fetches the user's record, identifies their default `Group` and `Book`, and returns a consolidated object containing the necessary details for the UI to render its initial state. This ensures that the user always returns to their last-used context.

    *If a user does not have a default book or group, the system should return the first book/group they have access to, or null if none exist.*

*   **Request:**
    *   **Method:** `GET`
    *   **Path:** `/initState`
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)

*   **Responses:**
    *   **200 OK (Success):**
        ```json
        {
          "user": {
            "username": "string",
            "email": "user@example.com",
            "is_active": true
          },
          "book": {
            "id": "integer",
            "name": "string",
            "default_currency_code": "string"
          },
          "group": {
            "id": "integer",
            "name": "string"
          }
        }
        ```
    *   **401 Unauthorized:** If the JWT token is missing, invalid, or expired.
    *   **404 Not Found:** If the user associated with the token cannot be found.

*   **Database CRUD Operations:**
    1.  `READ`: Fetch the `User` from the `user` table based on the ID from the JWT token.
    2.  `READ`: Fetch the default `Book` from the `book` table using `user.default_book_id`.
    3.  `READ`: Fetch the default `Group` from the `group` table using `user.default_group_id`.

*   **Database SQL Statements (Illustrative):**
    ```sql
    -- Get user from token
    SELECT id, username, email, is_active, default_book_id, default_group_id FROM "user" WHERE id = ?;

    -- Get default book
    SELECT id, name, default_currency_code FROM book WHERE id = ?; -- using default_book_id from user

    -- Get default group
    SELECT id, name FROM "group" WHERE id = ?; -- using default_group_id from user
    ```

---

#### **Endpoint: `PUT /bind`**

Binds a username and password to the currently authenticated user account.

*   **Business Logic:**
    This endpoint is used to "claim" or fully register an account that was created without a standard username/password credential set. It takes a desired username and password, validates them, and updates the user's record. The `inviteCode` is likely used as a security measure or for tracking sign-up sources, and its validation logic must be confirmed.

*   **Request:**
    *   **Method:** `PUT`
    *   **Path:** `/bind`
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)
    *   **Body:**
        ```json
        {
          "username": "string",
          "password": "string",
          "inviteCode": "string"
        }
        ```

*   **Responses:**
    *   **200 OK (Success):** Returns a success message or status.
        ```json
        {
          "status": "success",
          "message": "User credentials bound successfully."
        }
        ```
    *   **400 Bad Request:**
        *   If the `username` is already taken.
        *   If the `inviteCode` is invalid or expired.
        *   If the user account already has a username/password bound.
    *   **401 Unauthorized:** If the JWT token is missing, invalid, or expired.

*   **Database CRUD Operations:**
    1.  `READ`: Fetch the `User` from the `user` table based on the ID from the JWT token.
    2.  `READ`: Check if the requested `username` already exists in the `user` table.
    3.  `UPDATE`: Update the `user` record for the current user, setting the `username` and `hashed_password` fields.

*   **Database SQL Statements (Illustrative):**
    ```sql
    -- Get current user
    SELECT id, username FROM "user" WHERE id = ?;

    -- Check if new username is taken
    SELECT id FROM "user" WHERE username = ?;

    -- Update user record with new credentials (password should be hashed by the application)
    UPDATE "user" SET username = ?, hashed_password = ? WHERE id = ?;
    ```

## 5. Data Model

This phase affects the following data models (read and write operations).

*   **`User` (`user` table):**
    *   `id`: Integer, Primary Key
    *   `username`: String, Unique
    *   `hashed_password`: String
    *   `email`: String
    *   `is_active`: Boolean
    *   `default_book_id`: Integer, Foreign Key to `book.id`
    *   `default_group_id`: Integer, Foreign Key to `group.id`

*   **`Book` (`book` table):**
    *   `id`: Integer, Primary Key
    *   `name`: String
    *   `group_id`: Integer, Foreign Key to `group.id`
    *   `default_currency_code`: String

*   **`Group` (`"group"` table):**
    *   `id`: Integer, Primary Key
    *   `name`: String
    *   `owner_id`: Integer, Foreign Key to `user.id`

## 6. Test Cases

| Test Case ID | Endpoint | Feature | Preconditions | Test Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-PH2-01** | `GET /initState` | Happy Path | User exists with `default_book_id=1` and `default_group_id=1`. | 1. Log in to get a valid token. <br> 2. Make a GET request to `/initState`. | 200 OK. The response body contains the correct user, book, and group objects. |
| **TC-PH2-02** | `GET /initState` | No Default Book | User exists but `default_book_id` is `NULL`. User has access to at least one book. | 1. Log in. <br> 2. Make a GET request to `/initState`. | 200 OK. The `book` object in the response should be the first book the user has access to, or null. |
| **TC-PH2-03** | `GET /initState` | Invalid Token | - | 1. Make a GET request to `/initState` with an invalid or expired token. | 401 Unauthorized. |
| **TC-PH2-04** | `PUT /bind` | Happy Path | User is authenticated but has no `username`. The desired username is available. `inviteCode` is valid. | 1. Log in. <br> 2. Make a PUT request to `/bind` with a new username, password, and invite code. | 200 OK. The user record in the database is updated with the new username and hashed password. |
| **TC-PH2-05** | `PUT /bind` | Username Taken | Another user already has the username "testuser". | 1. Log in. <br> 2. Make a PUT request to `/bind` with username "testuser". | 400 Bad Request with an error message like "Username already taken." |
| **TC-PH2-06** | `PUT /bind` | Account Already Bound | The authenticated user already has a `username` set. | 1. Log in. <br> 2. Make a PUT request to `/bind`. | 400 Bad Request with an error message like "Account already has credentials." |
| **TC-PH2-07** | `PUT /bind` | Invalid Invite Code | The provided `inviteCode` is not valid. | 1. Log in. <br> 2. Make a PUT request to `/bind` with an invalid invite code. | 400 Bad Request with an error message like "Invalid invitation code." |

## 7. Risks & Mitigations

| Risk | Mitigation |
| :--- | :--- |
| **Performance of `GET /initState`:** As more data is added to the initial state payload, this endpoint could become slow, impacting app load time. | Keep the `initState` payload lean. For any large datasets (e.g., lists of accounts, categories), create separate, dedicated endpoints with pagination. |
| **Security of `PUT /bind`:** An improperly secured `bind` endpoint could allow account takeovers. | Enforce strict validation on the `inviteCode`. Implement rate limiting to prevent brute-force attacks. Ensure the user is properly authenticated and authorized to modify their own account. |
| **Inconsistent State:** If a user's default book or group is deleted, `GET /initState` could fail or return invalid data. | Implement a fallback mechanism. When a book/group is deleted, the system should intelligently re-assign the user's default to another valid entity or set it to `NULL`. The `/initState` logic should handle `NULL` defaults gracefully. |

## 8. Open Questions

1.  What is the precise validation logic for the `inviteCode` in the `PUT /bind` endpoint? Is it a static value, a pattern, or a value from a database table?
2.  What is the expected behavior of `GET /initState` if a user is part of a group but no books have been created yet? Should the `book` field be `null`? (Assumption: Yes).
3.  Should the `PUT /bind` endpoint also log the user in with the new credentials immediately, or does it only associate them?

## 9. Task Seeds (for Agent Decomposition)

1.  **Task:** Create router and schema for `GET /initState`.
2.  **Task:** Implement service logic for `get_initial_state` to fetch user, default book, and default group.
3.  **Task:** Write unit and integration tests for the `GET /initState` endpoint, covering all scenarios from the test cases.
4.  **Task:** Create router and schema for `PUT /bind`.
5.  **Task:** Implement service logic for `bind_user` to validate input and update the user record with a username and hashed password.
6.  **Task:** Write unit and integration tests for the `PUT /bind` endpoint, covering success, duplicate username, and invalid code scenarios.
7.  **Task:** Define the data structures (`schemas`) for the response objects (`UserSessionVo`, `BookSessionVo`, `GroupSessionVo`).

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
