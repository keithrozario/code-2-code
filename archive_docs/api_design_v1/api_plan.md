# API Endpoint Dependencies

This document outlines the dependencies between the various API endpoints in the MoneyNote application. Understanding these dependencies is crucial for planning API implementation and testing.

---

## Core Concepts

The API revolves around a few core concepts that have inherent dependencies:

1.  **User**: A user must exist before any other action can be taken.
2.  **Group**: A group is a collection of users and books.
3.  **Book**: A book is a ledger for financial records. It belongs to a group.
4.  **Account**: A financial account (e.g., bank account, credit card).
5.  **Category, Payee, Tag**: These are used to classify transactions.
6.  **Balance Flow**: A transaction (expense, income, transfer).
7.  **Note Day**: A recurring event or reminder.

---

## User and Authentication API

The User and Authentication API is the foundation of the entire application.

*   **`POST /register`**
    *   **Dependencies**: None. This is the entry point for a new user.
    *   **Dependents**: `POST /login`, `PUT /bind`, `POST /groups/{id}/inviteUser`.

*   **`POST /login`**
    *   **Dependencies**: `POST /register`. A user must be registered to log in.
    *   **Dependents**: Almost all other API endpoints require an authenticated user.

*   **`POST /logout`**
    *   **Dependencies**: `POST /login`. A user must be logged in to log out.
    *   **Dependents**: None.

*   **`PUT /bind`**
    *   **Dependencies**: `POST /register`.
    *   **Dependents**: None.

*   **`GET /initState`**
    *   **Dependencies**: `POST /login`.
    *   **Dependents**: None.

*   **`PATCH /changePassword`**
    *   **Dependencies**: `POST /login`.
    *   **Dependents**: None.

*   **`PATCH /setDefaultBook/{id}`**
    *   **Dependencies**: `POST /login`, `POST /books`.
    *   **Dependents**: None.

*   **`PATCH /setDefaultGroup/{id}`**
    *   **Dependencies**: `POST /login`, `POST /groups`.
    *   **Dependents**: None.

*   **`PATCH /setDefaultGroupAndBook/{id}`**
    *   **Dependencies**: `POST /login`, `POST /groups`, `POST /books`.
    *   **Dependents**: None.

*   **`GET /bookSelect/all`**
    *   **Dependencies**: `POST /login`, `POST /books`.
    *   **Dependents**: None.

---

## Group API

Groups are for collaboration.

*   **`POST /groups`**
    *   **Dependencies**: `POST /login`.
    *   **Dependents**: `GET /groups`, `PUT /groups/{id}`, `DELETE /groups/{id}`, `POST /groups/{id}/inviteUser`, `GET /groups/{id}/users`, `PATCH /setDefaultGroup/{id}`.

*   **Other Group Endpoints (`GET`, `PUT`, `DELETE`, `invite`, `remove`, etc.)**
    *   **Dependencies**: `POST /groups` to have a group to operate on.
    *   **`POST /groups/{id}/inviteUser`** also depends on `POST /register` to have a user to invite.
    *   **`POST /groups/{id}/agree`** and **`POST /groups/{id}/reject`** depend on `POST /groups/{id}/inviteUser`.

---

## Books API

Books are the ledgers.

*   **`POST /books`**
    *   **Dependencies**: `POST /login`. Can optionally be associated with a group.
    *   **Dependents**: `GET /books`, `GET /books/all`, `GET /books/{id}`, `PUT /books/{id}`, `DELETE /books/{id}`, `PATCH /books/{id}/toggle`, `POST /books/copy`, `GET /books/{id}/export`, `PATCH /setDefaultBook/{id}`, `POST /balance-flows`.

*   **`POST /books/template`**
    *   **Dependencies**: `POST /login`.
    *   **Dependents**: None.

*   **`POST /books/copy`**
    *   **Dependencies**: `POST /books`.
    *   **Dependents**: None.

*   **`GET /books/{id}/export`**
    *   **Dependencies**: `POST /books`, `POST /balance-flows`.
    *   **Dependents**: None.

*   **Other Book Endpoints (`GET`, `PUT`, `DELETE`, `PATCH`)**
    *   **Dependencies**: `POST /books`.

---

## Accounts API

Accounts hold the money.

*   **`POST /accounts`**
    *   **Dependencies**: `POST /login`.
    *   **Dependents**: All other `/accounts` endpoints, `POST /balance-flows`.

*   **`POST /accounts/{id}/adjust`**
    *   **Dependencies**: `POST /accounts`, `POST /books`.
    *   **Dependents**: `PUT /accounts/{id}/adjust`.

*   **Other Account Endpoints (`GET`, `PUT`, `DELETE`, `PATCH`)**
    *   **Dependencies**: `POST /accounts`.

---

## Categories, Payees, and Tags APIs

These are for classifying transactions. They all follow a similar pattern.

*   **`POST /categories`**, **`POST /payees`**, **`POST /tags`**
    *   **Dependencies**: `POST /login`. Can be associated with a book.
    *   **Dependents**: The corresponding `GET`, `PUT`, `DELETE`, `PATCH` endpoints, and `POST /balance-flows`.

*   **Other Endpoints (`GET`, `PUT`, `DELETE`, `PATCH`)**
    *   **Dependencies**: The corresponding `POST` endpoint (e.g., `PUT /categories/{id}` depends on `POST /categories`).

---

## Balance Flow API

This is the core transaction API.

*   **`POST /balance-flows`**
    *   **Dependencies**: `POST /books`, `POST /accounts`. Can also depend on `POST /categories`, `POST /payees`, `POST /tags`.
    *   **Dependents**: All other `/balance-flows` endpoints, and all `/reports` endpoints.

*   **`POST /balance-flows/{id}/addFile`**
    *   **Dependencies**: `POST /balance-flows`.
    *   **Dependents**: `GET /balance-flows/{id}/files`, `GET /flow-files/view`, `DELETE /flow-files/{id}`.

*   **Other Balance Flow Endpoints (`GET`, `PUT`, `DELETE`, `PATCH`)**
    *   **Dependencies**: `POST /balance-flows`.

---

## Files API

For transaction attachments.

*   **`GET /flow-files/view`**
    *   **Dependencies**: `POST /balance-flows/{id}/addFile`.
    *   **Dependents**: None.

*   **`DELETE /flow-files/{id}`**
    *   **Dependencies**: `POST /balance-flows/{id}/addFile`.
    *   **Dependents**: None.

---

## Note Day API

For reminders.

*   **`POST /note-days`**
    *   **Dependencies**: `POST /login`.
    *   **Dependents**: All other `/note-days` endpoints.

*   **`PATCH /note-days/{id}/recall`**
    *   **Dependencies**: `PATCH /note-days/{id}/run`.

*   **Other Note Day Endpoints (`GET`, `PUT`, `DELETE`, `PATCH`)**
    *   **Dependencies**: `POST /note-days`.

---

## Currency API

Mostly independent, but crucial for creating accounts and transactions.

*   **`GET /currencies`, `GET /currencies/all`, `POST /currencies/refresh`**
    *   **Dependencies**: None.
    *   **Dependents**: `POST /accounts`, `POST /balance-flows`.

---

## Reports API

For summarizing financial data.

*   **All `/reports` endpoints**
    *   **Dependencies**: `POST /balance-flows` to have data to generate reports from. They also implicitly depend on `POST /books`, `POST /accounts`, `POST /categories`, `POST /payees`, and `POST /tags` which are all part of creating the balance flows.
    *   **Dependents**: None.
