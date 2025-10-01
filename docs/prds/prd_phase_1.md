# Product Requirements Document: Moneynote API - Phase 1

## 1) Goal & Scope

This document outlines the requirements for Phase 1 of the Moneynote backend API. The primary goal of this phase is to establish the foundational, independent endpoints required for the application to function. The scope is strictly limited to creating the initial building blocks: user registration, and endpoints to retrieve static application data such as version, currencies, and book templates.

## 2) Functional Specifications

The API will provide the following functionalities in Phase 1:

*   **FS-001: User Registration:** Allow a new user to create an account using a username, password, and a valid invitation code.
*   **FS-002: Currency Information:** Provide a list of all supported currencies and their exchange rates.
*   **FS-003: Book Template Information:** Provide a list of all available templates that can be used to create new financial books.
*   **FS-004: Application Version:** Expose an endpoint to check the current running version of the application.
*   **FS-005: Test/Configuration Endpoint:** Expose a test endpoint that returns the application's base URL.

## 3) UI / UX Flow

This PRD is for a backend API, so there is no direct UI. However, the expected interaction from a client application would be:

1.  **Registration Screen:** A client application would present a form for `username`, `password`, and `inviteCode`. On submission, it would call `POST /register`.
2.  **Book Creation Screen:** When a user creates a new book, the client would call `GET /book-templates/all` to populate a list of templates for the user to choose from.
3.  **Account/Transaction Creation:** When a user needs to select a currency, the client would have already fetched the list from `GET /currencies/all` to display the available options.

## 4) Technical Specifications

### 4.1) API Logic

---

#### **Endpoint: `GET /version`**

*   **Description:** Returns the current version of the deployed application. This is useful for client-side compatibility checks and debugging.
*   **Business Logic:** The endpoint retrieves the application version, which is defined in the project's build configuration (`build.gradle`). It returns this version string as a response.
*   **Request Parameters:**
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)
*   **Responses and Scenarios:**
    *   **200 OK (Success):** The user is authenticated.
        ```json
        {
          "data": "1.0.0"
        }
        ```
    *   **401 Unauthorized:** The `Authorization` header is missing or the token is invalid.
*   **Database CRUD Operations:** None.
*   **Database SQL Statements:** None.

---

#### **Endpoint: `GET /test3`**

*   **Description:** Returns the base URL of the application. This is a utility endpoint primarily for testing and configuration verification.
*   **Business Logic:** The endpoint retrieves the application's base URL from its runtime configuration (e.g., `application.properties`) and returns it as a string.
*   **Request Parameters:**
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)
*   **Responses and Scenarios:**
    *   **200 OK (Success):** The user is authenticated.
        ```json
        {
          "data": "http://localhost:8080"
        }
        ```
    *   **401 Unauthorized:** The `Authorization` header is missing or the token is invalid.
*   **Database CRUD Operations:** None.
*   **Database SQL Statements:** None.

---

#### **Endpoint: `POST /register`**

*   **Description:** Registers a new user in the system. No authentication is required for this endpoint.
*   **Business Logic:**
    1.  The system validates that `username`, `password`, and `inviteCode` are present in the request body.
    2.  It checks if a user with the given `username` already exists. If so, the request fails.
    3.  It validates the `inviteCode`. If the code is not valid, the request fails.
    4.  The user's `password` is securely hashed using BCrypt.
    5.  A new `User` record is created and saved to the database.
    6.  A default `Group` and a default `Book` are created for the new user.
*   **Request Parameters:**
    *   **Body:**
        *   `username` (String, Mandatory): The desired username.
        *   `password` (String, Mandatory): The user's password.
        *   `inviteCode` (String, Mandatory): A valid invitation code.
*   **Responses and Scenarios:**
    *   **201 Created (Success):** The user account was successfully created. The response body is empty.
    *   **400 Bad Request:** Required fields are missing from the request, or the `inviteCode` is invalid.
    *   **409 Conflict:** A user with the provided `username` already exists.
*   **Database CRUD Operations:**
    *   `READ` from `t_user` to check for username uniqueness.
    *   `READ` from an assumed `t_invite_code` table to validate the code.
    *   `CREATE` a new record in `t_user`.
    *   `CREATE` a new record in `t_user_group`.
    *   `CREATE` a new record in `t_user_book`.
*   **Database SQL Statements:**
    ```sql
    -- Check for existing user
    SELECT 1 FROM t_user WHERE username = ?;

    -- Create new user
    INSERT INTO t_user (username, password, create_time) VALUES (?, ?, ?);

    -- Create default group for the user
    INSERT INTO t_user_group (name, owner_id, create_time) VALUES (?, ?, ?);

    -- Create default book for the user
    INSERT INTO t_user_book (name, group_id, default_currency_code, create_time) VALUES (?, ?, ?, ?);
    ```

---

#### **Endpoint: `GET /currencies/all`**

*   **Description:** Retrieves the complete list of all currencies supported by the application.
*   **Business Logic:** On application startup, currency data is loaded from a `currency.json` file into an in-memory cache. This endpoint reads the list of currencies directly from this in-memory cache and returns it.
*   **Request Parameters:**
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)
*   **Responses and Scenarios:**
    *   **200 OK (Success):** Returns a list of currency objects.
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
    *   **401 Unauthorized:** The `Authorization` header is missing or the token is invalid.
*   **Database CRUD Operations:** None.
*   **Database SQL Statements:** None.

---

#### **Endpoint: `GET /book-templates/all`**

*   **Description:** Retrieves a list of all available book templates.
*   **Business Logic:** Similar to currencies, book templates are loaded from a `book_tpl.json` file into memory on application startup. This endpoint reads this cached list and returns it, providing clients with the necessary information to use the "Create Book from Template" feature.
*   **Request Parameters:**
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)
*   **Responses and Scenarios:**
    *   **200 OK (Success):** Returns a list of book template objects, each with an ID and name.
        ```json
        [
            {
                "id": 1,
                "name": "Daily Life"
            },
            {
                "id": 2,
                "name": "Catering Shop"
            }
        ]
        ```
    *   **401 Unauthorized:** The `Authorization` header is missing or the token is invalid.
*   **Database CRUD Operations:** None.
*   **Database SQL Statements:** None.

## 5) Data Model

The following data structures are affected or defined in this phase.

*   **User (`t_user` table)**
    | Field | Type | Constraints | Description |
    |---|---|---|---|
    | `id` | INTEGER | PRIMARY KEY | Unique identifier for the user. |
    | `username` | VARCHAR | UNIQUE, NOT NULL | User's chosen username. |
    | `password` | VARCHAR | NOT NULL | Securely hashed password. |
    | `create_time` | BIGINT | NOT NULL | Timestamp of user creation. |
    | `default_group_id` | INTEGER | FK to `t_user_group` | The default group for the user. |

*   **Currency (In-memory Object)**
    | Field | Type | Description |
    |---|---|---|
    | `id` | Integer | Unique identifier. |
    | `name` | String | 3-letter currency code (e.g., "USD"). |
    | `description` | String | Full currency name. |
    | `rate` | Double | Exchange rate against the base currency (USD). |

*   **Book Template (In-memory Object)**
    | Field | Type | Description |
    |---|---|---|
    | `id` | Integer | Unique identifier. |
    | `name` | String | Name of the template (e.g., "Personal Budget"). |

## 6) Test Cases

| Test Case ID | Endpoint | Test Case | Expected Result |
|---|---|---|---|
| TC-P1-01 | `GET /version` | Request with a valid token. | **200 OK** with the application version in the response body. |
| TC-P1-02 | `GET /version` | Request without a token. | **401 Unauthorized**. |
| TC-P1-03 | `POST /register` | Register with a unique username and valid invite code. | **201 Created**. A new user record appears in the `t_user` table. |
| TC-P1-04 | `POST /register` | Register with a username that already exists. | **409 Conflict**. |
| TC-P1-05 | `POST /register` | Register with an invalid invite code. | **400 Bad Request**. |
| TC-P1-06 | `POST /register` | Register without providing a password. | **400 Bad Request**. |
| TC-P1-07 | `GET /currencies/all` | Request with a valid token. | **200 OK** with a list of all currencies from `currency.json`. |
| TC-P1-08 | `GET /book-templates/all` | Request with a valid token. | **200 OK** with a list of all book templates from `book_tpl.json`. |

## 7) Risks & Mitigations

| Risk | Mitigation |
|---|---|
| **User Registration Abuse:** The `POST /register` endpoint is public and could be targeted by bots for spam account creation. | In a future phase, implement rate limiting, a CAPTCHA challenge, or a more robust invitation system where invite codes are single-use and expire. |
| **In-memory Data Scalability:** Storing currencies and templates in memory does not scale across multiple application instances. | For a horizontally scaled deployment, this data should be moved to a shared data store like a database or a distributed cache (e.g., Redis). |
| **Hardcoded Configuration:** The version and base URL may be hardcoded. | These values should be injected from the build environment (`build.gradle`) and runtime configuration (`application.properties`) respectively, to ensure they are always accurate. |
| **Security of Test Endpoints:** The `GET /version` and `GET /test3` endpoints require authentication, which is good, but their purpose is for diagnostics. | Maintain authentication on these endpoints. Ensure no sensitive information is ever exposed through them. |

## 8) Open Questions

1.  What is the specific validation logic for an `inviteCode`? Is it a static list, or are they generated and stored in a database table?
2.  Should the `GET /version` endpoint require authentication? Typically, version endpoints are public for easy access by monitoring tools.
3.  What is the full data structure of a book template returned by `GET /book-templates/all`? The plan says "ID and name", but the definition is vague. (Clarified for this doc to be ID and Name).

## 9) Task Seeds (for Agent Decomposition)

1.  Implement `TestController` with `GET /version` endpoint to read version from build config.
2.  Implement `GET /test3` in `TestController` to read base URL from runtime properties.
3.  Implement `UserController` with `POST /register` endpoint.
4.  Implement `UserService` to handle user creation logic: check for duplicates, hash password, validate invite code, and save the new user.
5.  Implement database logic to create a default `Group` and `Book` upon user registration.
6.  Implement `CurrencyController` with `GET /currencies/all` endpoint.
7.  Implement `CurrencyService` to read the list of currencies from the `ApplicationScopeBean`.
8.  Implement `BookTemplateController` with `GET /book-templates/all` endpoint.
9.  Implement `BookTemplateService` to read the list of templates from the `ApplicationScopeBean`.
10. Write unit and integration tests for all Phase 1 endpoints and services.
