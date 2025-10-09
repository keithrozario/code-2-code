# Product Requirements Document: Moneynote API - Phase 1

## 1. Goal & Scope

**Goal:** To establish the foundational, dependency-free endpoints for the Moneynote API.

**Scope:** This phase focuses on delivering a set of core, read-only APIs that provide essential metadata and configuration required by client applications. The scope is strictly limited to four endpoints that have no dependencies on other API functionalities, ensuring they can be developed and deployed independently as the first building block of the system.

---

## 2. Functional Specifications

*   **FS-001: Provide Application Version:** The API must expose an endpoint to return the current version of the backend application.
*   **FS-002: Provide Test URL:** The API must expose an endpoint for testing purposes that returns the application's base URL.
*   **FS-003: List Supported Currencies:** The API must provide a list of all supported currencies and their exchange rates, which are pre-loaded into the system.
*   **FS-004: List Book Templates:** The API must provide a list of all available book templates, which can be used to create new financial books with pre-defined settings.

---

## 3. UI / UX Flow

This PRD pertains exclusively to the backend API. There is no direct UI/UX flow associated with this phase. However, the endpoints are designed to be consumed by a client application in the following manner:

*   The `GET /currencies/all` endpoint would be used to populate a dropdown menu where users select a currency when creating a new account or book.
*   The `GET /book-templates/all` endpoint would be used to display a list of available templates (e.g., "Personal," "Business") that a user can choose from to quickly set up a new financial book.
*   The `GET /version` and `GET /test3` endpoints are primarily for diagnostics, testing, and client-side compatibility checks.

---

## 4. Technical Specifications

### 4.1 API Logic

Authentication: All endpoints in this phase require a valid JWT `Authorization: Bearer <token>` header.

#### **Endpoint 1: `GET /version`**

*   **Description:** Returns the current version of the application.
*   **Business Logic:** This endpoint provides a simple mechanism for clients to check the version of the API they are communicating with. The version is typically a static value defined in the application's build configuration.
*   **Request Parameters:**
    *   **Headers:**
        | Name | Description | Data type | Optionality |
        |---|---|---|---|
        | `Authorization` | Bearer token | String | Mandatory |
*   **Responses & Scenarios:**
    *   **200 OK:** The request is successful.
        ```json
        {
          "data": "1.0.0"
        }
        ```
    *   **401 Unauthorized:** The request lacks a valid authentication token.
*   **Database CRUD Operations:** None.
*   **Database SQL Statements:** None.

#### **Endpoint 2: `GET /test3`**

*   **Description:** Returns the base URL of the application.
*   **Business Logic:** This endpoint is used for connectivity testing and diagnostics, allowing clients to confirm the base URL of the API.
*   **Request Parameters:**
    *   **Headers:**
        | Name | Description | Data type | Optionality |
        |---|---|---|---|
        | `Authorization` | Bearer token | String | Mandatory |
*   **Responses & Scenarios:**
    *   **200 OK:** The request is successful.
        ```json
        {
          "data": "http://localhost:8080"
        }
        ```
    *   **401 Unauthorized:** The request lacks a valid authentication token.
*   **Database CRUD Operations:** None.
*   **Database SQL Statements:** None.

#### **Endpoint 3: `GET /currencies/all`**

*   **Description:** Gets all supported currencies.
*   **Business Logic:** The system loads a list of currencies from a local `currency.json` file into an in-memory cache upon startup. This endpoint retrieves and returns the cached list. This provides clients with all necessary currency information without requiring a database query.
*   **Request Parameters:**
    *   **Headers:**
        | Name | Description | Data type | Optionality |
        |---|---|---|---|
        | `Authorization` | Bearer token | String | Mandatory |
*   **Responses & Scenarios:**
    *   **200 OK:** The request is successful. The response is a list of currency objects.
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
    *   **401 Unauthorized:** The request lacks a valid authentication token.
*   **Database CRUD Operations:** None. This is a read operation from an in-memory data structure.
*   **Database SQL Statements:** None.

#### **Endpoint 4: `GET /book-templates/all`**

*   **Description:** Gets all available book templates.
*   **Business Logic:** Similar to currencies, the system loads book templates from a local `book_tpl.json` file into memory on startup. This endpoint returns the list of cached templates, which contain predefined categories, tags, and payees for different types of financial books (e.g., personal, business).
*   **Request Parameters:**
    *   **Headers:**
        | Name | Description | Data type | Optionality |
        |---|---|---|---|
        | `Authorization` | Bearer token | String | Mandatory |
*   **Responses & Scenarios:**
    *   **200 OK:** The request is successful. The response is a list of book template objects.
        ```json
        [
          {
            "id": 1,
            "name": "Daily Life",
            "description": "Template for personal daily expenses"
          },
          {
            "id": 2,
            "name": "Restaurant",
            "description": "Template for a small restaurant business"
          }
        ]
        ```
    *   **401 Unauthorized:** The request lacks a valid authentication token.
*   **Database CRUD Operations:** None. This is a read operation from an in-memory data structure.
*   **Database SQL Statements:** None.

---

## 5. Data Model

No database tables are directly created or modified in this phase. The data models are transient, in-memory representations loaded from local JSON files.

*   **Currency Model (In-Memory)**
    | Attribute | Data Type | Description |
    |---|---|---|
    | `id` | Integer | Unique identifier. |
    | `name` | String | The 3-letter currency code (e.g., "USD"). |
    | `description` | String | Human-readable name (e.g., "United States Dollar"). |
    | `rate` | Double | The exchange rate against the base currency (USD). |

*   **Book Template Model (In-Memory)**
    | Attribute | Data Type | Description |
    |---|---|---|
    | `id` | Integer | Unique identifier. |
    | `name` | String | The name of the template (e.g., "Daily Life"). |
    | `description` | String | A brief description of the template's purpose. |
    | `categories`| Array | List of predefined categories. |
    | `tags` | Array | List of predefined tags. |
    | `payees` | Array | List of predefined payees. |

---

## 6. Test Cases

| Test Case ID | Endpoint | Feature | Test Steps | Expected Result |
|---|---|---|---|---|
| TC-P1-01 | `GET /version` | Happy Path | Send an authenticated GET request to `/version`. | HTTP 200 OK. Response body contains a `data` field with a version string. |
| TC-P1-02 | `GET /version` | Unauthorized | Send a GET request to `/version` without an Authorization header. | HTTP 401 Unauthorized. |
| TC-P1-03 | `GET /test3` | Happy Path | Send an authenticated GET request to `/test3`. | HTTP 200 OK. Response body contains a `data` field with a URL string. |
| TC-P1-04 | `GET /currencies/all` | Happy Path | Send an authenticated GET request to `/currencies/all`. | HTTP 200 OK. Response body is a non-empty array of currency objects. |
| TC-P1-05 | `GET /currencies/all` | Data Verification | Check the response from TC-P1-04. | The array contains entries for "USD", "EUR", and "CNY". |
| TC-P1-06 | `GET /book-templates/all` | Happy Path | Send an authenticated GET request to `/book-templates/all`. | HTTP 200 OK. Response body is a non-empty array of book template objects. |
| TC-P1-07 | `GET /book-templates/all` | Unauthorized | Send a GET request to `/book-templates/all` without an Authorization header. | HTTP 401 Unauthorized. |

---

## 7. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Configuration files (`currency.json`, `book_tpl.json`) are missing or malformed. | Low | High | The application should fail to start with a clear, descriptive error message pointing to the problematic file. Implement schema validation for the JSON files as part of the build process. |
| In-memory caching strategy is not suitable for a horizontally scaled, distributed environment. | Medium | Medium | This is acceptable for initial phases. For future scalability, plan to migrate the cache to a distributed solution like Redis or rely on a database source-of-truth. |
| Hardcoded version and URL information becomes stale. | High | Low | The version and URL should be loaded from a central configuration file or environment variables rather than being hardcoded in the controller logic. |

---

## 8. Open Questions

1.  Should the application version be read dynamically from a build file (e.g., `pyproject.toml`, `build.gradle`) to ensure it is always synchronized with the release, or is a static value sufficient?
2.  Is the current in-memory caching strategy for currencies and templates acceptable for the projected v1 user load, or should a move to a distributed cache be prioritized in an earlier phase?

---

## 9. Task Seeds (for Agent Decomposition)

*   **Task 1.1:** Implement the `GET /version` endpoint in the `TestController` to return a static version string.
*   **Task 1.2:** Implement the `GET /test3` endpoint in the `TestController` to return the application's base URL from a configuration property.
*   **Task 1.3:** Create a `CurrencyDataLoader` service to read `currency.json` and populate an in-memory list of `CurrencyDetails` objects at application startup.
*   **Task 1.4:** Implement the `GET /currencies/all` endpoint in the `CurrencyController` to return the list of currencies from the in-memory cache.
*   **Task 1.5:** Create a `BookTemplateDataLoader` service to read `book_tpl.json` and populate an in-memory list of book templates at application startup.
*   **Task 1.6:** Implement the `GET /book-templates/all` endpoint in the `BookTemplateController` to return the list of templates from the in-memory cache.
*   **Task 1.7:** Write unit tests for all services and controllers created in this phase, mocking dependencies where necessary.
*   **Task 1.8:** Write integration tests to verify that all four endpoints require authentication and return the expected data structures and status codes.
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
