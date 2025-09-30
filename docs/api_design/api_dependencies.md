# API Endpoint Dependencies

This document outlines the dependencies between the API endpoints in the MoneyNote application. Understanding these dependencies is crucial for correct API usage and integration testing.

---

## Core Concepts

The API is structured around a few core concepts:

1.  **User**: The central entity. Most other data is directly or indirectly associated with a user.
2.  **Group**: A collection of users for collaboration.
3.  **Book**: A financial ledger that belongs to a user or a group. It contains accounts, categories, payees, tags, and transactions.
4.  **Account**: Represents a real-world financial account (e.g., bank account, credit card).
5.  **Category, Payee, Tag**: Used to classify and organize transactions.
6.  **Balance Flow**: A financial transaction (expense, income, transfer, or adjustment).

## Dependency List

### User and Authentication API (`/register`, `/login`, etc.)

-   **`POST /register`**
    -   Dependencies: **None**. This is the starting point for a new user.

-   **`POST /login`**
    -   Dependencies:
        -   `POST /register`: A user must be registered before they can log in.

-   **`POST /logout`**
    -   Dependencies:
        -   `POST /login`: A user must be logged in to be able to log out.

-   **`GET /initState`**
    -   Dependencies:
        -   `POST /login`: A user must be logged in to retrieve their initial application state.

-   **`PATCH /changePassword`**
    -   Dependencies:
        -   `POST /login`: A user must be logged in to change their password.

### Group API (`/groups`)

-   **`POST /groups`**
    -   Dependencies:
        -   `POST /login`: A user must be logged in to create a group.

-   **All other `/groups` endpoints (GET, PUT, DELETE, invite, etc.)**
    -   Dependencies:
        -   `POST /groups`: A group must exist to be managed or viewed.

-   **`POST /groups/{id}/agree` & `POST /groups/{id}/reject`**
    -   Dependencies:
        -   `POST /groups/{id}/inviteUser`: A user must be invited to a group before they can agree or reject the invitation.

### Book API (`/books`)

-   **`POST /books`**
    -   Dependencies:
        -   `POST /login`: A user must be logged in to create a book.

-   **All other `/books` endpoints (GET, PUT, DELETE, toggle, etc.)**
    -   Dependencies:
        -   `POST /books`: A book must exist to be managed or viewed.

-   **`POST /books/copy`**
    -   Dependencies:
        -   `POST /books`: A book must exist to be copied.

-   **`PATCH /setDefaultBook/{id}`**
    -   Dependencies:
        -   `POST /login`: A user must be logged in.
        -   `POST /books`: The book to be set as default must exist.

### Account API (`/accounts`)

-   **`POST /accounts`**
    -   Dependencies:
        -   `POST /books`: An account must be associated with a book.

-   **All other `/accounts` endpoints (GET, PUT, DELETE, toggle, etc.)**
    -   Dependencies:
        -   `POST /accounts`: An account must exist to be managed or viewed.

-   **`POST /accounts/{id}/adjust`**
    -   Dependencies:
        -   `POST /accounts`: The account to be adjusted must exist.
        -   `POST /books`: The adjustment is recorded within a book.

### Category, Payee, and Tag APIs (`/categories`, `/payees`, `/tags`)

-   **`POST /categories`, `POST /payees`, `POST /tags`**
    -   Dependencies:
        -   `POST /books`: These entities are created within the context of a specific book.

-   **All other endpoints for these APIs (GET, PUT, DELETE, toggle, etc.)**
    -   Dependencies:
        -   `POST /categories`, `POST /payees`, `POST /tags`: The respective entity must exist to be managed or viewed.

### Balance Flow API (`/balance-flows`)

-   **`POST /balance-flows`**
    -   Dependencies:
        -   `POST /books`: A transaction must belong to a book.
        -   `POST /accounts`: A transaction involves at least one account.
        -   (Optional) `POST /categories`, `POST /payees`, `POST /tags`: A transaction can be classified with these entities.

-   **All other `/balance-flows` endpoints (GET, PUT, DELETE, confirm, etc.)**
    -   Dependencies:
        -   `POST /balance-flows`: A balance flow (transaction) must exist to be managed or viewed.

-   **`POST /balance-flows/{id}/addFile`**
    -   Dependencies:
        -   `POST /balance-flows`: A balance flow must exist to have a file attached to it.

### Files API (`/flow-files`)

-   **`GET /flow-files/view` & `DELETE /flow-files/{id}`**
    -   Dependencies:
        -   `POST /balance-flows/{id}/addFile`: A file must have been attached to a balance flow to be viewed or deleted.

### Reports API (`/reports`)

-   **All `/reports` endpoints**
    -   Dependencies:
        -   `POST /balance-flows`: Reports are generated based on existing transaction data.
        -   `POST /books`, `POST /accounts`, `POST /categories`, `POST /payees`, `POST /tags`: These entities are used to filter and aggregate the data in the reports.

### Note Day API (`/note-days`)

-   **`POST /note-days`**
    -   Dependencies:
        -   `POST /login`: Note days are user-specific reminders.

-   **All other `/note-days` endpoints (GET, PUT, DELETE, run, recall)**
    -   Dependencies:
        -   `POST /note-days`: A note day must exist to be managed or viewed.

### Currency API (`/currencies`)

-   **Dependencies**: This API is mostly self-contained. It provides data that is used by other entities (like Accounts and Books), but its own operations do not have strong dependencies on the creation of other resources. `POST /currencies/refresh` indicates that the data is likely sourced externally.
