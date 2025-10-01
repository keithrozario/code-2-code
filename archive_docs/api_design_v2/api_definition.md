# MoneyNote API Definition

This document provides a detailed definition of the MoneyNote API endpoints.

## Authentication

Most API endpoints require authentication using a JSON Web Token (JWT). The JWT must be included in the `Authorization` header of the request, prefixed with "Bearer ".

**Request Header:**

| Name            | Description                                       | Type   | Data Type | Optionality |
| --------------- | ------------------------------------------------- | ------ | --------- | ----------- |
| Authorization   | The JWT token for authentication, prefixed with "Bearer ". | Header | String    | Mandatory   |

The following endpoints are exempt from authentication:
- `POST /login`
- `POST /register`
- `GET /version`
- `GET /book-templates/all`
- `GET /flow-files/view`

---

## User API

Handles user authentication, registration, and profile management.

### `POST /login`

Authenticates a user and returns a JWT.

**Request Body:** `LoginForm`

| Name     | Description        | Data Type | Optionality |
| -------- | ------------------ | --------- | ----------- |
| username | The user's username. | String    | Mandatory   |
| password | The user's password. | String    | Mandatory   |
| remember | If true, the token will have a longer expiration. | Boolean   | Optional    |

**Response Body:** `LoginResponse`

| Name          | Description         | Data Type |
| ------------- | ------------------- | --------- |
| accessToken   | The JWT access token. | String    |
| refreshToken  | The JWT refresh token. | String    |
| username      | The user's username.  | String    |
| remember      | True if the "remember me" option was selected. | Boolean   |

### `POST /logout`

Logs out the current user.

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `POST /register`

Registers a new user.

**Request Body:** `RegisterForm`

| Name       | Description        | Data Type | Optionality |
| ---------- | ------------------ | --------- | ----------- |
| username   | The new user's username. | String    | Mandatory   |
| password   | The new user's password. | String    | Mandatory   |
| inviteCode | The invitation code. | String    | Mandatory   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `GET /initState`

Retrieves the initial state for the current user, including user details, default book, and default group.

**Response Body:** `DataResponse<InitStateResponse>`

| Name  | Description                               | Data Type         |
| ----- | ----------------------------------------- | ----------------- |
| user  | The current user's session information.   | `UserSessionVo`   |
| book  | The user's default book session information. | `BookSessionVo`   |
| group | The user's default group session information. | `GroupSessionVo`  |

### `PATCH /setDefaultBook/{id}`

Sets the default book for the current user.

**Path Parameter:**

| Name | Description      | Data Type |
| ---- | ---------------- | --------- |
| id   | The ID of the book. | Integer   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `PATCH /setDefaultGroup/{id}`

Sets the default group for the current user.

**Path Parameter:**

| Name | Description      | Data Type |
| ---- | ---------------- | --------- |
| id   | The ID of the group. | Integer   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `PATCH /changePassword`

Changes the password for the current user.

**Request Body:** `ChangePasswordRequest`

| Name        | Description          | Data Type | Optionality |
| ----------- | -------------------- | --------- | ----------- |
| oldPassword | The user's old password. | String    | Mandatory   |
| newPassword | The user's new password. | String    | Mandatory   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `GET /bookSelect/all`

Retrieves a list of all books available to the user for selection.

**Response Body:** `DataResponse<List<SelectVo>>`

A list of objects with `value` (group-book ID) and `label` (group and book name).

### `PATCH /setDefaultGroupAndBook/{id}`

Sets the default group and book for the current user.

**Path Parameter:**

| Name | Description                         | Data Type |
| ---- | ----------------------------------- | --------- |
| id   | A string containing group and book IDs, separated by a hyphen (e.g., "1-2"). | String    |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

---

## Account API

Manages financial accounts.

### `POST /accounts`

Adds a new account.

**Request Body:** `AccountAddForm`

| Name         | Description        | Data Type    | Optionality |
| ------------ | ------------------ | ------------ | ----------- |
| type         | The account type.  | `AccountType`| Mandatory   |
| name         | The account name.  | String       | Mandatory   |
| no           | The account number. | String       | Optional    |
| balance      | The initial balance. | BigDecimal   | Mandatory   |
| include      | Whether to include in total balance. | Boolean      | Mandatory   |
| canTransferFrom | Whether transfers can be made from this account. | Boolean | Mandatory |
| canTransferTo | Whether transfers can be made to this account. | Boolean | Mandatory |
| canExpense   | Whether expenses can be recorded from this account. | Boolean | Mandatory |
| canIncome    | Whether income can be recorded to this account. | Boolean | Mandatory |
| notes        | Additional notes.  | String       | Optional    |
| currencyCode | The currency code. | String       | Mandatory   |
| creditLimit  | The credit limit for credit accounts. | BigDecimal | Optional |
| billDay      | The billing day for credit accounts. | Integer | Optional |
| apr          | The annual percentage rate. | BigDecimal | Optional |
| sort         | The sort order.    | Integer      | Optional    |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `GET /accounts`

Queries accounts based on specified criteria.

**Query Parameters:** `AccountQueryForm`

| Name         | Description        | Data Type    | Optionality |
| ------------ | ------------------ | ------------ | ----------- |
| type         | The account type.  | `AccountType`| Optional    |
| enable       | Filter by enabled status. | Boolean      | Optional    |
| name         | Filter by name.    | String       | Optional    |
| minBalance   | Minimum balance.   | Double       | Optional    |
| maxBalance   | Maximum balance.   | Double       | Optional    |
| no           | Filter by account number. | String       | Optional    |
| include      | Filter by inclusion in total balance. | Boolean | Optional |
| canExpense   | Filter by expense capability. | Boolean | Optional |
| canIncome    | Filter by income capability. | Boolean | Optional |
| canTransferFrom | Filter by transfer from capability. | Boolean | Optional |
| canTransferTo | Filter by transfer to capability. | Boolean | Optional |
| currencyCode | Filter by currency code. | String | Optional |

**Response Body:** `PageResponse<AccountDetails>`

A paginated list of account details.

### `GET /accounts/{id}`

Retrieves details for a specific account.

**Path Parameter:**

| Name | Description      | Data Type |
| ---- | ---------------- | --------- |
| id   | The ID of the account. | Integer   |

**Response Body:** `DataResponse<AccountDetails>`

Details of the specified account.

### `PUT /accounts/{id}`

Updates an existing account.

**Path Parameter:**

| Name | Description      | Data Type |
| ---- | ---------------- | --------- |
| id   | The ID of the account. | Integer   |

**Request Body:** `AccountUpdateForm`

(See `AccountAddForm` for parameter details)

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `DELETE /accounts/{id}`

Deletes an account.

**Path Parameter:**

| Name | Description      | Data Type |
| ---- | ---------------- | --------- |
| id   | The ID of the account. | Integer   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `GET /accounts/all`

Retrieves all accounts matching the given criteria (unpaginated).

**Query Parameters:** `AccountQueryForm`

(See `GET /accounts` for parameter details)

**Response Body:** `DataResponse<List<AccountDetails>>`

A list of all matching account details.

### `PATCH /accounts/{id}/toggle`

Toggles the enabled status of an account.

**Path Parameter:**

| Name | Description      | Data Type |
| ---- | ---------------- | --------- |
| id   | The ID of the account. | Integer   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

---

## Balance Flow API

Manages financial transactions (balance flows).

### `POST /balance-flows`

Adds a new balance flow.

**Request Body:** `BalanceFlowAddForm`

| Name       | Description        | Data Type    | Optionality |
| ---------- | ------------------ | ------------ | ----------- |
| book       | The ID of the book. | Integer      | Mandatory   |
| type       | The flow type.     | `FlowType`   | Mandatory   |
| title      | The title of the flow. | String       | Optional    |
| createTime | The creation timestamp. | Long         | Mandatory   |
| account    | The ID of the account. | Integer      | Optional    |
| categories | A list of category relations. | `List<CategoryRelationForm>` | Optional |
| payee      | The ID of the payee. | Integer      | Optional    |
| tags       | A set of tag IDs.  | `Set<Integer>` | Optional    |
| to         | The ID of the destination account for transfers. | Integer | Optional |
| amount     | The amount of the flow. | BigDecimal   | Optional    |
| convertedAmount | The converted amount for foreign currency transactions. | BigDecimal | Optional |
| notes      | Additional notes.  | String       | Optional    |
| confirm    | Whether the flow is confirmed. | Boolean      | Mandatory   |
| include    | Whether to include in statistics. | Boolean      | Mandatory   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `GET /balance-flows`

Queries balance flows based on specified criteria.

**Query Parameters:** `BalanceFlowQueryForm`

| Name       | Description        | Data Type    | Optionality |
| ---------- | ------------------ | ------------ | ----------- |
| book       | Filter by book ID. | Integer      | Optional    |
| type       | Filter by flow type. | `FlowType`   | Optional    |
| title      | Filter by title.   | String       | Optional    |
| minAmount  | Minimum amount.    | Double       | Optional    |
| maxAmount  | Maximum amount.    | Double       | Optional    |
| minTime    | Minimum creation time. | Long         | Optional    |
| maxTime    | Maximum creation time. | Long         | Optional    |
| account    | Filter by account ID. | Integer      | Optional    |
| payees     | Filter by payee IDs. | `Set<Integer>` | Optional    |
| categories | Filter by category IDs. | `Set<Integer>` | Optional    |
| tags       | Filter by tag IDs. | `Set<Integer>` | Optional    |
| confirm    | Filter by confirmation status. | Boolean      | Optional    |
| include    | Filter by inclusion in statistics. | Boolean      | Optional    |
| toId       | Filter by destination account ID. | Integer      | Optional    |
| notes      | Filter by notes.   | String       | Optional    |
| hasFile    | Filter by presence of attached files. | Boolean | Optional |

**Response Body:** `PageResponse<BalanceFlowDetails>`

A paginated list of balance flow details.

### `GET /balance-flows/{id}`

Retrieves details for a specific balance flow.

**Path Parameter:**

| Name | Description           | Data Type |
| ---- | --------------------- | --------- |
| id   | The ID of the balance flow. | Integer   |

**Response Body:** `DataResponse<BalanceFlowDetails>`

Details of the specified balance flow.

### `PUT /balance-flows/{id}`

Updates an existing balance flow.

**Path Parameter:**

| Name | Description           | Data Type |
| ---- | --------------------- | --------- |
| id   | The ID of the balance flow. | Integer   |

**Request Body:** `BalanceFlowAddForm`

(See `POST /balance-flows` for parameter details)

**Response Body:** `DataResponse<Integer>`

The ID of the updated balance flow.

### `DELETE /balance-flows/{id}`

Deletes a balance flow.

**Path Parameter:**

| Name | Description           | Data Type |
| ---- | --------------------- | --------- |
| id   | The ID of the balance flow. | Integer   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `GET /balance-flows/statistics`

Retrieves statistics for balance flows matching the given criteria.

**Query Parameters:** `BalanceFlowQueryForm`

(See `GET /balance-flows` for parameter details)

**Response Body:** `DataResponse<BigDecimal[]>`

An array of BigDecimals representing statistics.

### `PATCH /balance-flows/{id}/confirm`

Confirms a balance flow.

**Path Parameter:**

| Name | Description           | Data Type |
| ---- | --------------------- | --------- |
| id   | The ID of the balance flow. | Integer   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

---

## Book API

Manages financial books.

### `GET /books`

Queries books based on specified criteria.

**Query Parameters:** `BookQueryForm`

| Name   | Description        | Data Type | Optionality |
| ------ | ------------------ | --------- | ----------- |
| enable | Filter by enabled status. | Boolean   | Optional    |
| name   | Filter by name.    | String    | Optional    |

**Response Body:** `PageResponse<BookDetails>`

A paginated list of book details.

### `POST /books`

Adds a new book.

**Request Body:** `BookAddForm`

| Name            | Description        | Data Type | Optionality |
| --------------- | ------------------ | --------- | ----------- |
| name            | The book name.     | String    | Mandatory   |
| defaultCurrencyCode | The default currency code. | String | Mandatory |
| defaultExpenseAccountId | The ID of the default expense account. | Integer | Optional |
| defaultIncomeAccountId | The ID of the default income account. | Integer | Optional |
| defaultTransferFromAccountId | The ID of the default transfer from account. | Integer | Optional |
| defaultTransferToAccountId | The ID of the default transfer to account. | Integer | Optional |
| notes           | Additional notes.  | String    | Optional    |
| sort            | The sort order.    | Integer   | Optional    |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `GET /books/all`

Retrieves all books matching the given criteria (unpaginated).

**Query Parameters:** `BookQueryForm`

(See `GET /books` for parameter details)

**Response Body:** `DataResponse<List<BookDetails>>`

A list of all matching book details.

### `GET /books/{id}`

Retrieves details for a specific book.

**Path Parameter:**

| Name | Description      | Data Type |
| ---- | ---------------- | --------- |
| id   | The ID of the book. | Integer   |

**Response Body:** `DataResponse<BookDetails>`

Details of the specified book.

### `PUT /books/{id}`

Updates an existing book.

**Path Parameter:**

| Name | Description      | Data Type |
| ---- | ---------------- | --------- |
| id   | The ID of the book. | Integer   |

**Request Body:** `BookUpdateForm`

(See `BookAddForm` for parameter details)

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `DELETE /books/{id}`

Deletes a book.

**Path Parameter:**

| Name | Description      | Data Type |
| ---- | ---------------- | --------- |
| id   | The ID of the book. | Integer   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `PATCH /books/{id}/toggle`

Toggles the enabled status of a book.

**Path Parameter:**

| Name | Description      | Data Type |
| ---- | ---------------- | --------- |
| id   | The ID of the book. | Integer   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

---

## Category API

Manages transaction categories.

### `GET /categories`

Queries categories based on specified criteria.

**Query Parameters:** `CategoryQueryForm`

| Name   | Description        | Data Type      | Optionality |
| ------ | ------------------ | -------------- | ----------- |
| bookId | Filter by book ID. | Integer        | Optional    |
| type   | Filter by category type. | `CategoryType` | Optional    |
| name   | Filter by name.    | String         | Optional    |
| enable | Filter by enabled status. | Boolean        | Optional    |

**Response Body:** `DataResponse<List<CategoryDetails>>`

A list of category details, structured as a tree.

### `POST /categories`

Adds a new category.

**Request Body:** `CategoryAddForm`

| Name  | Description        | Data Type      | Optionality |
| ----- | ------------------ | -------------- | ----------- |
| type  | The category type. | `CategoryType` | Mandatory   |
| name  | The category name. | String         | Mandatory   |
| notes | Additional notes.  | String         | Optional    |
| pId   | The ID of the parent category. | Integer        | Optional    |
| sort  | The sort order.    | Integer        | Optional    |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `GET /categories/all`

Retrieves all categories matching the given criteria (unpaginated).

**Query Parameters:** `CategoryQueryForm`

(See `GET /categories` for parameter details)

**Response Body:** `DataResponse<List<CategoryDetails>>`

A list of all matching category details, structured as a tree.

### `PATCH /categories/{id}/toggle`

Toggles the enabled status of a category.

**Path Parameter:**

| Name | Description         | Data Type |
| ---- | ------------------- | --------- |
| id   | The ID of the category. | Integer   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `PUT /categories/{id}`

Updates an existing category.

**Path Parameter:**

| Name | Description         | Data Type |
| ---- | ------------------- | --------- |
| id   | The ID of the category. | Integer   |

**Request Body:** `CategoryUpdateForm`

(See `CategoryAddForm` for parameter details)

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `DELETE /categories/{id}`

Deletes a category.

**Path Parameter:**

| Name | Description         | Data Type |
| ---- | ------------------- | --------- |
| id   | The ID of the category. | Integer   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

---

## Currency API

Manages currencies and exchange rates.

### `GET /currencies/all`

Retrieves a list of all supported currencies.

**Response Body:** `DataResponse<List<CurrencyDetails>>`

A list of all currency details.

### `GET /currencies`

Queries currencies based on specified criteria.

**Query Parameters:** `CurrencyQueryForm`

| Name | Description        | Data Type | Optionality |
| ---- | ------------------ | --------- | ----------- |
| base | The base currency for rate calculation. | String    | Optional    |
| name | Filter by currency name. | String    | Optional    |

**Response Body:** `PageResponse<CurrencyDetails>`

A paginated list of currency details.

### `POST /currencies/refresh`

Refreshes currency exchange rates from a remote source.

**Response Body:** `DataResponse<Boolean>`

Indicates whether the refresh was successful.

### `GET /currencies/rate`

Retrieves the exchange rate between two currencies.

**Query Parameters:**

| Name | Description          | Data Type | Optionality |
| ---- | -------------------- | --------- | ----------- |
| from | The source currency code. | String    | Mandatory   |
| to   | The target currency code. | String    | Mandatory   |

**Response Body:** `DataResponse<BigDecimal>`

The exchange rate.

### `GET /currencies/calc`

Calculates the converted amount between two currencies.

**Query Parameters:**

| Name   | Description          | Data Type    | Optionality |
| ------ | -------------------- | ------------ | ----------- |
| from   | The source currency code. | String       | Mandatory   |
| to     | The target currency code. | String       | Mandatory   |
| amount | The amount to convert. | BigDecimal   | Mandatory   |

**Response Body:** `DataResponse<BigDecimal>`

The converted amount.

### `PUT /currencies/{id}/rate`

Updates the exchange rate for a currency.

**Path Parameter:**

| Name | Description         | Data Type |
| ---- | ------------------- | --------- |
| id   | The ID of the currency. | Integer   |

**Request Body:** `ChangeRateForm`

| Name | Description        | Data Type    | Optionality |
| ---- | ------------------ | ------------ | ----------- |
| base | The base currency. | String       | Optional    |
Indicates the success or failure of the operation.

---

## Group API

Manages user groups.

### `GET /groups`

Queries groups for the current user.

**Response Body:** `PageResponse<GroupDetails>`

A paginated list of group details.

### `POST /groups`

Adds a new group.

**Request Body:** `GroupAddForm`

| Name                | Description             | Data Type | Optionality |
| ------------------- | ----------------------- | --------- | ----------- |
| name                | The group name.         | String    | Mandatory   |
| defaultCurrencyCode | The default currency code. | String    | Mandatory   |
| notes               | Additional notes.       | String    | Optional    |
| templateId          | The ID of the book template to use. | Integer | Mandatory |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `PUT /groups/{id}`

Updates an existing group.

**Path Parameter:**

| Name | Description       | Data Type |
| ---- | ----------------- | --------- |
| id   | The ID of the group. | Integer   |

**Request Body:** `GroupUpdateForm`

| Name                | Description             | Data Type | Optionality |
| ------------------- | ----------------------- | --------- | ----------- |
| name                | The group name.         | String    | Mandatory   |
| notes               | Additional notes.       | String    | Optional    |
| defaultCurrencyCode | The default currency code. | String    | Mandatory   |
| defaultBookId       | The ID of the default book. | Integer   | Mandatory   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `DELETE /groups/{id}`

Deletes a group.

**Path Parameter:**

| Name | Description       | Data Type |
| ---- | ----------------- | --------- |
| id   | The ID of the group. | Integer   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

---

## Payee API

Manages payees.

### `POST /payees`

Adds a new payee.

**Request Body:** `PayeeAddForm`

| Name       | Description                  | Data Type | Optionality |
| ---------- | ---------------------------- | --------- | ----------- |
| name       | The payee name.              | String    | Mandatory   |
| notes      | Additional notes.            | String    | Optional    |
| canExpense | Whether the payee can be used for expenses. | Boolean | Mandatory |
| canIncome  | Whether the payee can be used for income. | Boolean | Mandatory |
| sort       | The sort order.              | Integer   | Optional    |

**Response Body:** `DataResponse`

Details of the newly created payee.

### `GET /payees`

Queries payees based on specified criteria.

**Query Parameters:** `PayeeQueryForm`

| Name       | Description        | Data Type | Optionality |
| ---------- | ------------------ | --------- | ----------- |
| bookId     | Filter by book ID. | Integer   | Optional    |
| name       | Filter by name.    | String    | Optional    |
| enable     | Filter by enabled status. | Boolean   | Optional    |
| canExpense | Filter by expense capability. | Boolean | Optional    |
| canIncome  | Filter by income capability. | Boolean | Optional    |

**Response Body:** `PageResponse<PayeeDetails>`

A paginated list of payee details.

### `PUT /payees/{id}`

Updates an existing payee.

**Path Parameter:**

| Name | Description       | Data Type |
| ---- | ----------------- | --------- |
| id   | The ID of the payee. | Integer   |

**Request Body:** `PayeeUpdateForm`

(See `PayeeAddForm` for parameter details)

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

---

## Tag API

Manages tags for transactions.

### `GET /tags`

Queries tags based on specified criteria.

**Query Parameters:** `TagQueryForm`

| Name        | Description        | Data Type | Optionality |
| ----------- | ------------------ | --------- | ----------- |
| bookId      | Filter by book ID. | Integer   | Optional    |
| name        | Filter by name.    | String    | Optional    |
| enable      | Filter by enabled status. | Boolean   | Optional    |
| canExpense  | Filter by expense capability. | Boolean   | Optional    |
| canIncome   | Filter by income capability. | Boolean   | Optional    |
| canTransfer | Filter by transfer capability. | Boolean | Optional    |

**Response Body:** `DataResponse<List<TagDetails>>`

A list of tag details, structured as a tree.

### `POST /tags`

Adds a new tag.

**Request Body:** `TagAddForm`

| Name        | Description        | Data Type | Optionality |
| ----------- | ------------------ | --------- | ----------- |
| name        | The tag name.      | String    | Mandatory   |
| notes       | Additional notes.  | String    | Optional    |
| pId         | The ID of the parent tag. | Integer   | Optional    |
| canExpense  | Whether the tag can be used for expenses. | Boolean | Mandatory |
| canIncome   | Whether the tag can be used for income. | Boolean | Mandatory |
| canTransfer | Whether the tag can be used for transfers. | Boolean | Mandatory |
| sort        | The sort order.    | Integer   | Optional    |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

---

## Report API

Provides reporting functionality.

### `GET /reports/expense-category`

Generates a report of expenses by category.

**Query Parameters:** `CategoryReportQueryForm`

(See `BalanceFlowQueryForm` for parameter details)

**Response Body:** `DataResponse<List<ChartVO>>`

A list of chart data objects.

### `GET /reports/income-category`

Generates a report of income by category.

**Query Parameters:** `CategoryReportQueryForm`

(See `BalanceFlowQueryForm` for parameter details)

**Response Body:** `DataResponse<List<ChartVO>>`

A list of chart data objects.

---

## Note Day API

Manages daily notes.

### `POST /note-days`

Adds a new note for a day.

**Request Body:** `NoteDayAddForm`

| Name       | Description        | Data Type | Optionality |
| ---------- | ------------------ | --------- | ----------- |
| title      | The title of the note. | String    | Mandatory   |
| notes      | The content of the note. | String    | Optional    |
| startDate  | The start date of the note. | Long      | Mandatory   |
| endDate    | The end date of the note. | Long      | Optional    |
| repeatType | The repeat type.   | Integer   | Mandatory   |
| interval   | The repeat interval. | Integer   | Optional    |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

### `GET /note-days`

Queries daily notes.

**Query Parameters:** `NoteDayQueryForm`

| Name  | Description      | Data Type | Optionality |
| ----- | ---------------- | --------- | ----------- |
| title | Filter by title. | String    | Optional    |

**Response Body:** `PageResponse<NoteDayDetails>`

A paginated list of note day details.

---

## Flow File API

Manages files attached to balance flows.

### `GET /flow-files/view`

Retrieves a file attached to a balance flow.

**Query Parameters:** `FlowFileViewForm`

| Name       | Description        | Data Type | Optionality |
| ---------- | ------------------ | --------- | ----------- |
| id         | The ID of the file. | Integer   | Mandatory   |
| createTime | The creation timestamp of the file. | Long | Mandatory   |

**Response Body:** `ResponseEntity<byte[]>`

The file content as a byte array.

### `DELETE /flow-files/{id}`

Deletes a file attached to a balance flow.

**Path Parameter:**

| Name | Description       | Data Type |
| ---- | ----------------- | --------- |
| id   | The ID of the file. | Integer   |

**Response Body:** `BaseResponse`

Indicates the success or failure of the operation.

---

## Book Template API

Manages book templates.

### `GET /book-templates`

Retrieves a list of available book templates.

**Response Body:** `DataResponse<List<BookTemplate>>`

A list of book templates.

### `GET /book-templates/all`

Retrieves a list of all book templates with basic details.

**Response Body:** `DataResponse<List<IdAndNameDetails>>`

A list of book templates with ID and name.

---

## Test API

Provides testing endpoints.

### `GET /version`

Retrieves the application version.

**Response Body:** `DataResponse<String>`

The application version string.
