# MoneyNote API Documentation

This document outlines the RESTful API endpoints for the MoneyNote application, based on the analysis of the provided design and user journey documents.

## Table of Contents
- [Authentication](#authentication)
- [Accounts](#accounts)
- [Balance Flows (Transactions)](#balance-flows-transactions)
- [File Attachments](#file-attachments)
- [Books](#books)
- [Categories](#categories)
- [Currencies](#currencies)
- [Reports](#reports)

---

## Authentication

### `POST /login`

Authenticates a user and returns a JWT.

**Request Body:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `username` | `string` | The user's username. |
| `password` | `string` | The user's password. |

**Response Body:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `token` | `string` | The JWT for authenticating subsequent requests. |
| `user` | `object` | User details object. |

### `POST /register`

Registers a new user.

**Request Body:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `username` | `string` | The new user's username. |
| `password` | `string` | The new user's password. |
| `email` | `string` | The new user's email. |

**Response Body:**

- Success: `200 OK` with user details.
- Error: `400 Bad Request` if username or email is taken.

---

## Accounts

### `GET /accounts`

Retrieves a paginated list of financial accounts for the user's group.

**Query Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `page` | `integer` | The page number to retrieve. |
| `size` | `integer` | The number of items per page. |
| `type` | `string` | Filter by account type (e.g., `CHECKING`, `CREDIT`). |
| `enable` | `boolean` | Filter by enabled status. |

**Response Body:**

A paginated list of `AccountDetails` objects.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `integer` | Account ID. |
| `name` | `string` | Account name. |
| `type` | `string` | Account type (`CHECKING`, `CREDIT`, `ASSET`, `DEBT`). |
| `balance` | `number` | Current account balance. |
| `currencyCode` | `string` | Currency code (e.g., "USD"). |
| `enable` | `boolean` | Whether the account is active. |
| `include` | `boolean` | Whether the account is included in net worth calculations. |
| `notes` | `string` | Optional notes. |

### `POST /accounts`

Creates a new financial account.

**Request Body:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | Name for the new account. |
| `type` | `string` | `CHECKING`, `CREDIT`, `ASSET`, or `DEBT`. |
| `currencyCode` | `string` | Currency code (e.g., "USD"). |
| `initialBalance`| `number` | The starting balance. |
| `creditLimit` | `number` | (Optional) Credit limit for `CREDIT` accounts. |
| `notes` | `string` | (Optional) Descriptive notes. |
| `include` | `boolean` | `true` to include in net worth calculations. |

**Response Body:**

The created `AccountDetails` object.

### `GET /accounts/overview`

Calculates and retrieves the user's financial overview (net worth).

**Response Body:**

An array of numbers.

| Index | Type | Description |
| :--- | :--- | :--- |
| 0 | `number` | Total Assets. |
| 1 | `number` | Total Liabilities. |
| 2 | `number` | Net Worth (Assets - Liabilities). |

### `POST /accounts/{id}/adjust`

Adjusts the balance of a specific account.

**Path Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `integer` | The ID of the account to adjust. |

**Request Body:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `balance` | `number` | The new balance for the account. |
| `createTime` | `integer` | Timestamp for when the adjustment occurred. |

**Response Body:**

- `200 OK` on success.

---

## Balance Flows (Transactions)

### `GET /balance-flows`

Retrieves a paginated list of transactions.

**Query Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `page` | `integer` | Page number. |
| `size` | `integer` | Items per page. |
| `bookId` | `integer` | Filter by book ID. |
| `minTime` | `integer` | Start of date range (Unix timestamp). |
| `maxTime` | `integer` | End of date range (Unix timestamp). |
| `type` | `string` | Filter by type (`EXPENSE`, `INCOME`, `TRANSFER`). |

**Response Body:**

A paginated list of `BalanceFlowDetails` objects.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `integer` | Transaction ID. |
| `type` | `string` | `EXPENSE`, `INCOME`, `TRANSFER`, `ADJUST`. |
| `amount` | `number` | Total transaction amount. |
| `convertedAmount`| `number` | Amount converted to the book's default currency. |
| `createTime` | `integer` | Timestamp of the transaction. |
| `title` | `string` | Optional title. |
| `notes` | `string` | Optional notes. |
| `confirm` | `boolean` | `true` if the transaction affects balances. |
| `account` | `object` | Details of the source account. |
| `to` | `object` | (For transfers) Details of the destination account. |
| `categories` | `array` | List of categories associated with the transaction. |
| `tags` | `array` | List of tags associated with the transaction. |

### `POST /balance-flows`

Creates a new transaction.

**Request Body:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `type` | `string` | `EXPENSE`, `INCOME`, or `TRANSFER`. |
| `book` | `integer` | ID of the book this transaction belongs to. |
| `createTime` | `integer` | Timestamp of the transaction. |
| `account` | `integer` | ID of the source account. |
| `to` | `integer` | (For transfers) ID of the destination account. |
| `categories` | `array` | List of category relations (`{category: integer, amount: number, convertedAmount: number}`). |
| `payee` | `integer` | (Optional) ID of the payee. |
| `tags` | `array` | (Optional) List of tag IDs. |
| `title` | `string` | (Optional) A short title. |
| `notes` | `string` | (Optional) Detailed notes. |
| `confirm` | `boolean` | If `true`, immediately updates account balance. |
| `include` | `boolean` | If `true`, includes transaction in statistics. |

**Response Body:**

The created `BalanceFlowDetails` object.

### `PUT /balance-flows/{id}`

Updates an existing transaction. Note: This is a destructive update (deletes and re-creates the record).

**Path Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `integer` | The ID of the transaction to update. |

**Request Body:**

(Same as `POST /balance-flows`, but `book`, `type`, and `confirm` cannot be changed).

**Response Body:**

The new `BalanceFlowDetails` object with a new ID.

### `DELETE /balance-flows/{id}`

Deletes a transaction.

**Path Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `integer` | The ID of the transaction to delete. |

**Response Body:**

- `200 OK` on success.

### `PATCH /balance-flows/{id}/confirm`

Confirms a previously unconfirmed transaction, triggering an update to the account balance.

**Path Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `integer` | The ID of the transaction to confirm. |

**Response Body:**

- `200 OK` on success.

---

## File Attachments

### `POST /balance-flows/{id}/addFile`

Attaches a file to a transaction.

**Path Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `integer` | The ID of the `BalanceFlow` transaction. |

**Request Body:**

- `multipart/form-data` containing the file.

**Response Body:**

A `FlowFileDetails` object.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `integer` | The file's unique ID. |
| `originalName` | `string` | The original name of the file. |
| `contentType` | `string` | The MIME type of the file. |
| `size` | `integer` | The file size in bytes. |
| `createTime` | `integer` | The upload timestamp. |

### `GET /flow-files/view`

Retrieves the content of an attached file.

**Query Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `integer` | The ID of the `FlowFile`. |
| `createTime` | `integer` | The creation timestamp of the `FlowFile` (for security). |

**Response Body:**

The raw binary data of the file with the correct `Content-Type` header.

### `DELETE /flow-files/{id}`

Deletes a file attachment.

**Path Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `integer` | The ID of the `FlowFile` to delete. |

**Response Body:**

- `200 OK` on success.

---

## Books

### `GET /books`

Retrieves a list of all books for the user's group.

**Response Body:**

A list of `BookDetails` objects.

### `POST /books`

Creates a new, empty book.

**Request Body:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | The name for the new book. |
| `defaultCurrencyCode` | `string` | The default currency for the book (e.g., "USD"). |
| `notes` | `string` | (Optional) Notes for the book. |

**Response Body:**

The created `BookDetails` object.

### `POST /books/template`

Creates a new book from a predefined template.

**Request Body:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | The name for the new book. |
| `templateId` | `integer` | The ID of the book template to use. |

**Response Body:**

The created `BookDetails` object.

### `POST /books/copy`

Creates a new book by copying the structure of an existing one.

**Request Body:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | The name for the new book. |
| `sourceId` | `integer` | The ID of the book to copy from. |

**Response Body:**

The created `BookDetails` object.

### `PUT /books/{id}`

Updates the details of a book.

**Path Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `integer` | The ID of the book to update. |

**Request Body:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | The updated name. |
| `notes` | `string` | Updated notes. |
| `defaultExpenseAccountId` | `integer` | ID of the default expense account. |
| `defaultIncomeAccountId` | `integer` | ID of the default income account. |

**Response Body:**

The updated `BookDetails` object.

### `DELETE /books/{id}`

Deletes a book if it has no transactions.

**Path Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `integer` | The ID of the book to delete. |

**Response Body:**

- `200 OK` on success.

### `GET /books/{id}/export`

Exports all transactions from a book to an Excel file.

**Path Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `integer` | The ID of the book to export. |

**Response Body:**

An `.xlsx` file download.

---

## Categories

### `GET /categories`

Retrieves a list of categories, typically filtered by book.

**Query Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `bookId` | `integer` | The ID of the book to retrieve categories for. |
| `type` | `string` | `EXPENSE` or `INCOME`. |

**Response Body:**

A list of `CategoryDetails` objects.

### `POST /categories`

Creates a new category.

**Request Body:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | The name of the new category. |
| `bookId` | `integer` | The ID of the book it belongs to. |
| `parentId` | `integer` | (Optional) The ID of the parent category for hierarchy. |
| `type` | `string` | `EXPENSE` or `INCOME`. |

**Response Body:**

The created `CategoryDetails` object.

---

## Currencies

### `GET /currencies`

Retrieves a list of supported currencies and their exchange rates.

**Query Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `base` | `string` | (Optional) The base currency to calculate rates against (e.g., "EUR"). |

**Response Body:**

A paginated list of `CurrencyDetails` objects.

### `GET /currencies/calc`

Calculates the converted value between two currencies for a given amount.

**Query Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `from` | `string` | The source currency code. |
| `to` | `string` | The target currency code. |
| `amount` | `number` | The amount to convert. |

**Response Body:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `convertedValue` | `number` | The resulting converted amount. |

### `PUT /currencies/{id}/rate`

Manually updates the exchange rate for a currency for the current session.

**Path Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `integer` | The ID of the currency to update. |

**Request Body:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `base` | `string` | The base currency for the new rate (e.g., "USD"). |
| `rate` | `number` | The new exchange rate. |

**Response Body:**

- `200 OK` on success.

### `POST /currencies/refresh`

Triggers a refresh of all exchange rates from the external API.

**Response Body:**

- `200 OK` on success.

---

## Reports

### `GET /reports/balance`

Retrieves data for visualizing the breakdown of assets and debts.

**Response Body:**

An array containing two lists of `ChartVO` objects: `[[assetChart], [debtChart]]`.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `x` | `string` | The label (account name). |
| `y` | `number` | The value (account balance). |
| `percent` | `number` | The percentage of the total. |

### `GET /reports/expense-category`

Retrieves a report of expenses aggregated by category.

**Query Parameters:**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `bookId` | `integer` | The ID of the book to report on. |
| `minTime` | `integer` | Start of date range (Unix timestamp). |
| `maxTime` | `integer` | End of date range (Unix timestamp). |

**Response Body:**

A list of `ChartVO` objects representing the expense breakdown by category.
