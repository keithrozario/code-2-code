# API Endpoint Dependencies

This document outlines the dependencies between the various API endpoints in the Moneynote application. Understanding these dependencies is crucial for correct API usage and integration testing.

---

## General Dependencies

- **Authentication:** Most endpoints require a user to be authenticated. This means a user must be created via `POST /register` and then logged in using `POST /login` to obtain a JWT token.
- **Book Selection:** Many endpoints operate within the context of a specific "book". A book must be created (`POST /books`) and often set as the current session book.

---

## 1. Test API

Endpoints in this section are for testing and generally have no dependencies on other API resources.

- **`GET /version`**: No dependencies.
- **`GET /test3`**: No dependencies.

---

## 2. User API

- **`POST /login`**: Depends on a user account existing, created via `POST /register`.
- **`POST /logout`**: Depends on an active user session (i.e., user must be logged in).
- **`POST /register`**: No dependencies. This is a starting point for user creation.
- **`PUT /bind`**: Depends on an active user session.
- **`GET /initState`**: Depends on an active user session.
- **`PATCH /setDefaultBook/{id}`**: Depends on an active user session and the existence of a Book with the specified `{id}` (created via `POST /books`).
- **`PATCH /setDefaultGroup/{id}`**: Depends on an active user session and the existence of a Group with the specified `{id}` (created via `POST /groups`).
- **`PATCH /changePassword`**: Depends on an active user session.
- **`GET /bookSelect/all`**: Depends on an active user session.
- **`PATCH /setDefaultGroupAndBook/{id}`**: Depends on an active user session and the existence of the corresponding Group and Book.

---

## 3. Account API

All endpoints in this section depend on an active user session and a selected Book context.

- **`POST /accounts`**:
    - Depends on the existence of a Book to associate the account with.
    - Depends on the existence of Currencies (`GET /currencies/all`).
- **`GET /accounts`**: Depends on at least one Account having been created via `POST /accounts`.
- **`GET /accounts/{id}`**: Depends on the existence of an Account with the specified `{id}`.
- **`GET /accounts/statistics`**: Depends on the existence of one or more accounts.
- **`PUT /accounts/{id}`**: Depends on the existence of an Account with the specified `{id}`.
- **`DELETE /accounts/{id}`**: Depends on the existence of an Account with the specified `{id}`.
- **`GET /accounts/all`**: Depends on at least one Account having been created.
- **`PATCH /accounts/{id}/*`**: All toggle endpoints depend on the existence of an Account with the specified `{id}`.
- **`POST /accounts/{id}/adjust`**: Depends on the existence of an Account with the specified `{id}`.
- **`PUT /accounts/{id}/adjust`**: Depends on a previous balance adjustment having been made with `POST /accounts/{id}/adjust`.
- **`GET /accounts/overview`**: Depends on the existence of one or more accounts.
- **`PUT /accounts/{id}/updateNotes`**: Depends on the existence of an Account with the specified `{id}`.

---

## 4. Balance Flow API

These endpoints are for managing financial transactions (balance flows).

- **`POST /balance-flows`**: This is a core endpoint with multiple potential dependencies based on the data provided.
    - **Required**: A Book (`book` ID) and an Account (`account` ID) must exist.
    - **Optional**: If `categories`, `payee`, `tags`, or a `to` account are specified, those entities must already exist. This implies dependencies on:
        - `POST /categories`
        - `POST /payees`
        - `POST /tags`
        - `POST /accounts` (for the `to` account)
- **`GET /balance-flows`**: Depends on at least one balance flow record being created via `POST /balance-flows`.
- **`GET /balance-flows/{id}`**: Depends on the existence of a Balance Flow with the specified `{id}`.
- **`PUT /balance-flows/{id}`**: Depends on the existence of a Balance Flow with the specified `{id}`.
- **`DELETE /balance-flows/{id}`**: Depends on the existence of a Balance Flow with the specified `{id}`.
- **`GET /balance-flows/statistics`**: Depends on the existence of balance flow records.
- **`PATCH /balance-flows/{id}/confirm`**: Depends on the existence of a Balance Flow with the specified `{id}`.
- **`POST /balance-flows/{id}/addFile`**: Depends on the existence of a Balance Flow with the specified `{id}`.
- **`GET /balance-flows/{id}/files`**: Depends on files having been added to the balance flow via `POST /balance-flows/{id}/addFile`.

---

## 5. Book API

- **`GET /books`**: Depends on at least one Book having been created via `POST /books`.
- **`GET /books/{id}`**: Depends on the existence of a Book with the specified `{id}`.
- **`POST /books`**:
    - Depends on an active user session.
    - Optionally depends on the existence of Accounts and Categories if default IDs are provided in the request.
- **`GET /books/all`**: Depends on at least one Book having been created.
- **`PUT /books/{id}`**: Depends on the existence of a Book with the specified `{id}`. If default account/category IDs are updated, those entities must exist.
- **`DELETE /books/{id}`**: Depends on the existence of a Book with the specified `{id}`.
- **`PATCH /books/{id}/toggle`**: Depends on the existence of a Book with the specified `{id}`.
- **`POST /books/template`**: Depends on the existence of a Book Template (`GET /book-templates`).
- **`POST /books/copy`**: Depends on the existence of the source Book to be copied.
- **`GET /books/{id}/export`**: Depends on the existence of a Book with the specified `{id}`.

---

## 6. Book Template API

- **`GET /book-templates`**: No dependencies. These are likely system-provided templates.
- **`GET /book-templates/all`**: No dependencies.

---

## 7. Category API

- **`GET /categories`**: Depends on at least one Category having been created via `POST /categories`.
- **`GET /categories/all`**: Depends on at least one Category having been created.
- **`POST /categories`**:
    - Depends on a selected Book context.
    - Can have a self-dependency if a parent category (`pId`) is specified.
- **`PATCH /categories/{id}/toggle`**: Depends on the existence of a Category with the specified `{id}`.
- **`PUT /categories/{id}`**: Depends on the existence of a Category with the specified `{id}`.
- **`DELETE /categories/{id}`**: Depends on the existence of a Category with the specified `{id}`.

---

## 8. Currency API

- The Currency APIs appear to manage a pre-populated or externally sourced list of currencies. Most endpoints do not have dependencies on other resources within this API.
- **`PUT /currencies/{id}/rate`**: Depends on the existence of a Currency with the specified `{id}`.

---

## 9. Flow File API

- **`GET /flow-files/view`**: Depends on a file having been uploaded and associated with a balance flow via `POST /balance-flows/{id}/addFile`.
- **`DELETE /flow-files/{id}`**: Depends on the existence of a Flow File with the specified `{id}`.

---

## 10. Group API

- **`GET /groups`**: Depends on at least one Group having been created via `POST /groups`.
- **`POST /groups`**: Depends on an active user session and the existence of a Book Template (`templateId`).
- **`PUT /groups/{id}`**: Depends on the existence of a Group with the specified `{id}`.
- **`DELETE /groups/{id}`**: Depends on the existence of a Group with the specified `{id}`.
- **`POST /groups/{id}/inviteUser`**: Depends on the existence of the Group (`{id}`) and the User (`username`).
- **`POST /groups/{id}/removeUser`**: Depends on the existence of the Group (`{id}`) and the User (`userId`) being a member of that group.
- **`POST /groups/{id}/agree`**: Depends on a pending invitation for the current user to join the specified Group.
- **`POST /groups/{id}/reject`**: Depends on a pending invitation for the current user to join the specified Group.
- **`GET /groups/{id}/users`**: Depends on the existence of a Group with the specified `{id}`.

---

## 11. Note Day API

The Note Day feature appears to be self-contained and does not have strong dependencies on other major entities like Books or Accounts.

- **`POST /note-days`**: No external dependencies.
- **`GET /note-days`**: Depends on at least one Note Day being created.
- **`PUT /note-days/{id}`**: Depends on the existence of a Note Day with the specified `{id}`.
- **`DELETE /note-days/{id}`**: Depends on the existence of a Note Day with the specified `{id}`.
- **`PATCH /note-days/{id}/*`**: Depends on the existence of a Note Day with the specified `{id}`.

---

## 12. Payee API

- **`POST /payees`**: Depends on a selected Book context.
- **`GET /payees`**: Depends on at least one Payee having been created via `POST /payees`.
- **`PUT /payees/{id}`**: Depends on the existence of a Payee with the specified `{id}`.
- **`GET /payees/all`**: Depends on at least one Payee having been created.
- **`PATCH /payees/{id}/*`**: All toggle endpoints depend on the existence of a Payee with the specified `{id}`.
- **`DELETE /payees/{id}`**: Depends on the existence of a Payee with the specified `{id}`.

---

## 13. Report API

All report endpoints are for data aggregation and visualization. They depend on the existence of the data they are reporting on.

- **All `GET /reports/*` endpoints**: Depend on the creation of `balance-flow` records (`POST /balance-flows`) that contain the relevant data (e.g., expenses, incomes, categories, tags, payees).

---

## 14. Tag API

- **`GET /tags`**: Depends on at least one Tag having been created via `POST /tags`.
- **`GET /tags/all`**: Depends on at least one Tag having been created.
- **`POST /tags`**:
    - Depends on a selected Book context.
    - Can have a self-dependency if a parent tag (`pId`) is specified.
- **`PATCH /tags/{id}/*`**: All toggle endpoints depend on the existence of a Tag with the specified `{id}`.
