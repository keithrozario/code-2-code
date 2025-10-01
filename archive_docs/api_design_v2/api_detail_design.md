# Detailed API Design: Moneynote Backend

This document outlines the detailed design for the Moneynote backend API, adhering to the specified architecture principles and API definitions.

## 1. Overall Architecture

The backend will be a monolithic API service built with Python and the FastAPI framework. It will follow a classic three-tier architecture, ensuring a clean separation of concerns. The application will be stateless, relying on an external database for data persistence and cloud storage for file persistence.

### Components

*   **API Layer (Web)**: Implemented using `FastAPI`. This layer is responsible for defining API endpoints (`/api/v1/...`), handling incoming HTTP requests, validating request data using Pydantic models, and serializing response data. It will extract user identity from the JWT `username` parameter, which is validated upstream by an API Gateway.
*   **Service Layer (Business Logic)**: This layer contains the core business logic of the application. It will be called by the API layer to perform operations. For example, when creating a new account, the service layer will handle the logic of associating it with the correct user and book, and ensuring all constraints are met. It will be agnostic of the web layer.
*   **Data Access Layer (DAL)**: Implemented using `SQLAlchemy` as the ORM. This layer is responsible for all interactions with the database, including creating, reading, updating, and deleting records. It will abstract the SQL queries and provide an object-oriented interface to the service layer.
*   **Database**: A single `SQLite3` database file will be used as the relational data store, as per the architectural principles. All application data (Users, Books, Accounts, etc.) will be stored here.
*   **File Storage**: For any file uploads, such as those associated with balance flows (`POST /balance-flows/{id}/addFile`), the service will interact directly with a **Google Cloud Storage (GCS)** bucket. The backend will not store files on its local disk.

### Request Flow

1.  A client sends an HTTPS request to the API endpoint, which hits the Google Cloud Load Balancer and then the API Gateway.
2.  The API Gateway validates the JWT. If valid, it forwards the request to the backend Cloud Run instance.
3.  The FastAPI application receives the request. A dependency injection system provides the user's identity (from the JWT) to the endpoint function.
4.  The endpoint function validates the request payload (body, query params) using Pydantic models.
5.  The endpoint function calls the appropriate method in the **Service Layer**, passing the validated data.
6.  The Service Layer executes the business logic, interacting with the **Data Access Layer** to query or modify data in the SQLite database.
7.  If file operations are needed, the Service Layer communicates with the **Google Cloud Storage** bucket.
8.  The result is returned up the chain, and FastAPI serializes the final response (e.g., a Pydantic model) into a JSON object and sends it back to the client.

## 2. Design Considerations

### Authentication & Authorization

*   Authentication is handled externally by an API Gateway. The backend will receive a `username` in the JWT payload.
*   A FastAPI `Depends` function will be created to extract the `username` from the `Authorization` header on every authenticated request.
*   All data will be partitioned by user. Every database query executed by the service layer must be filtered by the current user's ID to ensure data isolation and prevent users from accessing or modifying data that does not belong to them.

### Data Modeling (SQLAlchemy)

The database schema will be defined using SQLAlchemy ORM models. Based on the API dependencies, the key models and their relationships are:

*   `User`: Represents a user of the application.
*   `Book`: Belongs to a `User`. A user can have multiple books.
*   `Account`: Belongs to a `Book`. A book can have many accounts.
*   `Category`: Belongs to a `Book`.
*   `Payee`: Belongs to a `Book`.
*   `Tag`: Belongs to a `Book`.
*   `BalanceFlow`: The central transaction model. It will have foreign key relationships to `Book`, `Account` (source), `Account` (destination, optional), and `Payee`.
*   `CategoryRelation` & `TagRelation`: Many-to-many join tables to link `BalanceFlow` with `Category` and `Tag` respectively.
*   `FlowFile`: Represents a file stored in GCS, linked to a `BalanceFlow` via a foreign key.

### API Structure (FastAPI Routers)

To keep the API organized, FastAPI's `APIRouter` will be used. The endpoints defined in `api_definition.md` will be grouped into logical routers:

*   `accounts_router`: Will contain all endpoints under `/accounts`.
*   `balance_flows_router`: Will contain all endpoints under `/balance-flows`.
*   Other routers for `users`, `books`, `categories`, etc. will also be created.

These routers will be included in the main FastAPI app with the prefix `/api/v1`.

### Validation (Pydantic)

*   For every API endpoint that accepts a request body or query parameters, a corresponding Pydantic `BaseModel` will be defined.
*   These models will enforce data types, optionality, and basic constraints (e.g., string lengths) as defined in `api_definition.md`. This provides automatic request validation and documentation.
*   Separate Pydantic models will be used for creation (`AccountAddForm`), updates (`AccountUpdateForm`), and responses (`AccountDetails`) to ensure strict and clear API contracts.

### Error Handling

*   A global exception handler will be implemented using FastAPI's `@app.exception_handler`.
*   Custom exceptions (e.g., `EntityNotFoundException`, `PermissionDeniedException`) will be created and raised from the service layer.
*   The global handler will catch these exceptions and convert them into appropriate HTTP responses (e.g., 404 Not Found, 403 Forbidden) with a consistent JSON error message format.

## 3. Overall Structure of Files

The project will be organized into the following directory structure to maintain separation of concerns and facilitate testing.

```
/moneynote-api-python/
├── .gitignore
├── pyproject.toml          # Project metadata and dependencies for uv
├── README.md
│
├── src/
│   ├── main.py             # Main FastAPI application instance and startup logic
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── accounts.py     # Router for /accounts endpoints
│   │   └── balance_flows.py# Router for /balance-flows endpoints
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py       # Configuration management (e.g., GCS bucket name)
│   │   └── security.py     # JWT user extraction dependency
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   └── session.py      # SQLAlchemy engine, session management
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── account.py      # SQLAlchemy model for Account
│   │   └── balance_flow.py # SQLAlchemy model for BalanceFlow
│   │   └── ...             # Other models (user, book, etc.)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── account.py      # Pydantic schemas for Account API (Create, Update, Details)
│   │   └── balance_flow.py # Pydantic schemas for Balance Flow API
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── account_service.py # Business logic for accounts
│   │   └── balance_flow_service.py # Business logic for balance flows
│   │
│   └── crud/
│       ├── __init__.py
│       ├── base.py         # Base CRUD operations (Create, Read, Update, Delete)
│       ├── crud_account.py # Account-specific database operations
│       └── ...
│
└── tests/
    ├── __init__.py
    ├── test_accounts_api.py
    └── test_balance_flows_api.py
```
