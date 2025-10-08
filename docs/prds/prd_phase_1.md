# Product Requirements Document: Moneynote API - Phase 1

## 1. Goal & Scope

**Goal:** To establish the foundational, non-dependent API endpoints required for the Moneynote application's basic operation and configuration.

**Scope:** This PRD covers the implementation of four fundamental, read-only API endpoints as defined in Phase 1 of the API Development Plan. These endpoints provide essential metadata to client applications, such as application version, available currencies, and book templates, without any dependencies on other business logic or user data.

---

## 2. Functional Specifications

The following functionalities will be delivered in Phase 1:

*   **FS-001: Retrieve Application Version:** The API shall provide an endpoint to retrieve the current running version of the backend application.
*   **FS-002: Retrieve Base URL:** The API shall provide a test endpoint that returns the base URL of the application, which can be used by clients for configuration.
*   **FS-003: List All Currencies:** The API shall provide an endpoint that returns a complete list of all supported currencies and their exchange rates, which are pre-loaded into the system.
*   **FS-004: List All Book Templates:** The API shall provide an endpoint that returns a list of all available book templates, which users can use to create new financial books with predefined settings.

---

## 3. UI / UX Flow

As this document pertains to the backend API, there is no direct UI/UX flow. However, these endpoints are critical for the frontend to initialize itself:

1.  A client application starts.
2.  It might call `GET /version` to check for compatibility.
3.  It calls `GET /currencies/all` to populate currency selection dropdowns throughout the application (e.g., when creating a new account or book).
4.  It calls `GET /book-templates/all` to display the list of available templates when a user decides to create a new book.
5.  The `GET /test3` endpoint can be used in development or CI/CD environments to verify connectivity and retrieve the application's base URL.

---

## 4. Technical Specifications

### 4.1 API Logic

#### **Endpoint 1: `GET /version`**

*   **Description:** Returns the application's current version. This is useful for client-side compatibility checks and debugging.
*   **Business Logic:** The endpoint retrieves a static version string defined within the application's build configuration or properties.
*   **Request:**
    *   **Method:** `GET`
    *   **Path:** `/version`
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)
*   **Responses:**
    *   **200 OK:** Successful request.
        ```json
        {
          "data": "1.0.0"
        }
        ```
    *   **401 Unauthorized:** The JWT token is missing or invalid.
*   **Database CRUD:** None. This is a read-only operation from application metadata.
*   **SQL Statements:** N/A.

---

#### **Endpoint 2: `GET /test3`**

*   **Description:** A simple test endpoint that returns the base URL of the application.
*   **Business Logic:** The endpoint constructs and returns the base URL from the incoming request's context.
*   **Request:**
    *   **Method:** `GET`
    *   **Path:** `/test3`
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)
*   **Responses:**
    *   **200 OK:** Successful request.
        ```json
        {
          "data": "http://localhost:8080"
        }
        ```
    *   **401 Unauthorized:** The JWT token is missing or invalid.
*   **Database CRUD:** None.
*   **SQL Statements:** N/A.

---

#### **Endpoint 3: `GET /currencies/all`**

*   **Description:** Retrieves a list of all currencies supported by the application.
*   **Business Logic:** On application startup, the system loads currency data from a local `currency.json` file into an in-memory cache. This endpoint reads from that cache. The data is not fetched from the database.
*   **Request:**
    *   **Method:** `GET`
    *   **Path:** `/currencies/all`
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)
*   **Responses:**
    *   **200 OK:** Successful request. The response is a JSON array of currency objects.
        ```json
        [
          {
            "id": 1,
            "name": "USD",
            "description": "United States Dollar",
            "rate": 1.0,
            "rate2": null
          },
          {
            "id": 2,
            "name": "EUR",
            "description": "Euro",
            "rate": 0.92,
            "rate2": null
          }
        ]
        ```
    *   **401 Unauthorized:** The JWT token is missing or invalid.
*   **Database CRUD:** None. The data is read from the filesystem (`src/main/resources/currency.json`) on startup.
*   **SQL Statements:** N/A.

---

#### **Endpoint 4: `GET /book-templates/all`**

*   **Description:** Retrieves a list of all available book templates.
*   **Business Logic:** On application startup, the system loads book template data from a local `book_tpl.json` file. This endpoint serves the loaded data. This allows users to create new books with a predefined set of categories, tags, and payees.
*   **Request:**
    *   **Method:** `GET`
    *   **Path:** `/book-templates/all`
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)
*   **Responses:**
    *   **200 OK:** Successful request. The response is a JSON array of book template objects.
        ```json
        [
          {
            "id": 1,
            "name": "Daily Life"
          },
          {
            "id": 2,
            "name": "Restaurant"
          }
        ]
        ```
    *   **401 Unauthorized:** The JWT token is missing or invalid.
*   **Database CRUD:** None. The data is read from the filesystem (`src/main/resources/book_tpl.json`) on startup.
*   **SQL Statements:** N/A.

---

## 5. Data Model

This phase does not introduce any new database tables. It relies on data loaded from local JSON files into in-memory objects.

*   **Currency Model (`CurrencyDetails`)**:
    *   `id` (Integer): Unique identifier.
    *   `name` (String): 3-letter currency code (e.g., "USD").
    *   `description` (String): Full currency name.
    *   `rate` (Double): Exchange rate against the base currency (USD).

*   **Book Template Model (`IdAndNameDetails`)**:
    *   `id` (Integer): Unique identifier for the template.
    *   `name` (String): The display name of the template (e.g., "Daily Life").

---

## 6. Test Cases

| Test Case ID | Endpoint | Feature | Test Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-P1-01** | `GET /version` | Happy Path | Make a GET request with a valid auth token. | HTTP 200 OK. Response body contains a `data` field with a version string. |
| **TC-P1-02** | `GET /version` | Unauthorized | Make a GET request without an auth token. | HTTP 401 Unauthorized. |
| **TC-P1-03** | `GET /test3` | Happy Path | Make a GET request with a valid auth token. | HTTP 200 OK. Response body contains a `data` field with the application's base URL. |
| **TC-P1-04** | `GET /currencies/all` | Happy Path | Make a GET request with a valid auth token. | HTTP 200 OK. Response body is a JSON array of currency objects, matching the content of `currency.json`. |
| **TC-P1-05** | `GET /currencies/all` | Unauthorized | Make a GET request without an auth token. | HTTP 401 Unauthorized. |
| **TC-P1-06** | `GET /book-templates/all` | Happy Path | Make a GET request with a valid auth token. | HTTP 200 OK. Response body is a JSON array of book template objects, matching the content of `book_tpl.json`. |
| **TC-P1-07** | `GET /book-templates/all` | Unauthorized | Make a GET request without an auth token. | HTTP 401 Unauthorized. |

---

## 7. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| `currency.json` or `book_tpl.json` is missing or malformed. | Low | High | The application will fail to start. Implement robust error handling on startup to log a clear error message. Add file validation to the CI/CD pipeline. |
| The version number is not updated during the build process. | Medium | Low | The `GET /version` endpoint will return an outdated version. Automate version bumping as part of the release process. |

---

## 8. Open Questions

1.  Should the version number be sourced from a Maven/Gradle property, a git tag, or a static file? (Assuming build tool property is best practice).
2.  Is there a future requirement to make currencies or book templates manageable via an admin API instead of static JSON files? (For now, no, but good to keep in mind for future architecture).

---

## 9. Task Seeds (for Agent Decomposition)

1.  **Task 1.1:** Implement `GET /version` endpoint in `TestController`.
    *   Define a version property in the build configuration (`build.gradle`/`pom.xml`).
    *   Read the property in the controller and return it in the specified JSON format.
2.  **Task 1.2:** Implement `GET /test3` endpoint in `TestController`.
    *   Inject the `HttpServletRequest` to dynamically determine the base URL.
    *   Return the URL in the specified JSON format.
3.  **Task 1.3:** Implement `CurrencyDataLoader` to load `currency.json`.
    *   Create a service/bean to hold the currency list in memory (`ApplicationScopeBean`).
    *   On application startup (`@PostConstruct`), read `src/main/resources/currency.json`, parse it, and populate the in-memory list.
4.  **Task 1.4:** Implement `GET /currencies/all` endpoint in `CurrencyController`.
    *   Create the controller and endpoint.
    *   Inject the currency data service and return the list of all currencies.
5.  **Task 1.5:** Implement data loader for `book_tpl.json`.
    *   Similar to currencies, create a service to hold the book templates in memory.
    *   On startup, read `src/main/resources/book_tpl.json`, parse it, and populate the list.
6.  **Task 1.6:** Implement `GET /book-templates/all` endpoint in `BookTemplateController`.
    *   Create the controller and endpoint.
    *   Return the list of all loaded book templates.
7.  **Task 1.7:** Add unit and integration tests for all four endpoints.
    *   Verify correct responses for happy paths.
    *   Verify `401 Unauthorized` responses when the auth token is missing.
    *   Mock file loading to test data parsing logic.


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

