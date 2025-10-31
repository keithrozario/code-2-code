# Product Requirements Document: Moneynote API - Phase 1

## 1. Goal & Scope

This document outlines the requirements for Phase 1 of the Moneynote API rewrite. The goal of this phase is to establish the foundational, non-dependent API endpoints. These endpoints provide essential application metadata and configuration data, such as the application version, a test URL, a list of supported currencies, and available book templates. This phase lays the critical groundwork for all subsequent development by ensuring that basic configuration and metadata are accessible.

## 2. Functional Specifications

- **`GET /version`**: A client can retrieve the current version of the deployed application. This is used for diagnostics and compatibility checks.
- **`GET /test3`**: A client can retrieve the base URL of the application. This is a simple connectivity test to ensure the API is reachable.
- **`GET /currencies/all`**: A client can retrieve a list of all currencies supported by the application, including their names, codes, and latest exchange rates.
- **`GET /book-templates/all`**: A client can retrieve a list of all available "Book Templates." These templates are used to pre-populate new financial books with a standard set of categories, tags, and payees.

## 3. UI / UX Flow

This PRD is focused exclusively on the backend API. No UI/UX flow is defined as part of this phase. The endpoints specified herein are intended to be consumed by a frontend application, which will be responsible for the user interface and experience.

## 4. Technical Specifications

All endpoints require a valid JWT token in the `Authorization: Bearer <JWT_TOKEN>` header for authentication.

---

### 4.1 API Logic

#### **Endpoint: `GET /version`**

-   **Description:** Returns the application version.
-   **Business Logic:** The endpoint reads a static version number defined within the application's build configuration or properties. It provides a simple way for clients to identify the version of the backend they are communicating with.
-   **Request Parameters:** None.
-   **Responses & Scenarios:**
    -   **`200 OK`**: The request is successful.
        ```json
        {
          "data": "1.0.0"
        }
        ```
    -   **`401 Unauthorized`**: The request is missing a valid JWT token.
-   **Database CRUD Operations:** None.
-   **Database SQL Statements:** None.

---

#### **Endpoint: `GET /test3`**

-   **Description:** Returns the base URL of the application.
-   **Business Logic:** This endpoint returns a static string representing the application's base URL. It serves as a basic health and connectivity check.
-   **Request Parameters:** None.
-   **Responses & Scenarios:**
    -   **`200 OK`**: The request is successful.
        ```json
        {
          "data": "http://localhost:8080"
        }
        ```
    -   **`401 Unauthorized`**: The request is missing a valid JWT token.
-   **Database CRUD Operations:** None.
-   **Database SQL Statements:** None.

---

#### **Endpoint: `GET /currencies/all`**

-   **Description:** Gets all supported currencies.
-   **Business Logic:** The system loads a list of currencies and their base exchange rates from a local `currency.json` file at startup. These rates are periodically refreshed from an external API. This endpoint retrieves the current list of currencies and their latest rates from the application's in-memory cache.
-   **Request Parameters:** None.
-   **Responses & Scenarios:**
    -   **`200 OK`**: The request is successful, returning a list of currency objects.
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
    -   **`401 Unauthorized`**: The request is missing a valid JWT token.
-   **Database CRUD Operations:** None. This endpoint reads from an in-memory cache.
-   **Database SQL Statements:** None.

---

#### **Endpoint: `GET /book-templates/all`**

-   **Description:** Gets all available book templates.
-   **Business Logic:** The system loads a set of predefined book templates from a local `book_tpl.json` file at startup. These templates contain structures for categories, tags, and payees. This endpoint returns the list of available templates so a user can choose one when creating a new book.
-   **Request Parameters:** None.
-   **Responses & Scenarios:**
    -   **`200 OK`**: The request is successful, returning a list of book template objects.
        ```json
        [
          {
            "id": 1,
            "name": "Daily Life",
            "description": "Template for personal daily expense tracking."
          },
          {
            "id": 2,
            "name": "Small Business",
            "description": "Template for a small business with common income/expense categories."
          }
        ]
        ```
    -   **`401 Unauthorized`**: The request is missing a valid JWT token.
-   **Database CRUD Operations:** None. This endpoint reads from data loaded from the file system.
-   **Database SQL Statements:** None.

---

## 5. Data Model

Phase 1 does not interact with the main application database but relies on data loaded from local files.

-   **Currency:** Represents a supported currency and its exchange rate.
    -   `id` (Integer): Unique identifier.
    -   `name` (String): The ISO currency code (e.g., "USD").
    -   `description` (String): The full name of the currency.
    -   `rate` (Double): The exchange rate against the base currency (USD).

-   **Book Template:** Represents a predefined structure for a new book.
    -   `id` (Integer): Unique identifier for the template.
    -   `name` (String): The name of the template (e.g., "Daily Life").
    -   `description` (String): A brief description of the template's purpose.
    -   `categories` (List): A nested list of categories to be created.
    -   `tags` (List): A list of tags to be created.
    -   `payees` (List): A list of payees to be created.

## 6. Test Cases

| Test Case ID | Endpoint | Test Description | Preconditions | Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-P1-01** | `GET /version` | **Happy Path:** Retrieve version successfully. | User is authenticated. | Make a GET request to `/version`. | Status `200 OK`. Response body contains a valid version string. |
| **TC-P1-02** | `GET /version` | **Negative Path:** Unauthenticated access. | User is not authenticated. | Make a GET request to `/version`. | Status `401 Unauthorized`. |
| **TC-P1-03** | `GET /test3` | **Happy Path:** Retrieve base URL successfully. | User is authenticated. | Make a GET request to `/test3`. | Status `200 OK`. Response body contains a URL string. |
| **TC-P1-04** | `GET /currencies/all` | **Happy Path:** Retrieve all currencies. | User is authenticated. `currency.json` is present and valid. | Make a GET request to `/currencies/all`. | Status `200 OK`. Response body is a JSON array of currency objects. |
| **TC-P1-05** | `GET /currencies/all` | **Negative Path:** Unauthenticated access. | User is not authenticated. | Make a GET request to `/currencies/all`. | Status `401 Unauthorized`. |
| **TC-P1-06** | `GET /book-templates/all` | **Happy Path:** Retrieve all book templates. | User is authenticated. `book_tpl.json` is present and valid. | Make a GET request to `/book-templates/all`. | Status `200 OK`. Response body is a JSON array of book template objects. |
| **TC-P1-07** | `GET /book-templates/all` | **Negative Path:** Unauthenticated access. | User is not authenticated. | Make a GET request to `/book-templates/all`. | Status `401 Unauthorized`. |

## 7. Risks & Mitigations

-   **Risk 1:** The `currency.json` or `book_tpl.json` files are missing, corrupt, or malformed.
    -   **Mitigation:** Implement robust error handling during application startup. If a required file cannot be loaded, the application should log a fatal error and fail to start, preventing it from running in an unstable state.
-   **Risk 2:** The external currency exchange rate API is unavailable or changes its format.
    -   **Mitigation:** The system is designed to fall back to the last known rates (from the initial `currency.json` load or the last successful refresh). This behavior should be confirmed with tests. Additionally, implement logging to record when the external API fails, allowing for monitoring and alerting.

## 8. Open Questions

1.  What is the precise mechanism for injecting the application version into the `/version` endpoint? (Assumption: It will be handled via build tool properties, e.g., Maven/Gradle resource filtering).
2.  Should the list of currencies or book templates be refreshable without restarting the application, or is loading at startup sufficient for V1? (Assumption: Startup loading is sufficient for Phase 1).

## 9. Task Seeds (for Agent Decomposition)

-   **Task 1.1:** Implement the `GET /version` endpoint to return a static version string.
-   **Task 1.2:** Implement the `GET /test3` endpoint to return the application's base URL.
-   **Task 1.3:** Create a `CurrencyDataLoader` service to read `currency.json` into an in-memory cache at application startup.
-   **Task 1.4:** Implement the `GET /currencies/all` endpoint to serve the list of currencies from the in-memory cache.
-   **Task 1.5:** Create a `BookTemplateLoader` service to read `book_tpl.json` at application startup.
-   **Task 1.6:** Implement the `GET /book-templates/all` endpoint to serve the list of available book templates.
-   **Task 1.7:** Add authentication checks to all Phase 1 endpoints.
-   **Task 1.8:** Write unit and integration tests for all Phase 1 endpoints and data loading services to validate both happy paths and error conditions.
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
