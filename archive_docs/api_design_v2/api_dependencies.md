# API Endpoint Dependencies

This document outlines the dependencies between the API endpoints for the moneynote application. Understanding these dependencies is crucial for correct API usage.

## General Dependencies

*   **Authentication**: All endpoints require a valid JSON Web Token (JWT) to be passed in the `Authorization` header. This token is obtained through a login process, which in turn requires a user to be registered.
    *   Dependency Chain: `User Registration` -> `User Login` -> `Get JWT` -> `Authenticated API Call`

## Entity Management Dependencies

The application's data model has inherent dependencies. For example, a `Book` must exist before you can add an `Account` to it. A `BalanceFlow` (transaction) requires a `Book`, `Account`, and `Category` to exist.

### User Management

*   **`POST /users/login`**
    *   Depends on: A user having been created via a registration endpoint.
*   **`GET /users/me`**
    *   Depends on: The user being logged in.

### Book Management

*   **`POST /books`**
    *   Depends on: A logged-in user.
*   **`GET /books`, `GET /books/{id}`, `PUT /books/{id}`, `DELETE /books/{id}`**
    *   Depends on: One or more `Book` entities being created.

### Account Management

*   **`POST /accounts`**
    *   Depends on: A `Book` must exist to associate the account with.
*   **`GET /accounts`, `GET /accounts/{id}`, `PUT /accounts/{id}`, `DELETE /accounts/{id}` and all other account-specific endpoints**
    *   Depends on: One or more `Account` entities being created.
*   **`POST /accounts/{id}/adjust`**
    *   Depends on: An `Account` and a `Book` must exist.

### Category Management

*   **`POST /categories`**
    *   Depends on: A `Book` must exist to associate the category with.
*   **`GET /categories`, `GET /categories/{id}`, `PUT /categories/{id}`, `DELETE /categories/{id}`**
    *   Depends on: One or more `Category` entities being created.

### Payee Management

*   **`POST /payees`**
    *   Depends on: A `Book` must exist to associate the payee with.
*   **`GET /payees`, `GET /payees/{id}`, `PUT /payees/{id}`, `DELETE /payees/{id}`**
    *   Depends on: One or more `Payee` entities being created.

### Tag Management

*   **`POST /tags`**
    *   Depends on: A `Book` must exist to associate the tag with.
*   **`GET /tags`, `GET /tags/{id}`, `PUT /tags/{id}`, `DELETE /tags/{id}`**
    *   Depends on: One or more `Tag` entities being created.

### Balance Flow (Transaction) Management

*   **`POST /balance-flows`**
    *   This is a central endpoint with multiple dependencies.
    *   Depends on:
        *   A `Book` must exist.
        *   At least one `Account` must exist (for the `account` and `to` fields).
        *   At least one `Category` must exist (for the `categories` field).
        *   Optionally, a `Payee` can be associated.
        *   Optionally, `Tag`(s) can be associated.
*   **`GET /balance-flows`, `GET /balance-flows/{id}`, `PUT /balance-flows/{id}`, `DELETE /balance-flows/{id}` and all other flow-specific endpoints**
    *   Depends on: One or more `BalanceFlow` entities being created.
*   **`POST /balance-flows/{id}/addFile`**
    *   Depends on: A `BalanceFlow` entity must exist.
*   **`GET /balance-flows/{id}/files`**
    *   Depends on: A `BalanceFlow` entity must exist and have one or more files attached.
