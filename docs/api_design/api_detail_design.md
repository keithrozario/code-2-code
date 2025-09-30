# API Detailed Design Document

This document outlines the detailed design for the MoneyNote backend API, synthesizing the API definition, dependencies, and architectural principles.

## 1. Overall Architecture

The application will be built using a 3-tier architecture as defined in the architecture principles.

*   **Backend**: An API-driven backend built with Python and the **FastAPI** framework. It will handle all business logic, validation, and data processing.
*   **Database**: A single **SQLite3** relational database will serve as the datastore. The backend will interact with it using the **SQLAlchemy** ORM. As per the principles, the database will not contain any logic (e.g., triggers, stored procedures).
*   **Frontend**: A web-based frontend built with native JavaScript, which will consume the backend API.

### Deployment & Infrastructure

*   The backend API will be packaged as a container and deployed as a **Google Cloud Run** application.
*   A **Google Cloud Load Balancer** will be placed in front of the Cloud Run service to manage traffic.
*   Due to the use of a single file-based SQLite3 database, the backend application is **limited to a single running instance**.
*   File and object storage (e.g., for transaction attachments) will be handled by a **Google Cloud Storage (GCS)** bucket. The application will store references to these objects, not the files themselves.

### Authentication

*   Authentication will be managed via **JSON Web Tokens (JWTs)**.
*   The backend will operate under the assumption that an upstream gateway has already validated the JWT.
*   The backend is responsible for decoding the JWT and extracting the user's identity from the `username` parameter within the token payload to authorize requests.

## 2. Design Considerations

### API Versioning

*   All API endpoints will be prefixed with `/api/v1` to ensure clear versioning from the start.

### Data Model & Relationships

The API revolves around several core entities with clear dependencies:

*   **User**: The central entity. All data is owned by a user.
*   **Group**: A collaborative space for users. A user can be in multiple groups.
*   **Book**: A financial ledger that belongs to a user (or a group). It acts as a container for accounts, categories, payees, tags, and transactions.
*   **Account**: Represents a real-world financial account (e.g., bank account, credit card) and belongs to a book.
*   **Category, Payee, Tag**: Hierarchical or flat lists used to classify transactions within a book.
*   **Balance Flow**: The core transaction entity (expense, income, transfer). It belongs to a book, involves one or two accounts, and can be linked to categories, payees, and tags.
*   **Note Day**: A user-specific reminder or recurring event.

These entities will be mapped to relational tables in the SQLite database using the SQLAlchemy ORM.

### Authentication & Authorization

*   A dependency injector in FastAPI will be created to handle JWT decoding and extract the `username`. This will provide a `current_user` object to the endpoint functions.
*   Authorization will be enforced at the service/CRUD layer. Before any operation, the service will verify that the `current_user` has the necessary permissions to access or modify the requested resource. For example, when fetching a book, the service will check that the book belongs to the user.

### File Handling

*   Endpoints that accept files, like `POST /balance-flows/{id}/addFile`, will expect `multipart/form-data` requests.
*   A dedicated `FileService` will handle the logic of uploading the file content to a GCS bucket and returning the unique object identifier.
*   The database will store this GCS object identifier in the corresponding table (e.g., `FlowFile`).
*   When a file is requested, the service will generate a signed URL for the GCS object to grant the user temporary access.

### Error Handling

*   The API will use standard HTTP status codes to indicate the outcome of a request.
    *   `2xx`: Success
    *   `400 Bad Request`: For validation errors (e.g., missing fields, invalid data types).
    *   `401 Unauthorized`: If the JWT is missing or invalid (though validation is primarily the gateway's role).
    *   `403 Forbidden`: If the user is authenticated but not authorized to perform the action.
    *   `404 Not Found`: If a requested resource does not exist.
    *   `500 Internal Server Error`: For unexpected server-side errors.
*   Error responses will contain a JSON body with a `detail` key explaining the error.

## 3. Overall Structure of Files

To maintain a clean and scalable codebase, the project will follow a modular structure that separates concerns.

```
moneynote-py-api/
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
├── main.py                 # FastAPI app entry point, includes main router
├── core/
│   ├── __init__.py
│   ├── config.py           # Manages settings and environment variables (e.g., DB path, GCS bucket)
│   └── security.py         # Handles JWT decoding and password hashing
├── db/
│   ├── __init__.py
│   ├── database.py         # SQLAlchemy engine, session management
│   └── base.py             # Declarative base for all ORM models
├── models/                 # SQLAlchemy ORM model classes
│   ├── __init__.py
│   ├── user.py
│   ├── group.py
│   ├── book.py
│   ├── account.py
│   ├── category.py
│   ├── payee.py
│   ├── tag.py
│   ├── balance_flow.py
│   └── note_day.py
├── schemas/                # Pydantic schemas for request/response validation and serialization
│   ├── __init__.py
│   ├── user.py
│   ├── group.py
│   ├── book.py
│   ├── account.py
│   ├── category.py
│   ├── payee.py
│   ├── tag.py
│   ├── balance_flow.py
│   └── token.py            # Schema for JWT token
├── crud/                   # CRUD (Create, Read, Update, Delete) database interaction logic
│   ├── __init__.py
│   ├── base.py             # Base CRUD class with common methods
│   ├── crud_user.py
│   ├── crud_book.py
│   ├── crud_account.py
│   └── ...                 # CRUD files for other models
├── api/
│   ├── __init__.py
│   ├── deps.py             # FastAPI dependencies (e.g., get_current_user, get_db_session)
│   └── v1/
│       ├── __init__.py
│       ├── api.py          # Main API router that includes all resource-specific routers
│       └── endpoints/
│           ├── __init__.py
│           ├── login.py
│           ├── accounts.py
│           ├── books.py
│           ├── balance_flows.py
│           ├── reports.py
│           └── ...         # Endpoint files for other resources
├── services/               # Business logic layer, orchestrating CRUD operations and external services
│   ├── __init__.py
│   ├── gcs_service.py      # Service for interacting with Google Cloud Storage
│   └── report_service.py   # Service for generating complex reports
└── tests/                  # Pytest tests
    ├── __init__.py
    ├── conftest.py         # Test fixtures and setup
    └── api/
        └── v1/
            ├── __init__.py
            └── test_accounts.py # Tests for the accounts API
```
