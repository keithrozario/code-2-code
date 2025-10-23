# Product Requirements Document: Moneynote API - Phase 2

## 1. Goal & Scope

**Goal:** To enhance user account management and streamline the application initialization process.

**Scope:** This phase focuses on two key features: allowing existing users to bind a permanent username and password to their accounts, and providing a single endpoint to fetch the essential initial state (User, Book, Group) required for the frontend to render the user's context after login. This PRD covers the backend API implementation for these features.

---

## 2. Functional Specifications

*   **FS-001: User Account Binding:** An authenticated user, potentially a guest or temporary user, must be able to secure their account by associating it with a unique username and a password.
*   **FS-002: Initial State Hydration:** Upon successful login or session resumption, the client application must be able to fetch a consolidated payload containing the current user's information, their default financial "Book," and their default "Group."

---

## 3. UI / UX Flow

This PRD focuses on the backend API. The UI/UX flow describes the client-side interactions that trigger the APIs defined in this document.

**Flow 1: Securing an Account**
1.  A user who is already logged in (e.g., as a guest) navigates to their "Profile" or "Account Settings" page.
2.  The user clicks an option like "Secure Your Account" or "Register Username."
3.  A form is presented asking for a `username`, `password`, and an `inviteCode`.
4.  The user fills out the form and clicks "Submit."
5.  The client makes a `PUT /bind` request to the backend.
6.  Upon success, the UI confirms that the account is now secured, and the user can log in with these credentials in the future. On failure, an appropriate error message is displayed (e.g., "Username already taken").

**Flow 2: Application Loading**
1.  A user successfully logs in or returns to the application with a valid session.
2.  The client application immediately makes a `GET /initState` request to the backend.
3.  While the request is in flight, the UI may display a loading spinner or a skeleton screen.
4.  Upon receiving the response, the client application populates the user's context:
    *   The user's name/avatar is displayed.
    *   The application sets the active financial "Book" and "Group" to the defaults returned by the API.
    *   All subsequent API requests for financial data will use the retrieved Book and Group IDs.
5.  The main dashboard, showing data for the default book, is rendered.

---

## 4. Technical Specifications

### 4.1 API Logic

#### **Endpoint: `PUT /bind`**

Binds a username and password to the currently authenticated user, formalizing their account.

*   **Business Logic:**
    1.  The system receives the request and authenticates the user via the provided JWT in the `Authorization` header.
    2.  It validates that the provided `username` is not already in use by another user in the `t_user_user` table. If it is, a `400 Bad Request` error is returned.
    3.  The system validates the `inviteCode` (logic to be confirmed, assumed to be a check against a predefined list or pattern).
    4.  The provided `password` is securely hashed using a strong hashing algorithm (e.g., bcrypt).
    5.  The current user's record in the `t_user_user` table is updated with the new `username` and `hashed_password`.

*   **Request Parameters:**

    **Header:**
    | Name | Description | Data type | Optionality |
    |---|---|---|---|
    | `Authorization` | Bearer token | String | Mandatory |

    **Body:**
    | Name | Description | Data type | Optionality |
    |---|---|---|---|
    | `username` | The desired username. | String | Mandatory |
    | `password` | The desired password. | String | Mandatory |
    | `inviteCode` | An invitation code. | String | Mandatory |

*   **Responses and Scenarios:**
    *   **200 OK:** The binding was successful. The user account is updated.
    *   **400 Bad Request:** The username is already taken, the invite code is invalid, or the password is too weak.
    *   **401 Unauthorized:** The user's JWT is invalid or expired.

*   **Database CRUD Operations:**
    *   **READ:** Check for the existence of the `username` in the `t_user_user` table.
    *   **UPDATE:** Update the `username` and `hashed_password` fields for the current user's record in the `t_user_user` table.

*   **Database SQL Statements:**
    ```sql
    -- Check for existing username
    SELECT id FROM t_user_user WHERE username = '<provided_username>';

    -- Update user record
    UPDATE t_user_user
    SET username = '<provided_username>', hashed_password = '<hashed_password>'
    WHERE id = <current_user_id>;
    ```

---

#### **Endpoint: `GET /initState`**

Fetches the essential session context for the currently authenticated user.

*   **Business Logic:**
    1.  The system receives the request and authenticates the user via the provided JWT in the `Authorization` header, retrieving the current user object.
    2.  It fetches the full user details from the `t_user_user` table based on the user's ID.
    3.  It uses the `default_book_id` from the user object to fetch the user's default book details from the `t_user_book` table.
    4.  It uses the `default_group_id` from the user object to fetch the user's default group details from the `t_user_group` table.
    5.  The system constructs a response object containing the user, book, and group information.

*   **Request Parameters:**

    **Header:**
    | Name | Description | Data type | Optionality |
    |---|---|---|---|
    | `Authorization` | Bearer token | String | Mandatory |

*   **Responses and Scenarios:**
    *   **200 OK:** Returns the initial state object.
        **Response Body:**
        | Name | Description | Data type |
        |---|---|---|
        | `user` | User information | `UserSessionVo` |
        | `book` | Default book information | `BookSessionVo` |
        | `group` | Default group information| `GroupSessionVo` |
    *   **401 Unauthorized:** The user's JWT is invalid or expired.
    *   **404 Not Found:** The user's default book or group as specified in their profile does not exist in the database.

*   **Database CRUD Operations:**
    *   **READ:** Fetch the user record from `t_user_user`.
    *   **READ:** Fetch the book record from `t_user_book` using `user.default_book_id`.
    *   **READ:** Fetch the group record from `t_user_group` using `user.default_group_id`.

*   **Database SQL Statements:**
    ```sql
    -- Get User (occurs in authentication middleware)
    SELECT * FROM t_user_user WHERE id = <current_user_id>;

    -- Get Default Book
    SELECT id, name, default_currency_code FROM t_user_book WHERE id = <user.default_book_id>;

    -- Get Default Group
    SELECT id, name, default_currency_code FROM t_user_group WHERE id = <user.default_group_id>;
    ```

---

## 5. Data Model

This phase primarily interacts with the following existing data models.

**`User` (Table: `t_user_user`)**
| Attribute | Data Type | Description |
|---|---|---|
| `id` | `INTEGER` | Primary Key |
| `username` | `VARCHAR` | The user's unique username. Nullable until bound. |
| `hashed_password` | `VARCHAR` | The user's hashed password. Nullable until bound. |
| `default_book_id` | `INTEGER` | Foreign Key to `t_user_book.id`. |
| `default_group_id`| `INTEGER` | Foreign Key to `t_user_group.id`. |
| ...other fields | | |

**`Book` (Table: `t_user_book`)**
| Attribute | Data Type | Description |
|---|---|---|
| `id` | `INTEGER` | Primary Key |
| `name` | `VARCHAR` | The name of the book. |
| `group_id` | `INTEGER` | Foreign Key to `t_user_group.id`. |
| `default_currency_code` | `VARCHAR` | The default currency for this book. |
| ...other fields | | |

**`Group` (Table: `t_user_group`)**
| Attribute | Data Type | Description |
|---|---|---|
| `id` | `INTEGER` | Primary Key |
| `name` | `VARCHAR` | The name of the group. |
| `default_currency_code` | `VARCHAR` | The default currency for this group. |
| ...other fields | | |

---

## 6. Test Cases

| Test Case ID | Endpoint | Feature | Test Steps | Expected Result |
|---|---|---|---|---|
| **TC-P2-01** | `PUT /bind` | Happy Path | 1. Authenticate as a user without a username. <br> 2. Call `PUT /bind` with a unique username, valid password, and valid invite code. | **200 OK**. The user record in `t_user_user` is updated with the new username and hashed password. |
| **TC-P2-02** | `PUT /bind` | Username Exists | 1. Authenticate. <br> 2. Call `PUT /bind` with a username that is already taken. | **400 Bad Request** with an error message like "Username already exists." |
| **TC-P2-03** | `PUT /bind` | Invalid Invite Code | 1. Authenticate. <br> 2. Call `PUT /bind` with an invalid `inviteCode`. | **400 Bad Request** with an error message about the invite code. |
| **TC-P2-04** | `GET /initState` | Happy Path | 1. Authenticate as a user with valid `default_book_id` and `default_group_id`. <br> 2. Call `GET /initState`. | **200 OK**. The response contains non-null `user`, `book`, and `group` objects with correct details. |
| **TC-P2-05** | `GET /initState` | Null Defaults | 1. Authenticate as a user where `default_book_id` is `NULL`. <br> 2. Call `GET /initState`. | **200 OK**. The response contains a `user` object, but the `book` object is `null`. |
| **TC-P2-06** | `GET /initState` | Invalid Foreign Key | 1. Authenticate as a user where `default_book_id` points to a non-existent book. <br> 2. Call `GET /initState`. | **404 Not Found**. An error is returned because the default book cannot be found. |

---

## 7. Risks & Mitigations

*   **Risk:** Insecure password handling during the `bind` process.
    *   **Mitigation:** Ensure industry-standard password hashing (e.g., bcrypt with a sufficient cost factor) is used. Never log plain-text passwords.
*   **Risk:** Race condition where two users attempt to bind the same username simultaneously.
    *   **Mitigation:** Enforce a `UNIQUE` constraint on the `username` column in the `t_user_user` database table.
*   **Risk:** Performance degradation on `initState` if fetching the user, book, and group involves complex queries.
    *   **Mitigation:** Ensure that `id`, `default_book_id`, and `default_group_id` are all indexed for fast lookups.

---

## 8. Open Questions

1.  What is the specific validation logic for the `inviteCode` on the `/bind` endpoint? Is it a static code, a pattern, or looked up from a table?
2.  What should be the system's behavior in `initState` if a user's default book or group has been disabled (`enable=false`)? Should it return the disabled entity or fall back to another one?

---

## 9. Task Seeds (for Agent Decomposition)

1.  **API Endpoint (`/bind`):**
    *   Create a new route `PUT /bind` in `moneynote/routers/users.py`.
    *   Implement the request body model for the bind operation.
    *   Add a function to `moneynote/crud/crud_user.py` to handle the username existence check and the database update.
    *   Integrate password hashing utility.
2.  **API Endpoint (`/initState`):**
    *   Create a new route `GET /initState` in `moneynote/routers/users.py`.
    *   Implement the service logic to fetch the user, book, and group objects.
    *   Create the `UserSessionVo`, `BookSessionVo`, and `GroupSessionVo` response schemas if they don't exist.
3.  **Testing:**
    *   Write unit tests for the `bind` CRUD logic.
    *   Write unit tests for the `initState` service logic.
    *   Write integration tests for both the `PUT /bind` and `GET /initState` endpoints.

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
