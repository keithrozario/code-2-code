# API Endpoint Dependencies

This document outlines the dependencies between the MoneyNote API endpoints. Understanding these dependencies is crucial for sequencing API calls correctly.

---

## User API

| Endpoint | Dependencies | Description |
| --- | --- | --- |
| `POST /login` | `POST /register` | A user must be registered before they can log in. |
| `POST /logout` | `POST /login` | A user must be logged in to log out. |
| `POST /register` | _None_ | This is a primary endpoint for user creation. |
| `GET /initState` | `POST /login`, `POST /groups`, `POST /books` | Requires an authenticated user session. It retrieves the user's default group and book, which must exist. |
| `PATCH /setDefaultBook/{id}` | `POST /login`, `POST /books` | Requires an authenticated user and an existing book to set as the default. |
| `PATCH /setDefaultGroup/{id}` | `POST /login`, `POST /groups` | Requires an authenticated user and an existing group to set as the default. |
| `PATCH /changePassword` | `POST /login` | A user must be logged in to change their password. |
| `GET /bookSelect/all` | `POST /login`, `POST /groups`, `POST /books` | Requires an authenticated user. It lists all books within their respective groups. |
| `PATCH /setDefaultGroupAndBook/{id}` | `POST /login`, `POST /groups`, `POST /books` | Requires an authenticated user and existing group and book entities. |

---

## Account API

| Endpoint | Dependencies | Description |
| --- | --- | --- |
| `POST /accounts` | `POST /login` | Requires an authenticated user to create a new account. |
| `GET /accounts` | `POST /login` | Requires an authenticated user to query accounts. |
| `GET /accounts/{id}` | `POST /login`, `POST /accounts` | Requires an authenticated user and an existing account to retrieve details. |
| `PUT /accounts/{id}` | `POST /login`, `POST /accounts` | Requires an authenticated user and an existing account to update. |
| `DELETE /accounts/{id}` | `POST /login`, `POST /accounts` | Requires an authenticated user and an existing account to delete. |
| `GET /accounts/all` | `POST /login` | Requires an authenticated user to retrieve all accounts. |
| `PATCH /accounts/{id}/toggle` | `POST /login`, `POST /accounts` | Requires an authenticated user and an existing account to toggle its status. |

---

## Balance Flow API

| Endpoint | Dependencies | Description |
| --- | --- | --- |
| `POST /balance-flows` | `POST /login`, `POST /books`, `POST /accounts`, `POST /categories`, `POST /payees`, `POST /tags` | Requires an authenticated user. A balance flow is a core transaction that links together a book, accounts, categories, payees, and tags. These entities must be created beforehand. |
| `GET /balance-flows` | `POST /login` | Requires an authenticated user to query balance flows. |
| `GET /balance-flows/{id}` | `POST /login`, `POST /balance-flows` | Requires an authenticated user and an existing balance flow to retrieve details. |
| `PUT /balance-flows/{id}` | `POST /login`, `POST /balance-flows` | Requires an authenticated user and an existing balance flow to update. It has the same entity dependencies as creating a new flow. |
| `DELETE /balance-flows/{id}` | `POST /login`, `POST /balance-flows` | Requires an authenticated user and an existing balance flow to delete. |
| `GET /balance-flows/statistics` | `POST /login` | Requires an authenticated user to generate statistics. |
| `PATCH /balance-flows/{id}/confirm` | `POST /login`, `POST /balance-flows` | Requires an authenticated user and an existing balance flow to confirm. |

---

## Book API

| Endpoint | Dependencies | Description |
| --- | --- | --- |
| `GET /books` | `POST /login` | Requires an authenticated user to query books. |
| `POST /books` | `POST /login`, `POST /accounts` | Requires an authenticated user. When creating a book, default accounts can be assigned, which must exist. |
| `GET /books/all` | `POST /login` | Requires an authenticated user to retrieve all books. |
| `GET /books/{id}` | `POST /login`, `POST /books` | Requires an authenticated user and an existing book to retrieve details. |
| `PUT /books/{id}` | `POST /login`, `POST /books`, `POST /accounts` | Requires an authenticated user and an existing book to update. |
| `DELETE /books/{id}` | `POST /login`, `POST /books` | Requires an authenticated user and an existing book to delete. |
| `PATCH /books/{id}/toggle` | `POST /login`, `POST /books` | Requires an authenticated user and an existing book to toggle its status. |

---

## Category API

| Endpoint | Dependencies | Description |
| --- | --- | --- |
| `GET /categories` | `POST /login` | Requires an authenticated user to query categories. |
| `POST /categories` | `POST /login` | Requires an authenticated user. A category can have a parent category, creating a dependency on itself. |
| `GET /categories/all` | `POST /login` | Requires an authenticated user to retrieve all categories. |
| `PATCH /categories/{id}/toggle` | `POST /login`, `POST /categories` | Requires an authenticated user and an existing category to toggle its status. |
| `PUT /categories/{id}` | `POST /login`, `POST /categories` | Requires an authenticated user and an existing category to update. |
| `DELETE /categories/{id}` | `POST /login`, `POST /categories` | Requires an authenticated user and an existing category to delete. |

---

## Currency API

| Endpoint | Dependencies | Description |
| --- | --- | --- |
| `GET /currencies/all` | _None_ | Does not require authentication. Retrieves all supported currencies. |
| `GET /currencies` | _None_ | Does not require authentication. Queries currencies. |
| `POST /currencies/refresh` | `POST /login` | Requires an authenticated user to refresh exchange rates. |
| `GET /currencies/rate` | _None_ | Does not require authentication. Retrieves an exchange rate. |
| `GET /currencies/calc` | _None_ | Does not require authentication. Calculates a currency conversion. |
| `PUT /currencies/{id}/rate` | `POST /login`, `GET /currencies/all` | Requires an authenticated user and an existing currency to update its rate. |

---

## Group API

| Endpoint | Dependencies | Description |
| --- | --- | --- |
| `GET /groups` | `POST /login` | Requires an authenticated user to query groups. |
| `POST /groups` | `POST /login`, `GET /book-templates/all` | Requires an authenticated user. Creating a group requires a book template, which must be available. |
| `PUT /groups/{id}` | `POST /login`, `POST /groups`, `POST /books` | Requires an authenticated user and an existing group to update. A default book can be set, which must exist. |
| `DELETE /groups/{id}` | `POST /login`, `POST /groups` | Requires an authenticated user and an existing group to delete. |

---

## Payee API

| Endpoint | Dependencies | Description |
| --- | --- | --- |
| `POST /payees` | `POST /login` | Requires an authenticated user to create a payee. |
| `GET /payees` | `POST /login` | Requires an authenticated user to query payees. |
| `PUT /payees/{id}` | `POST /login`, `POST /payees` | Requires an authenticated user and an existing payee to update. |

---

## Tag API

| Endpoint | Dependencies | Description |
| --- | --- | --- |
| `GET /tags` | `POST /login` | Requires an authenticated user to query tags. |
| `POST /tags` | `POST /login` | Requires an authenticated user. A tag can have a parent tag, creating a dependency on itself. |

---

## Report API

| Endpoint | Dependencies | Description |
| --- | --- | --- |
| `GET /reports/expense-category` | `POST /login`, `POST /balance-flows` | Requires an authenticated user. Generates reports based on existing balance flow data. |
| `GET /reports/income-category` | `POST /login`, `POST /balance-flows` | Requires an authenticated user. Generates reports based on existing balance flow data. |

---

## Note Day API

| Endpoint | Dependencies | Description |
| --- | --- | --- |
| `POST /note-days` | `POST /login` | Requires an authenticated user to create a daily note. |
| `GET /note-days` | `POST /login` | Requires an authenticated user to query daily notes. |

---

## Flow File API

| Endpoint | Dependencies | Description |
| --- | --- | --- |
| `GET /flow-files/view` | `POST /balance-flows` | Does not require authentication but needs a valid file ID from an existing balance flow. |
| `DELETE /flow-files/{id}` | `POST /login`, `POST /balance-flows` | Requires an authenticated user and a file associated with a balance flow to delete. |

---

## Book Template API

| Endpoint | Dependencies | Description |
| --- | --- | --- |
| `GET /book-templates` | _None_ | Does not require authentication. Retrieves book templates. |
| `GET /book-templates/all` | _None_ | Does not require authentication. Retrieves basic details for all book templates. |

---

## Test API

| Endpoint | Dependencies | Description |
| --- | --- | --- |
| `GET /version` | _None_ | Does not require authentication. Retrieves the application version. |
