# MoneyNote API Detailed Design

## 1. Introduction

This document provides a detailed design for the new MoneyNote backend API. The design is based on the API definition, dependencies, and plan, and it strictly adheres to the established architecture principles.

The backend will be a Python application built with the FastAPI framework, using SQLAlchemy as the ORM for a SQLite database.

## 2. Overall Architecture

The API will be implemented as a single, stateless web application deployed as a Google Cloud Run service. Due to the use of a single SQLite database file, the service will be limited to a single running instance.

The architecture follows a classic three-layered pattern:

1.  **API/Controller Layer**: This layer is responsible for handling HTTP requests. It defines the API endpoints (e.g., `/api/v1/users`, `/api/v1/accounts`), validates incoming data using Pydantic models, and handles authentication. It will extract user identity from the JWT token provided in the `Authorization` header, as per the architecture principles. This layer will then call the appropriate service layer function.

2.  **Service/Business Logic Layer**: This layer contains the core application logic. It orchestrates the application's functionality, processing data and making decisions based on the business rules. It is called by the API layer and, in turn, calls the Data Access Layer to interact with the database. It will be responsible for all logic and validation, assuming no validation has occurred on the frontend.

3.  **Data Access/Repository Layer**: This layer is responsible for all communication with the database. It uses SQLAlchemy as the ORM to perform CRUD (Create, Read, Update, Delete) operations on the SQLite database. This layer abstracts the database from the rest of the application.

### External Services

-   **Database**: A single SQLite3 database file will be used for all data storage. The architecture principles forbid the use of triggers or stored procedures.
-   **File Storage**: For any file-related operations (e.g., `FlowFile` attachments), the backend will interact with a Google Cloud Storage (GCS) bucket. The backend itself will remain stateless and will not write files to the local disk.

### Authentication

Authentication will be handled at the API Gateway level, which validates the JWT. The backend will receive the request with a validated token and will only be responsible for decoding it to extract the `username` to identify the user and scope the data accordingly.

## 3. Design Considerations

The design of the API is guided by the following principles:

-   **Statelessness**: The application will not hold any state in memory between requests. All persistent data will be stored in the SQLite database, and file uploads will be handled via Google Cloud Storage.
-   **API Versioning**: All API endpoints will be prefixed with `/api/v1` as specified in the architecture principles.
-   **Data Validation**: All incoming data will be rigorously validated by the backend. FastAPI's integration with Pydantic will be used to define schemas for request bodies and query parameters, ensuring that all data conforms to the required format before being processed by the service layer.
-   **ORM**: SQLAlchemy will be used as the ORM to map Python objects to database tables, providing a consistent and secure way to interact with the SQLite database. Database migrations will be managed using `alembic`.
-   **Dependency Management**: `uv` will be used for managing Python package dependencies, as specified in `pyproject.toml`.
-   **Testing and Linting**: The codebase will be tested using `pytest`. Code formatting will be enforced using `black` to ensure a consistent style.
-   **Configuration**: Application configuration (e.g., database path, GCS bucket name) will be managed in a centralized location and loaded at startup.

## 4. Overall Structure of Files

To ensure a clean, maintainable, and scalable codebase, the project will be organized by feature/domain. A new directory, `moneynote-api-python`, will be created for the FastAPI project.

```
/moneynote-api-python/
├── alembic/                  # Alembic migrations for the database
│   ├── versions/
│   └── env.py
├── src/
│   ├── main.py               # FastAPI application entry point and router setup
│   ├── core/                 # Core application components
│   │   ├── config.py         # Application configuration settings
│   │   ├── database.py       # Database session and connection management
│   │   └── security.py       # JWT decoding and user identity handling
│   │
│   ├── domains/              # Business logic, separated by domain/feature
│   │   ├── user/
│   │   │   ├── user_controller.py    # FastAPI routers for User API
│   │   │   ├── user_service.py       # Business logic for users
│   │   │   ├── user_repository.py    # Database operations for users
│   │   │   └── user_schemas.py       # Pydantic models for user requests/responses
│   │   │
│   │   ├── account/
│   │   │   ├── account_controller.py
│   │   │   ├── account_service.py
│   │   │   ├── account_repository.py
│   │   │   └── account_schemas.py
│   │   │
│   │   ├── book/
│   │   │   # ... similar structure for Book domain
│   │   │
│   │   ├── balance_flow/
│   │   │   # ... similar structure for Balance Flow domain
│   │   │
│   │   ├── category/
│   │   │   # ... etc.
│   │   │
│   │   ├── group/
│   │   │   # ... etc.
│   │   │
│   │   ├── payee/
│   │   │   # ... etc.
│   │   │
│   │   ├── tag/
│   │   │   # ... etc.
│   │   │
│   │   └── # ... other domains like currency, report, noteday, etc.
│   │
│   └── models/               # SQLAlchemy ORM models
│       ├── base.py             # Base class for all models
│       ├── user_models.py
│       ├── account_models.py
│       ├── book_models.py
│       ├── balance_flow_models.py
│       └── # ... other model files corresponding to domains
│
├── tests/                    # Pytest tests
│   ├── conftest.py           # Test fixtures and setup
│   └── domains/
│       └── user/
│           ├── test_user_controller.py
│           └── test_user_service.py
│
├── .gitignore
├── pyproject.toml            # Project metadata and dependencies for uv
└── README.md                 # Project documentation
```

### File Descriptions:

-   **`main.py`**: Initializes the FastAPI app and includes the routers from each domain controller.
-   **`core/`**: Contains cross-cutting concerns. `database.py` will manage the SQLAlchemy engine and session creation. `security.py` will contain a dependency function to extract the user from the JWT.
-   **`domains/<domain>/`**: Each module here represents a feature (e.g., "account", "book").
    -   `*_controller.py`: Defines the API routes using `APIRouter`, handles request validation, and calls the service layer.
    -   `*_service.py`: Implements the core business logic for the domain.
    -   `*_repository.py`: Contains functions to interact with the database for a specific model, using SQLAlchemy.
    -   `*_schemas.py`: Defines the Pydantic models for request and response data structures, ensuring type safety and validation.
-   **`models/`**: Contains the SQLAlchemy model definitions, each corresponding to a database table.
-   **`alembic/`**: Will be used to manage database schema migrations, allowing for version-controlled changes to the database structure.
-   **`tests/`**: Contains all automated tests, mirroring the structure of the `src` directory.
