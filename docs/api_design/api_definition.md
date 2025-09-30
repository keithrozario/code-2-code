# API Documentation

This document provides a detailed specification of the MoneyNote application's API.

## Table of Contents

*   [Accounts API](#accounts-api)
*   [Balance Flow API](#balance-flow-api)
*   [Books API](#books-api)
*   [Categories API](#categories-api)
*   [Currency API](#currency-api)
*   [Files API](#files-api)
*   [Group API](#group-api)
*   [Note Day API](#note-day-api)
*   [Payee API](#payee-api)
*   [Reports API](#reports-api)
*   [Tags API](#tags-api)
*   [User and Authentication API](#user-and-authentication-api)

---

## Accounts API

The Accounts API provides endpoints for managing financial accounts.

### GET /accounts

Retrieves a paginated list of accounts based on query parameters.

**Request Parameters**

| Name | Description | Type | Data Type | Optionality |
| :--- | :--- | :--- | :--- | :--- |
| `type` | Filter by account type. | Query | String | Optional |
| `enable` | Filter by enabled status. | Query | Boolean | Optional |
| `name` | Filter by account name (contains). | Query | String | Optional |
| `minBalance` | Filter by minimum balance. | Query | Number | Optional |
| `maxBalance` | Filter by maximum balance. | Query | Number | Optional |
| `no` | Filter by account number (contains). | Query | String | Optional |
| `include` | Filter by include in net worth status. | Query | Boolean | Optional |
| `canExpense` | Filter by can be used for expenses. | Query | Boolean | Optional |
| `canIncome` | Filter by can be used for income. | Query | Boolean | Optional |
| `canTransferFrom` | Filter by can be used for transfers from. | Query | Boolean | Optional |
| `canTransferTo` | Filter by can be used for transfers to. | Query | Boolean | Optional |
| `currencyCode` | Filter by currency code. | Query | String | Optional |
| `page` | The page number to retrieve. | Query | Integer | Optional |
| `size` | The number of items per page. | Query | Integer | Optional |
| `sort` | The sorting criteria. | Query | String | Optional |

**Response Body**

A paginated list of `AccountDetails` objects.

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier for the account. | Integer |
| `name` | The name of the account. | String |
| `type` | The type of the account (`CHECKING`, `CREDIT`, `ASSET`, `DEBT`). | String |
| `typeName` | The display name of the account type. | String |
| `no` | The account number. | String |
| `balance` | The current balance of the account. | Number |
| `convertedBalance` | The balance converted to the user's default currency. | Number |
| `rate` | The exchange rate used for conversion. | Number |
| `enable` | Whether the account is enabled. | Boolean |
| `include` | Whether the account is included in net worth calculations. | Boolean |
| `canExpense` | Whether the account can be used for expenses. | Boolean |
| `canIncome` | Whether the account can be used for income. | Boolean |
| `canTransferFrom` | Whether the account can be used for transfers from. | Boolean |
| `canTransferTo` | Whether the account can be used for transfers to. | Boolean |
| `notes` | Optional notes for the account. | String |
| `currencyCode` | The currency code for the account. | String |
| `creditLimit` | The credit limit for credit accounts. | Number |
| `billDay` | The billing day of the month for credit accounts. | Integer |
| `apr` | The annual percentage rate for the account. | Number |
| `asOfDate` | The timestamp of the last balance update. | Long |
| `sort` | The sort order of the account. | Integer |
| `remainLimit` | The remaining credit limit. | Number |

### POST /accounts

Creates a new account.

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `type` | The type of the account. | String | Mandatory |
| `name` | The name of the account. | String | Mandatory |
| `no` | The account number. | String | Optional |
| `balance` | The initial balance of the account. | Number | Mandatory |
| `include` | Whether to include in net worth calculations. | Boolean | Mandatory |
| `canTransferFrom` | Whether the account can be used for transfers from. | Boolean | Mandatory |
| `canTransferTo` | Whether the account can be used for transfers to. | Boolean | Mandatory |
| `canExpense` | Whether the account can be used for expenses. | Boolean | Mandatory |
| `canIncome` | Whether the account can be used for income. | Boolean | Mandatory |
| `notes` | Optional notes for the account. | String | Optional |
| `currencyCode` | The currency code for the account. | String | Mandatory |
| `creditLimit` | The credit limit for credit accounts. | Number | Optional |
| `billDay` | The billing day of the month for credit accounts. | Integer | Optional |
| `apr` | The annual percentage rate for the account. | Number | Optional |
| `sort` | The sort order of the account. | Integer | Optional |

**Response Body**

A success message.

### GET /accounts/{id}

Retrieves the details of a specific account.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the account. | Integer |

**Response Body**

An `AccountDetails` object. See `GET /accounts` for details.

### PUT /accounts/{id}

Updates an existing account.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the account. | Integer |

**Request Body**

| Name | Description | Data-Type | Optionality |
| :--- | :--- | :--- | :--- |
| `name` | The name of the account. | String | Optional |
| `no` | The account number. | String | Optional |
| `notes` | Optional notes for the account. | String | Optional |
| `creditLimit` | The credit limit for credit accounts. | Number | Optional |
| `billDay` | The billing day of the month for credit accounts. | Integer | Optional |
| `include` | Whether to include in net worth calculations. | Boolean | Optional |
| `canTransferFrom` | Whether the account can be used for transfers from. | Boolean | Optional |
| `canTransferTo` | Whether the account can be used for transfers to. | Boolean | Optional |
| `canExpense` | Whether the account can be used for expenses. | Boolean | Optional |
| `canIncome` | Whether the account can be used for income. | Boolean | Optional |
| `apr` | The annual percentage rate for the account. | Number | Optional |
| `sort` | The sort order of the account. | Integer | Optional |

**Response Body**

A success message.

### DELETE /accounts/{id}

Deletes an account.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the account. | Integer |

**Response Body**

A success message.

### GET /accounts/all

Retrieves all accounts without pagination.

**Request Parameters**

See `GET /accounts` for query parameters.

**Response Body**

A list of `AccountDetails` objects.

### GET /accounts/overview

Retrieves an overview of the user's financial situation.

**Response Body**

An array of three numbers: `[TotalAssets, TotalLiabilities, NetWorth]`.

### GET /accounts/statistics

Retrieves statistics for accounts.

**Request Parameters**

See `GET /accounts` for query parameters.

**Response Body**

An object containing account statistics.

### POST /accounts/{id}/adjust

Adjusts the balance of an account.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the account. | Integer |

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `book` | The ID of the book this adjustment belongs to. | Integer | Mandatory |
| `createTime` | The timestamp of the adjustment. | Long | Mandatory |
| `title` | An optional title for the adjustment. | String | Optional |
| `notes` | Optional notes for the adjustment. | String | Optional |
| `balance` | The new balance of the account. | Number | Mandatory |

**Response Body**

A success message.

### PUT /accounts/{id}/adjust

Updates a balance adjustment.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the account. | Integer |

**Request Body**

The request body is an `AdjustBalanceUpdateForm`, which is not defined in the provided files. It is likely similar to `AdjustBalanceAddForm`.

**Response Body**

A success message.

### PATCH /accounts/{id}/toggle

Toggles the enabled status of an account.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the account. | Integer |

**Response Body**

A success message.

### PATCH /accounts/{id}/toggleInclude

Toggles the "include in net worth" status of an account.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the account. | Integer |

**Response Body**

A success message.

### PATCH /accounts/{id}/toggleCanExpense

Toggles the "can be used for expenses" status of an account.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the account. | Integer |

**Response Body**

A success message.

### PATCH /accounts/{id}/toggleCanIncome

Toggles the "can be used for income" status of an account.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the account. | Integer |

**Response Body**

A success message.

### PATCH /accounts/{id}/toggleCanTransferFrom

Toggles the "can be used for transfers from" status of an account.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the account. | Integer |

**Response Body**

A success message.

### PATCH /accounts/{id}/toggleCanTransferTo

Toggles the "can be used for transfers to" status of an account.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the account. | Integer |

**Response Body**

A success message.

### PUT /accounts/{id}/updateNotes

Updates the notes of an account.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the account. | Integer |

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `notes` | The new notes for the account. | String | Optional |

**Response Body**

A success message.

## Balance Flow API

The Balance Flow API is used for managing financial transactions, which are referred to as "balance flows". These can be expenses, incomes, transfers, or balance adjustments.

### GET /balance-flows

Retrieves a paginated list of balance flows based on query parameters.

**Request Parameters**

| Name | Description | Type | Data Type | Optionality |
| :--- | :--- | :--- | :--- | :--- |
| `book` | Filter by book ID. | Query | Integer | Optional |
| `type` | Filter by flow type (`EXPENSE`, `INCOME`, `TRANSFER`, `ADJUST`). | Query | String | Optional |
| `title` | Filter by title (contains). | Query | String | Optional |
| `minAmount` | Filter by minimum amount. | Query | Number | Optional |
| `maxAmount` | Filter by maximum amount. | Query | Number | Optional |
| `minTime` | Filter by minimum creation time (timestamp). | Query | Long | Optional |
| `maxTime` | Filter by maximum creation time (timestamp). | Query | Long | Optional |
| `account` | Filter by account ID (source or destination). | Query | Integer | Optional |
| `payees` | Filter by a set of payee IDs. | Query | Array[Integer] | Optional |
| `categories` | Filter by a set of category IDs. | Query | Array[Integer] | Optional |
| `tags` | Filter by a set of tag IDs. | Query | Array[Integer] | Optional |
| `confirm` | Filter by confirmed status. | Query | Boolean | Optional |
| `include` | Filter by included in statistics status. | Query | Boolean | Optional |
| `toId` | Filter by destination account ID (for transfers). | Query | Integer | Optional |
| `notes` | Filter by notes (contains). | Query | String | Optional |
| `hasFile` | Filter by whether the flow has file attachments. | Query | Boolean | Optional |
| `page` | The page number to retrieve. | Query | Integer | Optional |
| `size` | The number of items per page. | Query | Integer | Optional |
| `sort` | The sorting criteria. | Query | String | Optional |

**Response Body**

A paginated list of `BalanceFlowDetails` objects.

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier for the balance flow. | Integer |
| `book` | The book this flow belongs to. | Object |
| `type` | The type of the flow. | String |
| `typeName` | The display name of the flow type. | String |
| `title` | The title of the flow. | String |
| `notes` | Optional notes for the flow. | String |
| `createTime` | The timestamp of the flow. | Long |
| `amount` | The amount of the flow in the account's currency. | Number |
| `convertedAmount` | The amount converted to the book's default currency. | Number |
| `account` | The source account of the flow. | Object |
| `confirm` | Whether the flow is confirmed and affects balance. | Boolean |
| `include` | Whether the flow is included in statistics. | Boolean |
| `categories` | A list of categories associated with the flow. | Array[Object] |
| `tags` | A list of tags associated with the flow. | Array[Object] |
| `accountName` | The name of the source account. | String |
| `categoryName` | A comma-separated list of category names. | String |
| `to` | The destination account (for transfers). | Object |
| `payee` | The payee associated with the flow. | Object |

### POST /balance-flows

Creates a new balance flow.

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `book` | The ID of the book this flow belongs to. | Integer | Mandatory |
| `type` | The type of the flow. | String | Mandatory |
| `title` | An optional title for the flow. | String | Optional |
| `createTime` | The timestamp of the flow. | Long | Mandatory |
| `account` | The ID of the source account. | Integer | Optional |
| `categories` | A list of category relations. | Array[Object] | Optional |
| `payee` | The ID of the payee. | Integer | Optional |
| `tags` | A set of tag IDs. | Array[Integer] | Optional |
| `to` | The ID of the destination account (for transfers). | Integer | Optional |
| `amount` | The amount of the flow (for transfers and adjustments). | Number | Optional |
| `convertedAmount` | The converted amount (for transfers and adjustments). | Number | Optional |
| `notes` | Optional notes for the flow. | String | Optional |
| `confirm` | Whether the flow is confirmed. | Boolean | Mandatory |
| `include` | Whether the flow is included in statistics. | Boolean | Mandatory |

**Category Relation Object**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `category` | The ID of the category. | Integer | Mandatory |
| `amount` | The amount for this category. | Number | Mandatory |
| `convertedAmount` | The converted amount for this category. | Number | Optional |

**Response Body**

A success message.

### GET /balance-flows/{id}

Retrieves the details of a specific balance flow.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the balance flow. | Integer |

**Response Body**

A `BalanceFlowDetails` object. See `GET /balance-flows` for details.

### PUT /balance-flows/{id}

Updates an existing balance flow.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the balance flow. | Integer |

**Request Body**

The request body is the same as for `POST /balance-flows`.

**Response Body**

A `BalanceFlowDetails` object with the updated information.

### DELETE /balance-flows/{id}

Deletes a balance flow.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the balance flow. | Integer |

**Response Body**

A success message.

### GET /balance-flows/statistics

Retrieves statistics for balance flows.

**Request Parameters**

See `GET /balance-flows` for query parameters.

**Response Body**

An object containing balance flow statistics.

### PATCH /balance-flows/{id}/confirm

Confirms a balance flow.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the balance flow. | Integer |

**Response Body**

A success message.

### POST /balance-flows/{id}/addFile

Attaches a file to a balance flow.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the balance flow. | Integer |

**Request Body**

The request body should be a multipart form data with a `file` part.

**Response Body**

A `FlowFileDetails` object.

### GET /balance-flows/{id}/files

Retrieves the list of files attached to a balance flow.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the balance flow. | Integer |

**Response Body**

A list of `FlowFileDetails` objects.

## Books API

The Books API is used for managing financial books. A book is a ledger for organizing financial records.

### GET /books

Retrieves a paginated list of books based on query parameters.

**Request Parameters**

| Name | Description | Type | Data Type | Optionality |
| :--- | :--- | :--- | :--- | :--- |
| `enable` | Filter by enabled status. | Query | Boolean | Optional |
| `name` | Filter by book name (contains). | Query | String | Optional |
| `page` | The page number to retrieve. | Query | Integer | Optional |
| `size` | The number of items per page. | Query | Integer | Optional |
| `sort` | The sorting criteria. | Query | String | Optional |

**Response Body**

A paginated list of `BookDetails` objects.

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier for the book. | Integer |
| `name` | The name of the book. | String |
| `group` | The group this book belongs to. | Object |
| `notes` | Optional notes for the book. | String |
| `enable` | Whether the book is enabled. | Boolean |
| `defaultCurrencyCode` | The default currency for the book. | String |
| `defaultExpenseAccount` | The default account for expenses. | Object |
| `defaultIncomeAccount` | The default account for income. | Object |
| `defaultTransferFromAccount` | The default account for transfers from. | Object |
| `defaultTransferToAccount` | The default account for transfers to. | Object |
| `defaultExpenseCategory` | The default category for expenses. | Object |
| `defaultIncomeCategory` | The default category for income. | Object |
| `current` | Whether this is the current book for the user. | Boolean |
| `groupDefault` | Whether this is the default book for the group. | Boolean |
| `sort` | The sort order of the book. | Integer |

### POST /books

Creates a new book.

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `name` | The name of the book. | String | Mandatory |
| `defaultCurrencyCode` | The default currency for the book. | String | Mandatory |
| `defaultExpenseAccountId` | The ID of the default account for expenses. | Integer | Optional |
| `defaultIncomeAccountId` | The ID of the default account for income. | Integer | Optional |
| `defaultTransferFromAccountId` | The ID of the default account for transfers from. | Integer | Optional |
| `defaultTransferToAccountId` | The ID of the default account for transfers to. | Integer | Optional |
| `notes` | Optional notes for the book. | String | Optional |
| `sort` | The sort order of the book. | Integer | Optional |

**Response Body**

A success message.

### GET /books/all

Retrieves all books without pagination.

**Request Parameters**

See `GET /books` for query parameters.

**Response Body**

A list of `BookDetails` objects.

### GET /books/{id}

Retrieves the details of a specific book.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the book. | Integer |

**Response Body**

A `BookDetails` object. See `GET /books` for details.

### PUT /books/{id}

Updates an existing book.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the book. | Integer |

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `name` | The name of the book. | String | Optional |
| `defaultExpenseAccountId` | The ID of the default account for expenses. | Integer | Optional |
| `defaultIncomeAccountId` | The ID of the default account for income. | Integer | Optional |
| `defaultTransferFromAccountId` | The ID of the default account for transfers from. | Integer | Optional |
| `defaultTransferToAccountId` | The ID of the default account for transfers to. | Integer | Optional |
| `defaultExpenseCategoryId` | The ID of the default category for expenses. | Integer | Optional |
| `defaultIncomeCategoryId` | The ID of the default category for income. | Integer | Optional |
| `notes` | Optional notes for the book. | String | Optional |
| `sort` | The sort order of the book. | Integer | Optional |

**Response Body**

A success message.

### DELETE /books/{id}

Deletes a book.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the book. | Integer |

**Response Body**

A success message.

### PATCH /books/{id}/toggle

Toggles the enabled status of a book.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the book. | Integer |

**Response Body**

A success message.

### POST /books/template

Creates a new book from a template.

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `templateId` | The ID of the template to use. | Integer | Mandatory |
| `book` | The details of the new book. | Object | Mandatory |

**Book Object**

See `POST /books` for the structure of the `book` object.

**Response Body**

A success message.

### POST /books/copy

Creates a new book by copying an existing one.

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `bookId` | The ID of the book to copy. | Integer | Mandatory |
| `book` | The details of the new book. | Object | Mandatory |

**Book Object**

See `POST /books` for the structure of the `book` object.

**Response Body**

A success message.

### GET /books/{id}/export

Exports the balance flows of a book to an Excel file.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the book. | Integer |

**Query Parameters**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `timeZoneOffset` | The timezone offset in minutes. | Integer | Mandatory |

**Response Body**

An Excel file (`.xlsx`).

## Categories API

The Categories API is used for managing categories for financial transactions. Categories are hierarchical and can be of type expense or income.

### GET /categories

Retrieves a paginated list of categories based on query parameters.

**Request Parameters**

| Name | Description | Type | Data Type | Optionality |
| :--- | :--- | :--- | :--- | :--- |
| `bookId` | Filter by book ID. | Query | Integer | Optional |
| `type` | Filter by category type (`EXPENSE`, `INCOME`). | Query | String | Optional |
| `name` | Filter by category name (contains). | Query | String | Optional |
| `enable` | Filter by enabled status. | Query | Boolean | Optional |
| `page` | The page number to retrieve. | Query | Integer | Optional |
| `size` | The number of items per page. | Query | Integer | Optional |
| `sort` | The sorting criteria. | Query | String | Optional |

**Response Body**

A paginated list of `CategoryDetails` objects, which are tree nodes.

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier for the category. | Integer |
| `name` | The name of the category. | String |
| `pId` | The ID of the parent category. | Integer |
| `children` | A list of child categories. | Array[Object] |
| `type` | The type of the category. | String |
| `notes` | Optional notes for the category. | String |
| `enable` | Whether the category is enabled. | Boolean |
| `canExpense` | Whether the category can be used for expenses. | Boolean |
| `canIncome` | Whether the category can be used for income. | Boolean |
| `level` | The level of the category in the hierarchy. | Integer |
| `sort` | The sort order of the category. | Integer |

### GET /categories/all

Retrieves all categories without pagination, structured as a tree.

**Request Parameters**

See `GET /categories` for query parameters.

**Response Body**

A list of `CategoryDetails` objects, representing the root nodes of the category tree.

### POST /categories

Creates a new category.

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `type` | The type of the category. | String | Mandatory |
| `name` | The name of the category. | String | Mandatory |
| `notes` | Optional notes for the category. | String | Optional |
| `pId` | The ID of the parent category. | Integer | Optional |
| `sort` | The sort order of the category. | Integer | Optional |

**Response Body**

A success message.

### PATCH /categories/{id}/toggle

Toggles the enabled status of a category.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the category. | Integer |

**Response Body**

A success message.

### PUT /categories/{id}

Updates an existing category.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the category. | Integer |

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `name` | The name of the category. | String | Optional |
| `notes` | Optional notes for the category. | String | Optional |
| `pId` | The ID of the parent category. | Integer | Optional |
| `sort` | The sort order of the category. | Integer | Optional |

**Response Body**

A success message.

### DELETE /categories/{id}

Deletes a category.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the category. | Integer |

**Response Body**

A success message.

## Currency API

The Currency API is used for managing currencies and exchange rates.

### GET /currencies

Retrieves a paginated list of currencies.

**Request Parameters**

| Name | Description | Type | Data Type | Optionality |
| :--- | :--- | :--- | :--- | :--- |
| `base` | The base currency for calculating exchange rates. | Query | String | Optional |
| `name` | Filter by currency name (contains). | Query | String | Optional |
| `page` | The page number to retrieve. | Query | Integer | Optional |
| `size` | The number of items per page. | Query | Integer | Optional |

**Response Body**

A paginated list of `CurrencyDetails` objects.

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier for the currency. | Integer |
| `name` | The name of the currency (e.g., "USD"). | String |
| `description` | The description of the currency. | String |
| `rate` | The exchange rate against the system's base currency (USD). | Number |
| `rate2` | The exchange rate against the specified `base` currency. | Number |

### GET /currencies/all

Retrieves all supported currencies without pagination.

**Response Body**

A list of `CurrencyDetails` objects.

### POST /currencies/refresh

Refreshes the exchange rates from an external API.

**Response Body**

A boolean indicating if the refresh was successful.

### GET /currencies/rate

Calculates the exchange rate between two currencies.

**Request Parameters**

| Name | Description | Type | Data Type | Optionality |
| :--- | :--- | :--- | :--- | :--- |
| `from` | The source currency code. | Query | String | Mandatory |
| `to` | The target currency code. | Query | String | Mandatory |

**Response Body**

The exchange rate as a number.

### GET /currencies/calc

Calculates the converted amount between two currencies.

**Request Parameters**

| Name | Description | Type | Data Type | Optionality |
| :--- | :--- | :--- | :--- | :--- |
| `from` | The source currency code. | Query | String | Mandatory |
| `to` | The target currency code. | Query | String | Mandatory |
| `amount` | The amount to convert. | Query | Number | Mandatory |

**Response Body**

The converted amount as a number.

### PUT /currencies/{id}/rate

Updates the exchange rate of a currency. This change is not persistent and will be lost on application restart.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the currency. | Integer |

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `base` | The base currency for the new rate. | String | Optional |
| `rate` | The new exchange rate. | Number | Optional |

**Response Body**

A success message.

## Files API

The Files API is used for managing files attached to balance flows.

### GET /flow-files/view

Retrieves the content of a file.

**Request Parameters**

| Name | Description | Type | Data Type | Optionality |
| :--- | :--- | :--- | :--- | :--- |
| `id` | The unique identifier of the file. | Query | Integer | Mandatory |
| `createTime` | The creation timestamp of the file. Used for authorization. | Query | Long | Mandatory |

**Response Body**

The binary content of the file.

### DELETE /flow-files/{id}

Deletes a file.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the file. | Integer |

**Response Body**

A success message.

## Group API

The Group API is used for managing groups. A group is a collection of users who can collaborate on financial books.

### GET /groups

Retrieves a paginated list of groups for the current user.

**Request Parameters**

| Name | Description | Type | Data Type | Optionality |
| :--- | :--- | :--- | :--- | :--- |
| `page` | The page number to retrieve. | Query | Integer | Optional |
| `size` | The number of items per page. | Query | Integer | Optional |

**Response Body**

A paginated list of `GroupDetails` objects.

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier for the group. | Integer |
| `name` | The name of the group. | String |
| `notes` | Optional notes for the group. | String |
| `enable` | Whether the group is enabled. | Boolean |
| `defaultCurrencyCode` | The default currency for the group. | String |
| `role` | The role of the current user in the group. | String |
| `current` | Whether this is the current group for the user. | Boolean |
| `roleId` | The ID of the user's role in the group. | Integer |
| `defaultBook` | The default book for the group. | Object |

### POST /groups

Creates a new group.

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `name` | The name of the group. | String | Mandatory |
| `defaultCurrencyCode` | The default currency for the group. | String | Mandatory |
| `notes` | Optional notes for the group. | String | Optional |
| `templateId` | The ID of the book template to use for the default book. | Integer | Mandatory |

**Response Body**

A success message.

### PUT /groups/{id}

Updates an existing group.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the group. | Integer |

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `name` | The name of the group. | String | Mandatory |
| `notes` | Optional notes for the group. | String | Optional |
| `defaultCurrencyCode` | The default currency for the group. | String | Mandatory |
| `defaultBookId` | The ID of the default book for the group. | Integer | Mandatory |

**Response Body**

A success message.

### DELETE /groups/{id}

Deletes a group.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the group. | Integer |

**Response Body**

A success message.

### POST /groups/{id}/inviteUser

Invites a user to a group.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the group. | Integer |

**Request Body**

The request body is an `InviteUserForm`, which is not defined in the provided files. It likely contains the user's email or username.

**Response Body**

A success message.

### POST /groups/{id}/removeUser

Removes a user from a group.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the group. | Integer |

**Request Body**

The request body is a `RemoveUserForm`, which is not defined in the provided files. It likely contains the ID of the user to remove.

**Response Body**

A success message.

### POST /groups/{id}/agree

Agrees to join a group after being invited.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the group. | Integer |

**Response Body**

A success message.

### POST /groups/{id}/reject

Rejects an invitation to join a group.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the group. | Integer |

**Response Body**

A success message.

### GET /groups/{id}/users

Retrieves the list of users in a group.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the group. | Integer |

**Response Body**

A list of user objects.

## Note Day API

The Note Day API is used for managing "note days", which are recurring events or reminders.

### GET /note-days

Retrieves a paginated list of note days.

**Request Parameters**

| Name | Description | Type | Data Type | Optionality |
| :--- | :--- | :--- | :--- | :--- |
| `title` | Filter by title (contains). | Query | String | Optional |
| `page` | The page number to retrieve. | Query | Integer | Optional |
| `size` | The number of items per page. | Query | Integer | Optional |

**Response Body**

A paginated list of `NoteDayDetails` objects.

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier for the note day. | Integer |
| `title` | The title of the note day. | String |
| `notes` | Optional notes for the note day. | String |
| `startDate` | The start date of the note day (timestamp). | Long |
| `endDate` | The end date of the note day (timestamp). | Long |
| `repeatType` | The repeat type (0: once, 1: daily, 2: monthly, 3: yearly). | Integer |
| `interval` | The interval for repeating. | Integer |
| `repeatDescription` | A description of the repeat rule. | String |
| `countDown` | The number of days until the next occurrence. | Long |
| `nextDate` | The timestamp of the next occurrence. | Long |
| `totalCount` | The total number of occurrences. | Integer |
| `runCount` | The number of times the event has occurred. | Integer |
| `remainCount` | The number of remaining occurrences. | Integer |

### POST /note-days

Creates a new note day.

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `title` | The title of the note day. | String | Mandatory |
| `notes` | Optional notes for the note day. | String | Optional |
| `startDate` | The start date of the note day (timestamp). | Long | Mandatory |
| `endDate` | The end date of the note day (timestamp). | Long | Optional |
| `repeatType` | The repeat type. | Integer | Mandatory |
| `interval` | The interval for repeating. | Integer | Optional |

**Response Body**

A success message.

### PUT /note-days/{id}

Updates an existing note day.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the note day. | Integer |

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `title` | The title of the note day. | String | Optional |
| `notes` | Optional notes for the note day. | String | Optional |
| `startDate` | The start date of the note day (timestamp). | Long | Optional |
| `endDate` | The end date of the note day (timestamp). | Long | Optional |
| `repeatType` | The repeat type. | Integer | Optional |
| `interval` | The interval for repeating. | Integer | Optional |

**Response Body**

A success message.

### DELETE /note-days/{id}

Deletes a note day.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the note day. | Integer |

**Response Body**

A success message.

### PATCH /note-days/{id}/run

Marks a note day as "run" for the current period.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the note day. | Integer |

**Response Body**

A success message.

### PATCH /note-days/{id}/recall

Recalls a "run" note day.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the note day. | Integer |

**Response Body**

A success message.

## Payee API

The Payee API is used for managing payees. A payee is a person or organization that you pay money to or receive money from.

### GET /payees

Retrieves a paginated list of payees based on query parameters.

**Request Parameters**

| Name | Description | Type | Data Type | Optionality |
| :--- | :--- | :--- | :--- | :--- |
| `bookId` | Filter by book ID. | Query | Integer | Optional |
| `name` | Filter by payee name (contains). | Query | String | Optional |
| `enable` | Filter by enabled status. | Query | Boolean | Optional |
| `canExpense` | Filter by can be used for expenses. | Query | Boolean | Optional |
| `canIncome` | Filter by can be used for income. | Query | Boolean | Optional |
| `page` | The page number to retrieve. | Query | Integer | Optional |
| `size` | The number of items per page. | Query | Integer | Optional |
| `sort` | The sorting criteria. | Query | String | Optional |

**Response Body**

A paginated list of `PayeeDetails` objects.

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier for the payee. | Integer |
| `name` | The name of the payee. | String |
| `notes` | Optional notes for the payee. | String |
| `enable` | Whether the payee is enabled. | Boolean |
| `canExpense` | Whether the payee can be used for expenses. | Boolean |
| `canIncome` | Whether the payee can be used for income. | Boolean |
| `sort` | The sort order of the payee. | Integer |

### POST /payees

Creates a new payee.

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `name` | The name of the payee. | String | Mandatory |
| `notes` | Optional notes for the payee. | String | Optional |
| `canExpense` | Whether the payee can be used for expenses. | Boolean | Mandatory |
| `canIncome` | Whether the payee can be used for income. | Boolean | Mandatory |
| `sort` | The sort order of the payee. | Integer | Optional |

**Response Body**

A `PayeeDetails` object for the newly created payee.

### GET /payees/all

Retrieves all payees without pagination.

**Request Parameters**

See `GET /payees` for query parameters.

**Response Body**

A list of `PayeeDetails` objects.

### PUT /payees/{id}

Updates an existing payee.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the payee. | Integer |

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `name` | The name of the payee. | String | Optional |
| `notes` | Optional notes for the payee. | String | Optional |
| `canExpense` | Whether the payee can be used for expenses. | Boolean | Optional |
| `canIncome` | Whether the payee can be used for income. | Boolean | Optional |
| `sort` | The sort order of the payee. | Integer | Optional |

**Response Body**

A success message.

### DELETE /payees/{id}

Deletes a payee.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the payee. | Integer |

**Response Body**

A success message.

### PATCH /payees/{id}/toggle

Toggles the enabled status of a payee.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the payee. | Integer |

**Response Body**

A success message.

### PATCH /payees/{id}/toggleCanExpense

Toggles the "can be used for expenses" status of a payee.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the payee. | Integer |

**Response Body**

A success message.

### PATCH /payees/{id}/toggleCanIncome

Toggles the "can be used for income" status of a payee.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the payee. | Integer |

**Response Body**

A success message.

## Reports API

The Report API is used for generating various financial reports.

### GET /reports/expense-category

Generates a report of expenses by category.

**Request Parameters**

| Name | Description | Type | Data Type | Optionality |
| :--- | :--- | :--- | :--- | :--- |
| `book` | The ID of the book to generate the report for. | Query | Integer | Mandatory |
| `minTime` | The minimum creation time (timestamp). | Query | Long | Optional |
| `maxTime` | The maximum creation time (timestamp). | Query | Long | Optional |
| `title` | Filter by title (contains). | Query | String | Optional |
| `payees` | Filter by a set of payee IDs. | Query | Array[Integer] | Optional |
| `categories` | Filter by a set of category IDs. | Query | Array[Integer] | Optional |
| `tags` | Filter by a set of tag IDs. | Query | Array[Integer] | Optional |
| `account` | Filter by account ID. | Query | Integer | Optional |

**Response Body**

A list of objects, each containing category information and the total amount for that category.

### GET /reports/income-category

Generates a report of incomes by category.

**Request Parameters**

See `GET /reports/expense-category` for request parameters.

**Response Body**

A list of objects, each containing category information and the total amount for that category.

### GET /reports/expense-tag

Generates a report of expenses by tag.

**Request Parameters**

See `GET /reports/expense-category` for request parameters.

**Response Body**

A list of objects, each containing tag information and the total amount for that tag.

### GET /reports/income-tag

Generates a report of incomes by tag.

**Request Parameters**

See `GET /reports/expense-category` for request parameters.

**Response Body**

A list of objects, each containing tag information and the total amount for that tag.

### GET /reports/expense-payee

Generates a report of expenses by payee.

**Request Parameters**

The request parameters are the same as for `GET /balance-flows`.

**Response Body**

A list of objects, each containing payee information and the total amount for that payee.

### GET /reports/income-payee

Generates a report of incomes by payee.

**Request Parameters**

The request parameters are the same as for `GET /balance-flows`.

**Response Body**

A list of objects, each containing payee information and the total amount for that payee.

### GET /reports/balance

Generates a balance report, showing total assets and liabilities.

**Response Body**

An object containing two lists: `assets` and `debts`. Each list contains objects with account information and the balance.

## Tags API

The Tags API is used for managing tags for financial transactions. Tags are hierarchical and can be used to categorize transactions in a flexible way.

### GET /tags

Retrieves a paginated list of tags based on query parameters.

**Request Parameters**

| Name | Description | Type | Data Type | Optionality |
| :--- | :--- | :--- | :--- | :--- |
| `bookId` | Filter by book ID. | Query | Integer | Optional |
| `name` | Filter by tag name (contains). | Query | String | Optional |
| `enable` | Filter by enabled status. | Query | Boolean | Optional |
| `canExpense` | Filter by can be used for expenses. | Query | Boolean | Optional |
| `canIncome` | Filter by can be used for income. | Query | Boolean | Optional |
| `canTransfer` | Filter by can be used for transfers. | Query | Boolean | Optional |
| `page` | The page number to retrieve. | Query | Integer | Optional |
| `size` | The number of items per page. | Query | Integer | Optional |
| `sort` | The sorting criteria. | Query | String | Optional |

**Response Body**

A paginated list of `TagDetails` objects, which are tree nodes.

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier for the tag. | Integer |
| `name` | The name of the tag. | String |
| `pId` | The ID of the parent tag. | Integer |
| `children` | A list of child tags. | Array[Object] |
| `notes` | Optional notes for the tag. | String |
| `enable` | Whether the tag is enabled. | Boolean |
| `canExpense` | Whether the tag can be used for expenses. | Boolean |
| `canIncome` | Whether the tag can be used for income. | Boolean |
| `canTransfer` | Whether the tag can be used for transfers. | Boolean |
| `level` | The level of the tag in the hierarchy. | Integer |
| `sort` | The sort order of the tag. | Integer |

### GET /tags/all

Retrieves all tags without pagination, structured as a tree.

**Request Parameters**

See `GET /tags` for query parameters.

**Response Body**

A list of `TagDetails` objects, representing the root nodes of the tag tree.

### POST /tags

Creates a new tag.

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `name` | The name of the tag. | String | Mandatory |
| `notes` | Optional notes for the tag. | String | Optional |
| `pId` | The ID of the parent tag. | Integer | Optional |
| `canExpense` | Whether the tag can be used for expenses. | Boolean | Mandatory |
| `canIncome` | Whether the tag can be used for income. | Boolean | Mandatory |
| `canTransfer` | Whether the tag can be used for transfers. | Boolean | Mandatory |
| `sort` | The sort order of the tag. | Integer | Optional |

**Response Body**

A success message.

### PUT /tags/{id}

Updates an existing tag.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the tag. | Integer |

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `name` | The name of the tag. | String | Optional |
| `notes` | Optional notes for the tag. | String | Optional |
| `pId` | The ID of the parent tag. | Integer | Optional |
| `canExpense` | Whether the tag can be used for expenses. | Boolean | Optional |
| `canIncome` | Whether the tag can be used for income. | Boolean | Optional |
| `canTransfer` | Whether the tag can be used for transfers. | Boolean | Optional |
| `sort` | The sort order of the tag. | Integer | Optional |

**Response Body**

A success message.

### DELETE /tags/{id}

Deletes a tag.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the tag. | Integer |

**Response Body**

A success message.

### PATCH /tags/{id}/toggle

Toggles the enabled status of a tag.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the tag. | Integer |

**Response Body**

A success message.

### PATCH /tags/{id}/toggleCanExpense

Toggles the "can be used for expenses" status of a tag.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the tag. | Integer |

**Response Body**

A success message.

### PATCH /tags/{id}/toggleCanIncome

Toggles the "can be used for income" status of a tag.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the tag. | Integer |

**Response Body**

A success message.

### PATCH /tags/{id}/toggleCanTransfer

Toggles the "can be used for transfers" status of a tag.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the tag. | Integer |

**Response Body**

A success message.

## User and Authentication API

The User and Authentication API is used for managing users, authentication, and user-specific settings.

### POST /login

Logs in a user and returns an access token.

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `username` | The username of the user. | String | Mandatory |
| `password` | The password of the user. | String | Mandatory |

**Response Body**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `accessToken` | The access token for the user. | String |
| `user` | The details of the logged-in user. | Object |

**Response Headers**

| Name | Description |
| :--- | :--- |
| `Set-Cookie` | Sets the `accessToken` in a session cookie. |

### POST /logout

Logs out the current user.

**Response Body**

A success message.

### POST /register

Registers a new user.

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `username` | The username for the new user. | String | Mandatory |
| `password` | The password for the new user. | String | Mandatory |
| `nickName` | The nickname for the new user. | String | Mandatory |

**Response Body**

A success message.

### PUT /bind

Binds a username to an existing account (e.g., for social logins).

**Request Body**

The request body is a `RegisterForm`, which is not defined in the provided files. It is likely similar to `UserRegisterForm`.

**Response Body**

A success message.

### GET /initState

Retrieves the initial state for the current user, including user details, groups, books, etc.

**Response Body**

An object containing the user's initial state.

### PATCH /setDefaultBook/{id}

Sets the default book for the current user.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the book. | Integer |

**Response Body**

A success message.

### PATCH /setDefaultGroup/{id}

Sets the default group for the current user.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | The unique identifier of the group. | Integer |

**Response Body**

A success message.

### PATCH /setDefaultGroupAndBook/{id}

Sets the default group and book for the current user. The ID is a string in the format `groupId-bookId`.

**Path Parameters**

| Name | Description | Data Type |
| :--- | :--- | :--- |
| `id` | A string containing the group and book IDs. | String |

**Response Body**

A success message.

### PATCH /changePassword

Changes the password for the current user.

**Request Body**

| Name | Description | Data Type | Optionality |
| :--- | :--- | :--- | :--- |
| `oldPassword` | The user's current password. | String | Mandatory |
| `newPassword` | The user's new password. | String | Mandatory |

**Response Body**

A success message.

### GET /bookSelect/all

Retrieves a list of all books for the current user, formatted for a select/dropdown component.

**Response Body**

A list of book objects.
