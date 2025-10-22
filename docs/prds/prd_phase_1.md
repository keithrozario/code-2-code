# PRD - Moneynote API: Phase 1

## 1. Goal & Scope

**Goal:** To establish the foundational, non-dependent API endpoints for the Moneynote application.

**Scope:** This PRD covers Phase 1 of the Moneynote API development. The scope is strictly limited to providing essential, read-only system and configuration data required by a client application for its initial setup. This includes fetching the application version, a test URL, the list of supported currencies, and available book templates. These endpoints form the bedrock upon which user-facing features will be built in subsequent phases.

## 2. Functional Specifications

The API will provide the following functionalities:
- **FS-001:** Ability to retrieve the current version of the backend application.
- **FS-002:** Ability to retrieve a base URL, intended for testing and configuration.
- **FS-003:** Ability to retrieve a complete list of all currencies supported by the application.
- **FS-004:** Ability to retrieve a complete list of all predefined book templates available for creating new books.

## 3. UI / UX Flow

As this is a backend API, there is no direct UI. However, the intended flow for a client application is as follows:
1.  The client application authenticates the user and obtains a JWT token.
2.  Upon successful login, or during initial application loading, the client calls the Phase 1 endpoints to gather necessary configuration data.
3.  The response from `GET /currencies/all` would be used to populate currency selection dropdowns throughout the application (e.g., when creating a new account).
4.  The response from `GET /book-templates/all` would be used to populate a "Create Book from Template" wizard or selection screen.
5.  The `GET /version` endpoint may be used for diagnostic purposes or to display in an "About" section.

## 4. Technical Specifications

All endpoints in Phase 1 require authentication. A valid JWT must be provided in the `Authorization: Bearer <token>` header.

---

### 4.1 API Logic: `GET /version`

*   **Description:** Returns the current version of the application. This is useful for client-side compatibility checks and diagnostics.
*   **Business Logic:** The endpoint retrieves the application version string from the application's configuration. It does not involve any dynamic calculation.
*   **Request Parameters:** None.
*   **Possible Responses:**
    *   **200 OK:** The request was successful.
        ```json
        {
          "version": "1.0.0"
        }
        ```
    *   **401 Unauthorized:** The request was made without a valid JWT token.
*   **Database CRUD:** None.
*   **Database SQL Statements:** None.

---

### 4.2 API Logic: `GET /test3`

*   **Description:** Returns the base URL of the application. This is intended for testing and client configuration.
*   **Business Logic:** The endpoint retrieves the base URL string from the application's configuration.
*   **Request Parameters:** None.
*   **Possible Responses:**
    *   **200 OK:** The request was successful.
        ```json
        {
          "base_url": "http://localhost:8000"
        }
        ```
    *   **401 Unauthorized:** The request was made without a valid JWT token.
*   **Database CRUD:** None.
*   **Database SQL Statements:** None.

---

### 4.3 API Logic: `GET /currencies/all`

*   **Description:** Retrieves a list of all currencies supported by the application.
*   **Business Logic:** Upon application startup, a data loader reads the `currency.json` file and caches the list of currencies in memory. This endpoint returns the cached list. This ensures fast response times without requiring a database query.
*   **Request Parameters:** None.
*   **Possible Responses:**
    *   **200 OK:** The request was successful. The body will contain a list of currency objects.
        ```json
        [
          {
            "id": "USD",
            "name": "United States Dollar",
            "description": "The official currency of the United States and its territories.",
            "rate": 1.0
          },
          {
            "id": "EUR",
            "name": "Euro",
            "description": "The official currency of 19 of the 27 member states of the European Union.",
            "rate": 0.92
          }
        ]
        ```
    *   **401 Unauthorized:** The request was made without a valid JWT token.
*   **Database CRUD:** None.
*   **Database SQL Statements:** None.

---

### 4.4 API Logic: `GET /book-templates/all`

*   **Description:** Retrieves a list of all available book templates.
*   **Business Logic:** Similar to currencies, a data loader reads the `book_tpl.json` file at startup and caches the list of templates in memory. This endpoint returns the cached list.
*   **Request Parameters:** None.
*   **Possible Responses:**
    *   **200 OK:** The request was successful. The body will contain a list of book template objects.
        ```json
        [
          {
            "id": "personal_v1",
            "name": "Personal Finance",
            "description": "A template for managing personal finances, including daily expenses, income, and savings.",
            "categories": [],
            "tags": [],
            "payees": []
          },
          {
            "id": "business_v1",
            "name": "Small Business",
            "description": "A template for small business accounting, including revenue, expenses, and payroll.",
            "categories": [],
            "tags": [],
            "payees": []
          }
        ]
        ```
    *   **401 Unauthorized:** The request was made without a valid JWT token.
*   **Database CRUD:** None.
*   **Database SQL Statements:** None.

## 5. Data Model

The data for Phase 1 is not sourced from the database but from static JSON files loaded into memory.

**Currency Model (`currency.json`)**
| Attribute | Data Type | Description | Example |
|---|---|---|---|
| `id` | String | The ISO currency code. | "USD" |
| `name` | String | The full name of the currency. | "United States Dollar" |
| `description` | String | A brief description of the currency. | "The official currency..." |
| `rate` | Float | The initial exchange rate against a base currency (USD). | 1.0 |

**Book Template Model (`book_tpl.json`)**
| Attribute | Data Type | Description | Example |
|---|---|---|---|
| `id` | String | A unique identifier for the template. | "personal_v1" |
| `name` | String | The display name of the template. | "Personal Finance" |
| `description` | String | A brief description of the template's purpose. | "A template for managing..." |
| `categories`| Array | A list of categories to be created with the book. | `[]` |
| `tags` | Array | A list of tags to be created with the book. | `[]` |
| `payees` | Array | A list of payees to be created with the book. | `[]` |

## 6. Test Cases

| Test Case ID | Endpoint | Feature | Test Steps | Expected Result |
|---|---|---|---|---|
| **TC-P1-01** | `GET /version` | Happy Path | 1. Authenticate and get JWT. <br> 2. Make GET request to `/version`. | **Status:** 200 OK. <br> **Body:** `{"version": "x.y.z"}` where version is a non-empty string. |
| **TC-P1-02** | `GET /version` | Unauthorized | 1. Make GET request to `/version` without `Authorization` header. | **Status:** 401 Unauthorized. |
| **TC-P1-03** | `GET /currencies/all` | Happy Path | 1. Authenticate and get JWT. <br> 2. Make GET request to `/currencies/all`. | **Status:** 200 OK. <br> **Body:** A JSON array matching the contents of `currency.json`. |
| **TC-P1-04** | `GET /book-templates/all` | Happy Path | 1. Authenticate and get JWT. <br> 2. Make GET request to `/book-templates/all`. | **Status:** 200 OK. <br> **Body:** A JSON array matching the contents of `book_tpl.json`. |

## 7. Risks & Mitigations

*   **Risk 1: Dependency on Static Files:** The endpoints depend entirely on `currency.json` and `book_tpl.json` being present and correctly formatted at startup.
    *   **Mitigation:** Implement startup validation checks in the `data_loader` service to ensure files exist and are parseable. Log a critical error and fail to start if they are missing or corrupt. Ensure these files are included in the deployment package.
*   **Risk 2: Stale Data:** The currency data is loaded once at startup and is not refreshed. While the initial rates are not critical for Phase 1, this will become a problem later.
    *   **Mitigation:** This is an accepted limitation for Phase 1. The plan includes a future phase (`Phase 18: POST /currencies/refresh`) specifically to address refreshing currency rates from an external API.

## 8. Open Questions

1.  Are the `GET /version` and `GET /test3` endpoints intended for long-term use, or are they for initial development and testing only? Should they be removed in a production build or protected under a specific debug/admin flag?
2.  Should the structure of the `book_tpl.json` be validated against a schema on startup to prevent runtime errors if the file is manually edited incorrectly?

## 9. Task Seeds (for Agent Decomposition)

- `task: Implement router and service logic for GET /version to read from application settings.`
- `task: Implement router and service logic for GET /test3 to read from application settings.`
- `task: Implement data loader service to read and cache currency.json on startup.`
- `task: Implement GET /currencies/all endpoint to return cached currency data.`
- `task: Implement data loader service to read and cache book_tpl.json on startup.`
- `task: Implement GET /book-templates/all endpoint to return cached book template data.`
- `task: Create Pydantic/Schema models for Currency and BookTemplate to ensure type safety.`
- `task: Write unit tests for the data loader services to handle file-not-found and JSON parsing errors.`
- `task: Write integration tests for all four Phase 1 endpoints, verifying authentication and response correctness.`
# Moneynote API - Detailed Design Document

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
