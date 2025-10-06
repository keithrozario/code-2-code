# Product Requirements Document: Moneynote API - Phase 1

## 1. Goal & Scope

**Goal:** To establish the foundational, independent API endpoints for the Moneynote application.

**Scope:** This phase focuses on delivering five core, non-dependent endpoints that are essential for basic application setup and user onboarding. This includes application versioning, user registration, and the retrieval of static configuration data like currencies and book templates. This PRD covers only the backend API implementation for Phase 1 as defined in the `api_plan.md`.

---

## 2. Functional Specifications

- **FS-001:** The system shall provide an endpoint to return its current version.
- **FS-002:** The system shall provide a test endpoint that returns the application's base URL.
- **FS-003:** The system shall allow a new user to register for the application.
- **FS-004:** The system shall provide a list of all supported currencies.
- **FS-005:** The system shall provide a list of all available book templates.

---

## 3. UI / UX Flow

This document pertains exclusively to the backend API. No user interface is being developed in this phase. The user flow consists of API clients making requests to the specified endpoints and receiving JSON responses.

- **Registration Flow:** A client sends a `POST` request with user credentials. The API validates the data, creates a new user record, and returns a success or error response.
- **Data Retrieval Flow:** A client sends a `GET` request to the version, test, currency, or book template endpoint. The API returns the requested data in a JSON format.

---

## 4. Technical Specifications

### 4.1 API Logic

#### 4.1.1 `GET /version`

-   **Description:** Returns the static application version. This is a simple endpoint for health checks and version tracking.
-   **Request Parameters:** None.
-   **Responses:**
    -   **200 OK:**
        ```json
        {
          "data": "1.0.0"
        }
        ```
    -   **401 Unauthorized:** If the JWT token is missing or invalid.
-   **Database CRUD:** None.
-   **SQL Statements:** None.

#### 4.1.2 `GET /test3`

-   **Description:** A test endpoint that returns the base URL of the application. Used for connectivity and configuration testing.
-   **Request Parameters:** None.
-   **Responses:**
    -   **200 OK:**
        ```json
        {
          "data": "http://localhost:8080"
        }
        ```
    -   **401 Unauthorized:** If the JWT token is missing or invalid.
-   **Database CRUD:** None.
-   **SQL Statements:** None.

#### 4.1.3 `POST /register`

-   **Description:** Registers a new user in the system. It takes a username and password, hashes the password, and creates a new user record. This endpoint does not require authentication.
-   **Request Parameters:**
    | Name | Description | Data type | Optionality |
    | :--- | :--- | :--- | :--- |
    | `username` | User's desired username | String | Mandatory |
    | `password` | User's desired password | String | Mandatory |
    | `inviteCode`| Invitation code | String | Mandatory |
-   **API Logic:**
    1.  Validate that `username` and `password` are not empty.
    2.  Check if a user with the given `username` already exists in the database. If so, return an error.
    3.  (Assumption) Validate the `inviteCode`. If invalid, return an error.
    4.  Hash the provided `password` using a secure hashing algorithm (e.g., bcrypt).
    5.  Create a new `User` entity with the `username` and `hashed_password`.
    6.  Save the new `User` entity to the database.
-   **Responses:**
    -   **200 OK:** On successful registration. The response body is empty.
    -   **400 Bad Request:** If `username` or `password` are missing, or if the `username` already exists.
        ```json
        {
          "error": "Username already exists."
        }
        ```
-   **Database CRUD:** `CREATE`
-   **SQL Statements:**
    ```sql
    -- Check for existing user
    SELECT * FROM "user" WHERE username = '<username>';

    -- Insert new user
    INSERT INTO "user" (username, hashed_password, email, is_active) VALUES ('<username>', '<hashed_password>', NULL, true);
    ```

#### 4.1.4 `GET /currencies/all`

-   **Description:** Retrieves a list of all supported currencies and their exchange rates. The data is loaded into memory from the `currency.json` file at application startup.
-   **Request Parameters:** None.
-   **Responses:**
    -   **200 OK:**
        ```json
        [
          {
            "id": 1,
            "name": "USD",
            "description": "United States Dollar",
            "rate": 1.0
          },
          {
            "id": 2,
            "name": "EUR",
            "description": "Euro",
            "rate": 0.92
          }
        ]
        ```
    -   **401 Unauthorized:** If the JWT token is missing or invalid.
-   **Database CRUD:** None. Data is read from in-memory cache.
-   **SQL Statements:** None.

#### 4.1.5 `GET /book-templates/all`

-   **Description:** Retrieves a list of all available book templates. The data is loaded from the `book_tpl.json` file.
-   **Request Parameters:** None.
-   **Responses:**
    -   **200 OK:**
        ```json
        [
          {
            "id": 1,
            "name": "Default Template"
          },
          {
            "id": 2,
            "name": "Business Template"
          }
        ]
        ```
    -   **401 Unauthorized:** If the JWT token is missing or invalid.
-   **Database CRUD:** None. Data is read from a JSON file.
-   **SQL Statements:** None.

---

## 5. Data Model

This phase primarily introduces the `User` data model.

### `User` Entity (`user` table)

| Attribute | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `PRIMARY KEY` | Unique identifier for the user. |
| `username` | `String` | `NOT NULL`, `UNIQUE` | The user's chosen username. |
| `hashed_password` | `String` | `NOT NULL` | The securely hashed password. |
| `email` | `String` | `UNIQUE` | The user's email address (optional). |
| `is_active` | `Boolean` | `NOT NULL` | Flag to indicate if the user account is active. |

---

## 6. Test Cases

| Test Case ID | Endpoint | Feature | Test Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-P1-01** | `GET /version` | Version Check | Make a GET request to `/version`. | HTTP 200 OK. Response body contains the version string. |
| **TC-P1-02** | `GET /test3` | Test Endpoint | Make a GET request to `/test3`. | HTTP 200 OK. Response body contains the base URL. |
| **TC-P1-03** | `POST /register` | User Registration (Happy Path) | Make a POST request with a unique username and password. | HTTP 200 OK. A new user record is created in the database. |
| **TC-P1-04** | `POST /register` | User Registration (Duplicate) | Make a POST request with a username that already exists. | HTTP 400 Bad Request. Error message indicating the username is taken. |
| **TC-P1-05** | `POST /register` | User Registration (Validation) | Make a POST request with a missing password. | HTTP 400 Bad Request. Error message indicating a missing field. |
| **TC-P1-06** | `GET /currencies/all` | Get Currencies | Make a GET request to `/currencies/all`. | HTTP 200 OK. Response body is a JSON array of currency objects. |
| **TC-P1-07** | `GET /book-templates/all`| Get Book Templates | Make a GET request to `/book-templates/all`. | HTTP 200 OK. Response body is a JSON array of book template objects. |

---

## 7. Risks & Mitigations

| Risk | Mitigation |
| :--- | :--- |
| **Undefined Invite Code Logic:** The validation logic for the `inviteCode` on registration is not specified. | **Mitigation:** For Phase 1, any non-empty string will be considered valid. This will be flagged as an open question for clarification in a future phase. |
| **Hardcoded Configuration:** The version number and base URL may be hardcoded. | **Mitigation:** These values should be loaded from a configuration file to allow for easier updates without code changes. |
| **File Dependencies:** The system depends on `currency.json` and `book_tpl.json` being present at startup. | **Mitigation:** The application should implement a robust startup check that verifies the existence and validity of these files, logging a clear error if they are missing or corrupt. |

---

## 8. Open Questions

1.  What is the definitive validation logic for the `inviteCode` during registration? Is it a static value, or is it dynamically generated?
2.  What is the source of truth for the application version returned by `GET /version`? (e.g., a build file, a config file).

---

## 9. Task Seeds (for Agent Decomposition)

1.  **Task 1.1:** Implement the `GET /version` endpoint to return a static version string from a configuration file.
2.  **Task 1.2:** Implement the `GET /test3` endpoint to return the application's base URL from a configuration file.
3.  **Task 1.3:** Implement the `User` data model (SQLAlchemy or equivalent) corresponding to the `user` table.
4.  **Task 1.4:** Implement the `POST /register` endpoint, including username existence check and password hashing.
5.  **Task 1.5:** Implement the in-memory loading mechanism for `currency.json`.
6.  **Task 1.6:** Implement the `GET /currencies/all` endpoint to serve data from the in-memory currency cache.
7.  **Task 1.7:** Implement the loading mechanism for `book_tpl.json`.
8.  **Task 1.8:** Implement the `GET /book-templates/all` endpoint to serve data from the book template file.
9.  **Task 1.9:** Write unit and integration tests covering all test cases outlined in section 6.


# Moneynote API Detailed Design

This document outlines the detailed design for the Moneynote backend API, based on the provided API definitions, dependencies, build plan, and architecture principles.

## 1. Overall Architecture

The Moneynote API will be a Python-based backend built using the **FastAPI** framework, adhering to the specified architecture principles.

-   **Application Type**: Web-based, API-driven backend.
-   **Deployment**: The application is designed to be deployed as a **Google Cloud Run** service. Due to the use of a single SQLite database file, the service will be configured to run as a single instance.
-   **API Gateway**: The backend will operate behind an API Gateway (such as a Google Cloud Load Balancer). The gateway is responsible for validating JWTs for authentication. The backend will not perform JWT validation or issuance.
-   **Database**: A relational database using **SQLite3** will serve as the primary datastore. All data logic will be in the backend, with no triggers or stored procedures in the database itself. **SQLAlchemy** will be used as the ORM for database interactions.
-   **File Storage**: All file uploads (e.g., receipts, documents associated with transactions) will be stored in a **Google Cloud Storage (GCS)** bucket.
-   **User Identity**: The backend will infer the user's identity from the `sub` claim within the JWT, which is passed in the `Authorization: Bearer` header by the upstream gateway.

## 2. Design Considerations

### 2.1. Authentication and Authorization

-   **Authentication**: The API relies on an external identity provider and gateway for authentication. The backend will receive a valid JWT and can trust its contents. The user's unique identifier will be extracted from the `sub` claim of the token. A dependency injection utility will be created in FastAPI to extract the user identity from the request header and make it available to endpoint functions.
-   **Authorization**: Resource-level protection will be implemented within the backend. Business logic in the service layer will be responsible for verifying that the authenticated user (from the JWT `sub`) has the necessary permissions to access or modify a resource. This is particularly important in a multi-tenant system where users belong to groups and books. For example, before accessing a book's details, the service will verify that the user is a member of the group that owns the book.

### 2.2. Data Model (SQLAlchemy Models)

The database schema will be defined using SQLAlchemy ORM models. The primary entities are derived from the API definition:

-   **User**: Stores user information (`id`, `username`, `password_hash`).
-   **Group**: Represents a collection of users sharing books (`id`, `name`, `owner_id`).
-   **Book**: A ledger or a collection of financial records (`id`, `name`, `group_id`, `default_currency_code`).
-   **Account**: Represents a financial account like a bank account or credit card (`id`, `book_id`, `name`, `type`, `balance`).
-   **Category**: User-defined categories for income/expense (`id`, `book_id`, `name`, `type`, `parent_id`).
-   **Payee**: Represents the other party in a transaction (`id`, `book_id`, `name`).
-   **Tag**: User-defined tags for transactions (`id`, `book_id`, `name`).
-   **BalanceFlow**: The core transaction record (`id`, `book_id`, `account_id`, `amount`, `type`, `create_time`).
-   **FlowFile**: A record linking a `BalanceFlow` to a file stored in GCS (`id`, `balance_flow_id`, `gcs_object_name`).
-   **NoteDay**: For recurring reminders or notes.

Relationships will be defined between these models (e.g., one-to-many, many-to-many) to reflect the application's logic, such as the relationship between a `Book` and its `Accounts`.

### 2.3. Configuration

Application configuration will be managed via environment variables, following the twelve-factor app methodology. A Pydantic `Settings` class will be used to load and validate these variables.

-   `DATABASE_URL`: The connection string for the SQLite database (e.g., `sqlite:///./moneynote.db`).
-   `GCS_BUCKET_FLOW_FILES`: The name of the Google Cloud Storage bucket for storing transaction-related files.

### 2.4. Error Handling

The API will use FastAPI's built-in exception handling capabilities. Custom exception classes will be created for specific business logic errors (e.g., `ResourceNotFound`, `PermissionDenied`). These exceptions will be caught by custom exception handlers to return standardized JSON error responses with appropriate HTTP status codes (e.g., 404, 403, 400).

### 2.5. File Handling

File uploads will be handled via `POST` endpoints that accept `multipart/form-data`. The process will be:
1.  The API receives the file.
2.  The service layer generates a unique object name (e.g., using UUID).
3.  The file is uploaded to the configured GCS bucket using the `google-cloud-storage` Python library.
4.  A `FlowFile` record is created in the database to associate the GCS object name with the corresponding `BalanceFlow` record.
File downloads/views will generate a signed URL for the GCS object, allowing the client to securely access the file directly from GCS for a limited time.

## 3. Overall Structure of Files

The project will follow a standard FastAPI application structure to organize code logically by feature and layer.

```
/Users/krozario/projects/trial_4/moneynote_api_py/
├── .gitignore
├── pyproject.toml
├── uv.lock
├── main.py                 # FastAPI app instantiation and main router
├── config.py               # Pydantic settings management for env vars
├── database.py             # SQLAlchemy engine, session management
│
├── alembic/                # Alembic database migration scripts
│   ├── versions/
│   └── env.py
│
├── moneynote/
│   ├── __init__.py
│   │
│   ├── crud/               # Low-level database create, read, update, delete functions
│   │   ├── crud_account.py
│   │   ├── crud_book.py
│   │   └── ...
│   │
│   ├── models/             # SQLAlchemy ORM models
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── group.py
│   │   ├── book.py
│   │   ├── account.py
│   │   └── ...
│   │
│   ├── schemas/            # Pydantic schemas for request/response validation
│   │   ├── token.py
│   │   ├── user.py
│   │   ├── group.py
│   │   ├── book.py
│   │   ├── account.py
│   │   └── ...
│   │
│   ├── services/           # Business logic layer
│   │   ├── user_service.py
│   │   ├── book_service.py
│   │   ├── gcs_service.py  # GCS file operations
│   │   └── ...
│   │
│   ├── routers/            # API endpoint definitions (controllers)
│   │   ├── deps.py         # FastAPI dependencies (e.g., get_current_user)
│   │   ├── users.py
│   │   ├── groups.py
│   │   ├── books.py
│   │   ├── accounts.py
│   │   └── ...
│   │
│   └── security.py         # Password hashing and utility functions
│
└── tests/                  # Pytest tests
    ├── __init__.py
    ├── conftest.py         # Pytest fixtures (e.g., test client, db session)
    │
    ├── routers/
    │   ├── test_users.py
    │   └── ...
    │
    └── services/
        ├── test_user_service.py
        └── ...
```

### Key Components:

-   **`main.py`**: Initializes the FastAPI application and includes the API routers.
-   **`config.py`**: Defines and loads environment variables.
-   **`database.py`**: Sets up the SQLAlchemy engine and session factory.
-   **`models/`**: Contains the database table definitions as Python classes.
-   **`schemas/`**: Contains Pydantic models for data validation and serialization, ensuring API requests and responses conform to the defined structure.
-   **`crud/`**: Contains functions that interact directly with the database models to perform CRUD operations. This layer abstracts the database interaction from the business logic.
-   **`services/`**: The core business logic resides here. Services call CRUD functions and implement the application's rules and features. For example, a service would handle the logic for creating a book and its default accounts.
-   **`routers/`**: Defines the API paths, parameters, and responses. These modules handle the HTTP layer, calling service functions to perform actions and returning the results.
-   **`security.py`**: Handles security-related functions like password hashing and verification.
-   **`tests/`**: Contains all automated tests for the application, mirroring the application's structure.
-   **`alembic/`**: Manages database schema migrations, allowing for version-controlled changes to the database structure.

