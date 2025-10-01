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
