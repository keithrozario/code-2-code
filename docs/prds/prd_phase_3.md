# PRD - Phase 3: Group and Book Creation

## 1) Goal & Scope

**Goal:** To implement the foundational capabilities for creating core data structures: Groups and Books. This phase enables users to organize their finances into distinct containers, either from scratch, from a template, or by copying an existing structure.

**Scope:** This PRD covers the backend API endpoints required to create new groups and books. This includes creating a group with a default book, creating a standalone book in the current group, and creating a book pre-populated with data from a template or another book.

## 2) Functional Specifications

*   **Group Creation:** Users can create a new `Group`, which acts as a collaborative space. Creating a group also creates a default first `Book` within it, based on a user-selected template.
*   **Book Creation (from Scratch):** Users can create a new, empty `Book` within their currently active `Group`.
*   **Book Creation (from Template):** Users can create a new `Book` that is pre-populated with a standard set of `Categories`, `Tags`, and `Payees` from a predefined template (e.g., "Personal Finance").
*   **Book Creation (by Copying):** Users can create a new `Book` by duplicating the entire structure (`Categories`, `Tags`, `Payees`) of one of their existing `Books`.

## 3) UI / UX Flow

This PRD is for the backend API. The expected UI/UX flow is as follows:

1.  A user signs up and is prompted to create their first `Group` and `Book`. They provide a group name and select a book template (e.g., "Default").
2.  Once inside the application, the user can navigate to a "Settings" or "Manage Books" area.
3.  From there, they are presented with options to "Add a new Book".
4.  Choosing this option gives them three choices:
    *   "Create Empty Book": A simple form for a name and currency.
    *   "Create from Template": A form to select a template, provide a name, and set the currency.
    *   "Copy Existing Book": A form to select a source book, provide a new name, and set the currency.
5.  The newly created book becomes available in the user's list of books to switch to.

## 4) Technical Specifications

### 4.1) API Logic

---

#### **Endpoint: `POST /groups`**

*   **Description:** Adds a new `Group` for the current user. As part of the group creation, it also creates the first `Book` for that group, using a provided template. This is the standard onboarding flow.

*   **Business Logic:**
    1.  A user initiates the creation of a new `Group`.
    2.  The system validates that the user has not exceeded the maximum number of groups allowed.
    3.  A new `Group` record is created and associated with the current user as its owner.
    4.  The system then immediately calls the logic to create a new `Book` within this new `Group`, using the `templateId` provided in the request. This involves populating the new book with categories, tags, and payees from the template.
    5.  The user is automatically made a member of the new group.

*   **Request Parameters (`GroupAddForm`):**
    *   `name` (String, Mandatory): The name for the new group.
    *   `defaultCurrencyCode` (String, Mandatory): The default currency for the group and the first book.
    *   `notes` (String, Optional): Descriptive notes for the group.
    *   `templateId` (Integer, Mandatory): The ID of the book template to use for creating the first book.

*   **Responses & Scenarios:**
    *   **200 OK:** The group and its default book are created successfully. Returns the details of the new `Group`.
    *   **400 Bad Request:** Validation fails (e.g., `name` is missing, `templateId` is invalid).
    *   **409 Conflict:** A group with the same name already exists for this user.

*   **Database CRUD Operations:**
    1.  `INSERT` into `t_user_group`.
    2.  `INSERT` into `t_user_book` (for the default book).
    3.  `INSERT` into `t_user_category` (for each category in the template).
    4.  `INSERT` into `t_user_tag` (for each tag in the template).
    5.  `INSERT` into `t_user_payee` (for each payee in the template).
    6.  `INSERT` into `t_user_group_user_relation` (to link the user to the group).

*   **Database SQL Statements:**
    ```sql
    -- Create the group
    INSERT INTO t_user_group (name, owner_id, default_currency_code, notes, create_time) VALUES (?, ?, ?, ?, ?);
    -- Create the first book
    INSERT INTO t_user_book (name, group_id, default_currency_code, notes, create_time) VALUES (?, ?, ?, ?, ?);
    -- Populate categories, tags, payees from template
    INSERT INTO t_user_category (book_id, name, type, ...) VALUES (?, ?, ?, ...);
    INSERT INTO t_user_tag (book_id, name, ...) VALUES (?, ?, ...);
    INSERT INTO t_user_payee (book_id, name, ...) VALUES (?, ?, ...);
    -- Add user to group
    INSERT INTO t_user_group_user_relation (group_id, user_id, role, create_time) VALUES (?, ?, 'Owner', ?);
    ```

---

#### **Endpoint: `POST /books`**

*   **Description:** Adds a new, empty `Book` to the user's currently active `Group`.

*   **Business Logic:**
    1.  The user must be in an active `Group`.
    2.  The system validates that the proposed book `name` is unique within that `Group`.
    3.  A new `Book` record is created and associated with the active `Group`. No categories, tags, or payees are created.

*   **Request Parameters (`BookAddForm`):**
    *   `name` (String, Mandatory): The name for the new book.
    *   `defaultCurrencyCode` (String, Mandatory): The default currency for the book.
    *   `notes` (String, Optional): Descriptive notes.
    *   `sort` (Integer, Optional): A number for sorting purposes.

*   **Responses & Scenarios:**
    *   **200 OK:** The book is created successfully. Returns the details of the new `Book`.
    *   **400 Bad Request:** Validation fails (e.g., `name` is missing).
    *   **409 Conflict:** A book with the same name already exists in the current group.

*   **Database CRUD Operations:**
    1.  `SELECT` from `t_user_book` to check for name uniqueness within the group.
    2.  `INSERT` into `t_user_book`.

*   **Database SQL Statements:**
    ```sql
    -- Check for existing name
    SELECT id FROM t_user_book WHERE group_id = ? AND name = ?;
    -- Create the book
    INSERT INTO t_user_book (name, group_id, default_currency_code, notes, sort, create_time) VALUES (?, ?, ?, ?, ?, ?);
    ```

---

#### **Endpoint: `POST /books/template`**

*   **Description:** Adds a new `Book` to the user's active `Group`, pre-populated with data from a specified template.

*   **Business Logic:**
    1.  The system validates that the book `name` is unique within the active `Group`.
    2.  A new `Book` record is created.
    3.  The system reads a predefined JSON file (`book_tpl.json`) to find the structure of the given `templateId`.
    4.  It then iterates through the template's `categories`, `tags`, and `payees`, creating new database records for each and associating them with the newly created `Book`.

*   **Request Parameters (`BookAddByTemplateForm`):**
    *   `templateId` (Integer, Mandatory): The ID of the template to use.
    *   `book` (`BookAddForm`, Mandatory): An object containing the details for the new book (`name`, `defaultCurrencyCode`, etc.).

*   **Responses & Scenarios:**
    *   **200 OK:** The book and its associated data are created successfully.
    *   **400 Bad Request:** Validation fails (e.g., `templateId` not found, book name missing).
    *   **409 Conflict:** A book with the same name already exists.

*   **Database CRUD Operations:**
    1.  `INSERT` into `t_user_book`.
    2.  `INSERT` into `t_user_category` for each category in the template.
    3.  `INSERT` into `t_user_tag` for each tag in the template.
    4.  `INSERT` into `t_user_payee` for each payee in the template.

*   **Database SQL Statements:**
    ```sql
    -- Create the book
    INSERT INTO t_user_book (name, group_id, default_currency_code, ...) VALUES (?, ?, ?, ...);
    -- Populate from template (example for one category)
    INSERT INTO t_user_category (book_id, name, type, p_id, sort) VALUES (?, ?, ?, ?, ?);
    -- ... repeated for all items in template
    ```

---

#### **Endpoint: `POST /books/copy`**

*   **Description:** Adds a new `Book` by copying the structure (`Categories`, `Tags`, `Payees`) of an existing `Book`.

*   **Business Logic:**
    1.  The system validates that the new book `name` is unique within the active `Group`.
    2.  A new `Book` record is created.
    3.  The system queries the database for all `Category`, `Tag`, and `Payee` records associated with the source `bookId`.
    4.  It then creates new records for each of these items, associating them with the new `Book`.

*   **Request Parameters (`BookAddByBookForm`):**
    *   `bookId` (Integer, Mandatory): The ID of the book to copy from.
    *   `book` (`BookAddForm`, Mandatory): An object containing the details for the new book (`name`, `defaultCurrencyCode`, etc.).

*   **Responses & Scenarios:**
    *   **200 OK:** The book is successfully copied.
    *   **400 Bad Request:** Validation fails (e.g., source `bookId` not found, new name missing).
    *   **409 Conflict:** A book with the same name already exists.

*   **Database CRUD Operations:**
    1.  `INSERT` into `t_user_book`.
    2.  `SELECT` from `t_user_category` WHERE `book_id` = source `bookId`.
    3.  `INSERT` into `t_user_category` for the new book.
    4.  (Repeat for `t_user_tag` and `t_user_payee`).

*   **Database SQL Statements:**
    ```sql
    -- Create the new book
    INSERT INTO t_user_book (name, group_id, ...) VALUES (?, ?, ...);
    -- Get source categories
    SELECT * FROM t_user_category WHERE book_id = ?;
    -- Insert copied categories
    INSERT INTO t_user_category (book_id, name, type, p_id, sort) VALUES (?, ?, ?, ?, ?);
    -- ... repeated for all source categories, tags, and payees
    ```

## 5) Data Model

This phase impacts the `Group` and `Book` entities, which are central to data organization.

*   **`Group` (`t_user_group` table):**
    *   Represents a workspace for collaboration. A user can be a member of multiple groups.
    *   All data (`Books`, `Accounts`, `Transactions`) is scoped within a `Group`.
    *   **Key Fields:** `id`, `name`, `owner_id`, `default_currency_code`.

*   **`Book` (`t_user_book` table):**
    *   Represents an independent ledger within a `Group`.
    *   It has its own set of `Categories`, `Tags`, and `Payees`.
    *   Transactions (`BalanceFlows`) belong to a single `Book`.
    *   **Key Fields:** `id`, `name`, `group_id`, `default_currency_code`, `enable`.

## 6) Test Cases

| Test Case ID | Feature | Test Steps | Test Data | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-P3-01** | Create Group | 1. Call `POST /groups`. | `name`: "Family Finances", `templateId`: 1, `defaultCurrencyCode`: "USD" | 200 OK. A new group is created. A new book is also created inside it with categories from template 1. |
| **TC-P3-02** | Create Book (Scratch) | 1. Set active group. <br> 2. Call `POST /books`. | `name`: "2025 Vacation", `defaultCurrencyCode`: "EUR" | 200 OK. A new, empty book is created in the active group. |
| **TC-P3-03** | Create Book (Template) | 1. Set active group. <br> 2. Call `POST /books/template`. | `templateId`: 2, `book`: { `name`: "Side Business", `defaultCurrencyCode`: "USD" } | 200 OK. A new book is created, populated with categories, tags, and payees from template 2. |
| **TC-P3-04** | Create Book (Copy) | 1. Set active group. <br> 2. An existing book with ID 5 exists. <br> 3. Call `POST /books/copy`. | `bookId`: 5, `book`: { `name`: "2026 Taxes", `defaultCurrencyCode`: "USD" } | 200 OK. A new book is created with the same categories, tags, and payees as book 5. |
| **TC-P3-05** | **(Negative)** Duplicate Book Name | 1. A book named "Personal" exists. <br> 2. Call `POST /books`. | `name`: "Personal" | 409 Conflict error. |
| **TC-P3-06** | **(Negative)** Invalid Template ID | 1. Call `POST /books/template`. | `templateId`: 999 (does not exist) | 400 Bad Request error. |

## 7) Risks & Mitigations

*   **Risk:** Creating a book from a template or by copying a large book could be slow and resource-intensive.
    *   **Mitigation:** The operation should be performed within a single database transaction. For very large copies, consider an asynchronous job queue, though this is out of scope for the current phase.
*   **Risk:** Race condition if two users try to create a book with the same name at the same time.
    *   **Mitigation:** Add a `UNIQUE` constraint on (`group_id`, `name`) in the `t_user_book` table schema to enforce uniqueness at the database level.
*   **Risk:** A failure during the population of a book (from template/copy) could leave a partially created book.
    *   **Mitigation:** Ensure the entire creation process is wrapped in a single, atomic database transaction. If any part fails, the entire operation should be rolled back.

## 8) Open Questions

1.  What is the expected behavior if the `book_tpl.json` file is missing or malformed at startup? Does the application fail to start, or does it start with the "create from template" feature disabled?
2.  Are there limits on the number of categories, tags, or payees that can be in a template or a book to be copied? If not, this could be a performance concern.

## 9) Task Seeds (for Agent Decomposition)

1.  Implement the `POST /groups` endpoint in `routers/groups.py`.
2.  Create the service logic to handle group creation and the subsequent call to the book creation service.
3.  Implement the `POST /books` endpoint in `routers/books.py` to handle creation from scratch.
4.  Implement the `POST /books/template` endpoint. This includes the logic to parse the `book_tpl.json` file and create associated entities.
5.  Implement the `POST /books/copy` endpoint. This includes the logic to query a source book's structure and replicate it for a new book.
6.  Add database `UNIQUE` constraint for `(group_id, name)` on the `t_user_book` table.
7.  Write unit tests for the `BookService` and `GroupService` to cover all creation and error scenarios.
8.  Write integration tests for all four new API endpoints.

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
- [✔] Write Integration Tests for All Phase 1 Endpoints- [✔] Update Data Models and Create Database Migration
- [✔] Define Pydantic Schemas for Session and Binding
- [✔] Implement CRUD Functions for User and Invite Code
- [✔] Add Password Hashing Utility and Dependency
- [✔] Implement `get_initial_state` Service Logic
- [✔] Implement `bind_user` Service Logic
- [✔] Create `GET /initState` API Endpoint
- [✔] Create `PUT /bind` API Endpoint
- [✔] Write Integration Tests for Phase 2 Endpoints
- [✔] Update API Documentation# Moneynote API - Detailed Design Document

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
