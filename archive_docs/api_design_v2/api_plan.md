# API Endpoint Dependencies

This document outlines the dependencies between the API endpoints for the moneynote application. An API endpoint has a dependency on another if it requires data created by that other endpoint to function correctly.

---

## Accounts API

### `POST /accounts`

Adds a new account.

*   **Dependencies:** None. This is a primary endpoint for creating a new account.

### `GET /accounts`

Queries for accounts.

*   **Dependencies:**
    *   `POST /accounts`: At least one account must have been created to be listed.

### `GET /accounts/{id}`

Retrieves a specific account.

*   **Dependencies:**
    *   `POST /accounts`: The account with the specified `{id}` must have been created.

### `PUT /accounts/{id}`

Updates a specific account.

*   **Dependencies:**
    *   `POST /accounts`: The account with the specified `{id}` must have been created.

### `DELETE /accounts/{id}`

Removes a specific account.

*   **Dependencies:**
    *   `POST /accounts`: The account with the specified `{id}` must have been created.

### `GET /accounts/all`

Retrieves all accounts.

*   **Dependencies:**
    *   `POST /accounts`: At least one account must have been created to be listed.

### `PATCH /accounts/{id}/toggle`

Toggles the `enable` status of an account.

*   **Dependencies:**
    *   `POST /accounts`: The account with the specified `{id}` must have been created.

### `PATCH /accounts/{id}/toggleInclude`

Toggles the `include` status of an account.

*   **Dependencies:**
    *   `POST /accounts`: The account with the specified `{id}` must have been created.

### `POST /accounts/{id}/adjust`

Adjusts the balance of an account. The request body requires a `book` ID.

*   **Dependencies:**
    *   `POST /accounts`: The account with the specified `{id}` must have been created.
    *   `POST /books`: A book must have been created to be referenced in the request body. (Assumed endpoint)

### `PUT /accounts/{id}/adjust`

Updates a balance adjustment.

*   **Dependencies:**
    *   `POST /accounts/{id}/adjust`: A balance adjustment must have been created for the specified account.

---

## Balance Flow API

### `POST /balance-flows`

Adds a new balance flow (transaction). The request body requires IDs for `book`, `account`, `categories`, `payee`, and `tags`.

*   **Dependencies:**
    *   `POST /books`: A book must have been created. (Assumed endpoint)
    *   `POST /accounts`: At least one account must have been created to be used as the source or destination account.
    *   `POST /categories`: Categories must have been created to be associated with the flow. (Assumed endpoint)
    *   `POST /payees`: A payee must have been created. (Assumed endpoint)
    *   `POST /tags`: Tags must have been created to be associated with the flow. (Assumed endpoint)

### `GET /balance-flows`

Queries for balance flows.

*   **Dependencies:**
    *   `POST /balance-flows`: At least one balance flow must have been created to be listed.

### `GET /balance-flows/{id}`

Retrieves a specific balance flow.

*   **Dependencies:**
    *   `POST /balance-flows`: The balance flow with the specified `{id}` must have been created.

### `PUT /balance-flows/{id}`

Updates a specific balance flow.

*   **Dependencies:**
    *   `POST /balance-flows`: The balance flow with the specified `{id}` must have been created.

### `DELETE /balance-flows/{id}`

Removes a specific balance flow.

*   **Dependencies:**
    *   `POST /balance-flows`: The balance flow with the specified `{id}` must have been created.

### `PATCH /balance-flows/{id}/confirm`

Confirms a specific balance flow.

*   **Dependencies:**
    *   `POST /balance-flows`: The balance flow with the specified `{id}` must have been created.

### `POST /balance-flows/{id}/addFile`

Adds a file to a balance flow.

*   **Dependencies:**
    *   `POST /balance-flows`: The balance flow with the specified `{id}` must have been created.

### `GET /balance-flows/{id}/files`

Retrieves files for a balance flow.

*   **Dependencies:**
    *   `POST /balance-flows/{id}/addFile`: At least one file must have been added to the balance flow.
