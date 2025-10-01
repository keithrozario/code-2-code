# Moneynote API Documentation

This document provides a detailed description of the Moneynote API endpoints.

**Authentication:** Most endpoints require a valid JWT token to be passed in the `Authorization` header as a Bearer token.

`Authorization: Bearer <JWT_TOKEN>`

Endpoints that do not require authentication are explicitly marked.

---

## 1. Test API

Controller: `TestController`

### GET /version

Returns the application version.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Response Body**

| Name | Description         | Data type |
|------|---------------------|-----------|
| data | Application version | String    |

### GET /test3

Returns the base URL of the application.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Response Body**

| Name | Description | Data type |
|------|-------------|-----------|
| data | Base URL    | String    |

---

## 2. User API

Controller: `UserController`

### POST /login

Logs in a user and returns an access token. (No authentication required)

**Request Body**

| Name     | Description      | Data type | Optionality |
|----------|------------------|-----------|-------------|
| username | User's username  | String    | Mandatory   |
| password | User's password  | String    | Mandatory   |
| remember | Remember login   | Boolean   | Optional    |

**Response Body**

| Name         | Description        | Data type |
|--------------|--------------------|-----------|
| accessToken  | JWT access token   | String    |
| refreshToken | JWT refresh token  | String    |
| username     | User's username    | String    |
| remember     | Remember login     | Boolean   |

### POST /logout

Logs out the current user.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### POST /register

Registers a new user. (No authentication required)

**Request Body**

| Name       | Description     | Data type | Optionality |
|------------|-----------------|-----------|-------------|
| username   | Username        | String    | Mandatory   |
| password   | Password        | String    | Mandatory   |
| inviteCode | Invitation code | String    | Mandatory   |

### PUT /bind

Binds a username to the current user.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body**

| Name       | Description     | Data type | Optionality |
|------------|-----------------|-----------|-------------|
| username   | Username        | String    | Mandatory   |
| password   | Password        | String    | Mandatory   |
| inviteCode | Invitation code | String    | Mandatory   |

### GET /initState

Gets the initial state for the current user.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Response Body**

| Name  | Description      | Data type        |
|-------|------------------|------------------|
| user  | User information | UserSessionVo    |
| book  | Book information | BookSessionVo    |
| group | Group information| GroupSessionVo   |

### PATCH /setDefaultBook/{id}

Sets the default book for the current user.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Book ID     | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /setDefaultGroup/{id}

Sets the default group for the current user.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Group ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /changePassword

Changes the password for the current user.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body**

| Name          | Description     | Data type | Optionality |
|---------------|-----------------|-----------|-------------|
| oldPassword   | Old password    | String    | Mandatory   |
| newPassword   | New password    | String    | Mandatory   |

### GET /bookSelect/all

Gets all books for the current user.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /setDefaultGroupAndBook/{id}

Sets the default group and book for the current user.

**Request Path Parameters**

| Name | Description      | Data type |
|------|------------------|-----------|
| id   | Group and Book ID| String    |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

---

## 3. Account API

Controller: `AccountController`

### POST /accounts

Adds a new account.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`AccountAddForm`)**

| Name           | Description        | Data type    | Optionality |
|----------------|--------------------|--------------|-------------|
| type           | Account type       | String (Enum)| Mandatory   |
| name           | Account name       | String       | Mandatory   |
| no             | Account number     | String       | Optional    |
| balance        | Initial balance    | BigDecimal   | Mandatory   |
| include        | Include in total   | Boolean      | Mandatory   |
| canTransferFrom| Can transfer from  | Boolean      | Mandatory   |
| canTransferTo  | Can transfer to    | Boolean      | Mandatory   |
| canExpense     | Can be used for expense | Boolean | Mandatory   |
| canIncome      | Can be used for income | Boolean  | Mandatory   |
| notes          | Notes              | String       | Optional    |
| currencyCode   | Currency code      | String       | Mandatory   |
| creditLimit    | Credit limit       | BigDecimal   | Optional    |
| billDay        | Billing day        | Integer      | Optional    |
| apr            | APR                | BigDecimal   | Optional    |
| sort           | Sort order         | Integer      | Optional    |

### GET /accounts

Queries accounts.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`AccountQueryForm`)**

| Name           | Description       | Data type     | Optionality |
|----------------|-------------------|---------------|-------------|
| type           | Account type      | String (Enum) | Optional    |
| enable         | Is enabled        | Boolean       | Optional    |
| name           | Account name      | String        | Optional    |
| minBalance     | Minimum balance   | Double        | Optional    |
| maxBalance     | Maximum balance   | Double        | Optional    |
| no             | Account number    | String        | Optional    |
| include        | Include in total  | Boolean       | Optional    |
| canExpense     | Can be used for expense | Boolean | Optional    |
| canIncome      | Can be used for income | Boolean  | Optional    |
| canTransferFrom| Can transfer from | Boolean       | Optional    |
| canTransferTo  | Can transfer to   | Boolean       | Optional    |
| currencyCode   | Currency code     | String        | Optional    |
| page           | Page number       | Integer       | Optional    |
| size           | Page size         | Integer       | Optional    |
| sort           | Sort order        | String        | Optional    |

**Response Body**

A page of `AccountDetails` objects.

### GET /accounts/{id}

Gets an account by ID.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Account ID  | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Response Body (`AccountDetails`)**

| Name            | Description        | Data type    |
|-----------------|--------------------|--------------|
| id              | Account ID         | Integer      |
| name            | Account name       | String       |
| type            | Account type       | String (Enum)|
| typeName        | Account type name  | String       |
| no              | Account number     | String       |
| balance         | Balance            | BigDecimal   |
| convertedBalance| Converted balance  | BigDecimal   |
| rate            | Exchange rate      | BigDecimal   |
| enable          | Is enabled         | Boolean      |
| include         | Include in total   | Boolean      |
| canExpense      | Can be used for expense | Boolean |
| canIncome       | Can be used for income | Boolean  |
| canTransferFrom | Can transfer from  | Boolean      |
| canTransferTo   | Can transfer to    | Boolean      |
| notes           | Notes              | String       |
| currencyCode    | Currency code      | String       |
| creditLimit     | Credit limit       | BigDecimal   |
| billDay         | Billing day        | Integer      |
| apr             | APR                | BigDecimal   |
| asOfDate        | As of date         | Long         |
| sort            | Sort order         | Integer      |

### GET /accounts/statistics

Gets account statistics.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`AccountQueryForm`)**

Same as `GET /accounts`.

### PUT /accounts/{id}

Updates an account.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Account ID  | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`AccountUpdateForm`)**

| Name           | Description       | Data type    | Optionality |
|----------------|-------------------|--------------|-------------|
| name           | Account name      | String       | Optional    |
| no             | Account number    | String       | Optional    |
| notes          | Notes             | String       | Optional    |
| creditLimit    | Credit limit      | BigDecimal   | Optional    |
| billDay        | Billing day       | Integer      | Optional    |
| include        | Include in total  | Boolean      | Optional    |
| canTransferFrom| Can transfer from | Boolean      | Optional    |
| canTransferTo  | Can transfer to   | Boolean      | Optional    |
| canExpense     | Can be used for expense | Boolean | Optional    |
| canIncome      | Can be used for income | Boolean  | Optional    |
| apr            | APR               | BigDecimal   | Optional    |
| sort           | Sort order        | Integer      | Optional    |

### DELETE /accounts/{id}

Deletes an account.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Account ID  | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### GET /accounts/all

Gets all accounts.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`AccountQueryForm`)**

Same as `GET /accounts`.

**Response Body**

A list of `AccountDetails` objects.

### PATCH /accounts/{id}/toggle

Toggles the enabled state of an account.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Account ID  | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /accounts/{id}/toggleInclude

Toggles the `include` property of an account.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Account ID  | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /accounts/{id}/toggleCanExpense

Toggles the `canExpense` property of an account.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Account ID  | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /accounts/{id}/toggleCanIncome

Toggles the `canIncome` property of an account.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Account ID  | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /accounts/{id}/toggleCanTransferFrom

Toggles the `canTransferFrom` property of an account.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Account ID  | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /accounts/{id}/toggleCanTransferTo

Toggles the `canTransferTo` property of an account.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Account ID  | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### POST /accounts/{id}/adjust

Adjusts the balance of an account.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Account ID  | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`AdjustBalanceAddForm`)**

| Name       | Description   | Data type    | Optionality |
|------------|---------------|--------------|-------------|
| book       | Book ID       | Integer      | Mandatory   |
| createTime | Creation time | Long         | Mandatory   |
| title      | Title         | String       | Optional    |
| notes      | Notes         | String       | Optional    |
| balance    | New balance   | BigDecimal   | Mandatory   |

### PUT /accounts/{id}/adjust

Updates a balance adjustment.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Account ID  | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`AdjustBalanceUpdateForm`)**

| Name       | Description   | Data type | Optionality |
|------------|---------------|-----------|-------------|
| book       | Book ID       | Integer   | Optional    |
| createTime | Creation time | Long      | Mandatory   |
| title      | Title         | String    | Optional    |
| notes      | Notes         | String    | Optional    |

### GET /accounts/overview

Gets an overview of all accounts.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PUT /accounts/{id}/updateNotes

Updates the notes of an account.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Account ID  | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`AccountUpdateNotesForm`)**

| Name  | Description | Data type | Optionality |
|-------|-------------|-----------|-------------|
| notes | Notes       | String    | Optional    |

---

## 4. Balance Flow API

Controller: `BalanceFlowController`

### POST /balance-flows

Adds a new balance flow record.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`BalanceFlowAddForm`)**

| Name            | Description         | Data type      | Optionality |
|-----------------|---------------------|----------------|-------------|
| book            | Book ID             | Integer        | Mandatory   |
| type            | Flow type           | String (Enum)  | Mandatory   |
| title           | Title               | String         | Optional    |
| createTime      | Creation time       | Long           | Mandatory   |
| account         | Account ID          | Integer        | Optional    |
| categories      | List of categories  | List           | Optional    |
| payee           | Payee ID            | Integer        | Optional    |
| tags            | Set of tag IDs      | Set            | Optional    |
| to              | "To" account ID     | Integer        | Optional    |
| amount          | Amount              | BigDecimal     | Optional    |
| convertedAmount | Converted amount    | BigDecimal     | Optional    |
| notes           | Notes               | String         | Optional    |
| confirm         | Is confirmed        | Boolean        | Mandatory   |
| include         | Include in total    | Boolean        | Mandatory   |

### GET /balance-flows

Queries balance flow records.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`BalanceFlowQueryForm`)**

| Name       | Description      | Data type     | Optionality |
|------------|------------------|---------------|-------------|
| book       | Book ID          | Integer       | Optional    |
| type       | Flow type        | String (Enum) | Optional    |
| title      | Title            | String        | Optional    |
| minAmount  | Minimum amount   | Double        | Optional    |
| maxAmount  | Maximum amount   | Double        | Optional    |
| minTime    | Minimum time     | Long          | Optional    |
| maxTime    | Maximum time     | Long          | Optional    |
| account    | Account ID       | Integer       | Optional    |
| payees     | Set of payee IDs | Set           | Optional    |
| categories | Set of category IDs| Set           | Optional    |
| tags       | Set of tag IDs   | Set           | Optional    |
| confirm    | Is confirmed     | Boolean       | Optional    |
| include    | Include in total | Boolean       | Optional    |
| toId       | "To" account ID  | Integer       | Optional    |
| notes      | Notes            | String        | Optional    |
| hasFile    | Has file         | Boolean       | Optional    |
| page       | Page number      | Integer       | Optional    |
| size       | Page size        | Integer       | Optional    |
| sort       | Sort order       | String        | Optional    |

**Response Body**

A page of `BalanceFlowDetails` objects.

### GET /balance-flows/{id}

Gets a balance flow record by ID.

**Request Path Parameters**

| Name | Description        | Data type |
|------|--------------------|-----------|
| id   | Balance Flow ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Response Body (`BalanceFlowDetails`)**

| Name            | Description         | Data type      |
|-----------------|---------------------|----------------|
| book            | Book information    | BookForFlow    |
| type            | Flow type           | String (Enum)  |
| typeName        | Flow type name      | String         |
| title           | Title               | String         |
| notes           | Notes               | String         |
| createTime      | Creation time       | Long           |
| amount          | Amount              | BigDecimal     |
| convertedAmount | Converted amount    | BigDecimal     |
| account         | Account information | AccountForFlow |
| confirm         | Is confirmed        | Boolean        |
| include         | Include in total    | Boolean        |
| categories      | List of categories  | List           |
| tags            | List of tags        | List           |
| accountName     | Account name        | String         |
| categoryName    | Category name       | String         |
| to              | "To" account details| AccountDetails |
| payee           | Payee details       | IdAndNameDetails|

### PUT /balance-flows/{id}

Updates a balance flow record.

**Request Path Parameters**

| Name | Description        | Data type |
|------|--------------------|-----------|
| id   | Balance Flow ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`BalanceFlowAddForm`)**

Same as `POST /balance-flows`.

### DELETE /balance-flows/{id}

Deletes a balance flow record.

**Request Path Parameters**

| Name | Description        | Data type |
|------|--------------------|-----------|
| id   | Balance Flow ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### GET /balance-flows/statistics

Gets balance flow statistics.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`BalanceFlowQueryForm`)**

Same as `GET /balance-flows`.

### PATCH /balance-flows/{id}/confirm

Confirms a balance flow record.

**Request Path Parameters**

| Name | Description        | Data type |
|------|--------------------|-----------|
| id   | Balance Flow ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### POST /balance-flows/{id}/addFile

Adds a file to a balance flow record.

**Request Path Parameters**

| Name | Description        | Data type |
|------|--------------------|-----------|
| id   | Balance Flow ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body**

A multipart file.

### GET /balance-flows/{id}/files

Gets files for a balance flow record.

**Request Path Parameters**

| Name | Description        | Data type |
|------|--------------------|-----------|
| id   | Balance Flow ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

---

## 5. Book API

Controller: `BookController`

### GET /books

Queries books.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`BookQueryForm`)**

| Name   | Description | Data type | Optionality |
|--------|-------------|-----------|-------------|
| enable | Is enabled  | Boolean   | Optional    |
| name   | Book name   | String    | Optional    |
| page   | Page number | Integer   | Optional    |
| size   | Page size   | Integer   | Optional    |
| sort   | Sort order  | String    | Optional    |

**Response Body**

A page of `BookDetails` objects.

### GET /books/{id}

Gets a book by ID.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Book ID     | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Response Body (`BookDetails`)**

| Name                       | Description                  | Data type        |
|----------------------------|------------------------------|------------------|
| id                         | Book ID                      | Integer          |
| name                       | Book name                    | String           |
| group                      | Group information            | IdAndNameDetails |
| notes                      | Notes                        | String           |
| enable                     | Is enabled                   | Boolean          |
| defaultCurrencyCode        | Default currency code        | String           |
| defaultExpenseAccount      | Default expense account      | AccountDetails   |
| defaultIncomeAccount       | Default income account       | AccountDetails   |
| defaultTransferFromAccount | Default transfer from account| AccountDetails   |
| defaultTransferToAccount   | Default transfer to account  | AccountDetails   |
| defaultExpenseCategory     | Default expense category     | CategoryDetails  |
| defaultIncomeCategory      | Default income category      | CategoryDetails  |
| current                    | Is current book              | Boolean          |
| groupDefault               | Is group default book        | Boolean          |
| sort                       | Sort order                   | Integer          |

### POST /books

Adds a new book.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`BookAddForm`)**

| Name                       | Description                  | Data type | Optionality |
|----------------------------|------------------------------|-----------|-------------|
| name                       | Book name                    | String    | Mandatory   |
| defaultCurrencyCode        | Default currency code        | String    | Mandatory   |
| defaultExpenseAccountId      | Default expense account ID   | Integer   | Optional    |
| defaultIncomeAccountId       | Default income account ID    | Integer   | Optional    |
| defaultTransferFromAccountId | Default transfer from account ID| Integer| Optional    |
| defaultTransferToAccountId   | Default transfer to account ID| Integer  | Optional    |
| notes                      | Notes                        | String    | Optional    |
| sort                       | Sort order                   | Integer   | Optional    |

### GET /books/all

Gets all books.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`BookQueryForm`)**

Same as `GET /books`.

**Response Body**

A list of `BookDetails` objects.

### PUT /books/{id}

Updates a book.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Book ID     | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`BookUpdateForm`)**

| Name                       | Description                  | Data type | Optionality |
|----------------------------|------------------------------|-----------|-------------|
| name                       | Book name                    | String    | Optional    |
| defaultExpenseAccountId      | Default expense account ID   | Integer   | Optional    |
| defaultIncomeAccountId       | Default income account ID    | Integer   | Optional    |
| defaultTransferFromAccountId | Default transfer from account ID| Integer| Optional    |
| defaultTransferToAccountId   | Default transfer to account ID| Integer  | Optional    |
| defaultExpenseCategoryId     | Default expense category ID  | Integer   | Optional    |
| defaultIncomeCategoryId      | Default income category ID   | Integer   | Optional    |
| notes                      | Notes                        | String    | Optional    |
| sort                       | Sort order                   | Integer   | Optional    |

### DELETE /books/{id}

Deletes a book.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Book ID     | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /books/{id}/toggle

Toggles the enabled state of a book.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Book ID     | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### POST /books/template

Adds a new book from a template.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`BookAddByTemplateForm`)**

| Name       | Description    | Data type   | Optionality |
|------------|----------------|-------------|-------------|
| templateId | Template ID    | Integer     | Mandatory   |
| book       | Book details   | BookAddForm | Mandatory   |

### POST /books/copy

Adds a new book by copying an existing one.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`BookAddByBookForm`)**

| Name   | Description    | Data type   | Optionality |
|--------|----------------|-------------|-------------|
| bookId | Book ID to copy| Integer     | Mandatory   |
| book   | New book details| BookAddForm | Mandatory   |

### GET /books/{id}/export

Exports a book's data to an Excel file.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Book ID     | Integer   |

**Query Parameters**

| Name           | Description      | Data type | Optionality |
|----------------|------------------|-----------|-------------|
| timeZoneOffset | Timezone offset  | Integer   | Mandatory   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

---

## 6. Book Template API

Controller: `BookTemplateController`

### GET /book-templates

Gets all book templates.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### GET /book-templates/all

Gets all book templates as a list of ID and name.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

---

## 7. Category API

Controller: `CategoryController`

### GET /categories

Queries categories.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`CategoryQueryForm`)**

| Name   | Description    | Data type     | Optionality |
|--------|----------------|---------------|-------------|
| bookId | Book ID        | Integer       | Optional    |
| type   | Category type  | String (Enum) | Optional    |
| name   | Category name  | String        | Optional    |
| enable | Is enabled     | Boolean       | Optional    |
| page   | Page number    | Integer       | Optional    |
| size   | Page size      | Integer       | Optional    |
| sort   | Sort order     | String        | Optional    |

**Response Body**

A page of `CategoryDetails` objects.

### GET /categories/all

Gets all categories.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`CategoryQueryForm`)**

Same as `GET /categories`.

**Response Body**

A list of `CategoryDetails` objects.

### POST /categories

Adds a new category.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`CategoryAddForm`)**

| Name  | Description    | Data type     | Optionality |
|-------|----------------|---------------|-------------|
| type  | Category type  | String (Enum) | Mandatory   |
| name  | Category name  | String        | Mandatory   |
| notes | Notes          | String        | Optional    |
| pId   | Parent ID      | Integer       | Optional    |
| sort  | Sort order     | Integer       | Optional    |

### PATCH /categories/{id}/toggle

Toggles the enabled state of a category.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Category ID | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PUT /categories/{id}

Updates a category.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Category ID | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`CategoryUpdateForm`)**

| Name  | Description    | Data type | Optionality |
|-------|----------------|-----------|-------------|
| name  | Category name  | String    | Optional    |
| notes | Notes          | String    | Optional    |
| pId   | Parent ID      | Integer   | Optional    |
| sort  | Sort order     | Integer   | Optional    |

### DELETE /categories/{id}

Deletes a category.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Category ID | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

---

## 8. Currency API

Controller: `CurrencyController`

### GET /currencies/all

Gets all currencies.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### GET /currencies

Queries currencies.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`CurrencyQueryForm`)**

| Name | Description  | Data type | Optionality |
|------|--------------|-----------|-------------|
| base | Base currency| String    | Optional    |
| name | Currency name| String    | Optional    |
| page | Page number  | Integer   | Optional    |
| size | Page size    | Integer   | Optional    |

### POST /currencies/refresh

Refreshes currency rates.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### GET /currencies/rate

Gets the exchange rate between two currencies.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters**

| Name | Description      | Data type | Optionality |
|------|------------------|-----------|-------------|
| from | From currency    | String    | Mandatory   |
| to   | To currency      | String    | Mandatory   |

### GET /currencies/calc

Calculates the converted amount between two currencies.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters**

| Name   | Description      | Data type    | Optionality |
|--------|------------------|--------------|-------------|
| from   | From currency    | String       | Mandatory   |
| to     | To currency      | String       | Mandatory   |
| amount | Amount to convert| BigDecimal   | Mandatory   |

### PUT /currencies/{id}/rate

Updates the exchange rate of a currency.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Currency ID | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`ChangeRateForm`)**

| Name | Description  | Data type    | Optionality |
|------|--------------|--------------|-------------|
| base | Base currency| String       | Optional    |
| rate | Exchange rate| BigDecimal   | Optional    |

---

## 9. Flow File API

Controller: `FlowFileController`

### GET /flow-files/view

Views a flow file.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`FlowFileViewForm`)**

| Name       | Description   | Data type | Optionality |
|------------|---------------|-----------|-------------|
| id         | File ID       | Integer   | Mandatory   |
| createTime | Creation time | Long      | Mandatory   |

### DELETE /flow-files/{id}

Deletes a flow file.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | File ID     | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

---

## 10. Group API

Controller: `GroupController`

### GET /groups

Queries groups.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters**

| Name | Description | Data type | Optionality |
|------|-------------|-----------|-------------|
| page | Page number | Integer   | Optional    |
| size | Page size   | Integer   | Optional    |

### POST /groups

Adds a new group.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`GroupAddForm`)**

| Name                | Description         | Data type | Optionality |
|---------------------|---------------------|-----------|-------------|
| name                | Group name          | String    | Mandatory   |
| defaultCurrencyCode | Default currency code| String   | Mandatory   |
| notes               | Notes               | String    | Optional    |
| templateId          | Template ID         | Integer   | Mandatory   |

### PUT /groups/{id}

Updates a group.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Group ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`GroupUpdateForm`)**

| Name                | Description         | Data type | Optionality |
|---------------------|---------------------|-----------|-------------|
| name                | Group name          | String    | Mandatory   |
| notes               | Notes               | String    | Optional    |
| defaultCurrencyCode | Default currency code| String   | Mandatory   |
| defaultBookId       | Default book ID     | Integer   | Mandatory   |

### DELETE /groups/{id}

Deletes a group.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Group ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### POST /groups/{id}/inviteUser

Invites a user to a group.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Group ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`InviteUserForm`)**

| Name     | Description | Data type | Optionality |
|----------|-------------|-----------|-------------|
| username | Username    | String    | Mandatory   |

### POST /groups/{id}/removeUser

Removes a user from a group.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Group ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`RemoveUserForm`)**

| Name   | Description | Data type | Optionality |
|--------|-------------|-----------|-------------|
| userId | User ID     | Integer   | Mandatory   |

### POST /groups/{id}/agree

Agrees to a group invitation.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Group ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### POST /groups/{id}/reject

Rejects a group invitation.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Group ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### GET /groups/{id}/users

Gets all users in a group.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Group ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

---

## 11. Note Day API

Controller: `NoteDayController`

### POST /note-days

Adds a new note day.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`NoteDayAddForm`)**

| Name       | Description | Data type | Optionality |
|------------|-------------|-----------|-------------|
| title      | Title       | String    | Mandatory   |
| notes      | Notes       | String    | Optional    |
| startDate  | Start date  | Long      | Mandatory   |
| endDate    | End date    | Long      | Optional    |
| repeatType | Repeat type | Integer   | Mandatory   |
| interval   | Interval    | Integer   | Optional    |

### GET /note-days

Queries note days.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`NoteDayQueryForm`)**

| Name  | Description | Data type | Optionality |
|-------|-------------|-----------|-------------|
| title | Title       | String    | Optional    |
| page  | Page number | Integer   | Optional    |
| size  | Page size   | Integer   | Optional    |

### PUT /note-days/{id}

Updates a note day.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Note Day ID | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`NoteDayUpdateForm`)**

| Name       | Description | Data type | Optionality |
|------------|-------------|-----------|-------------|
| title      | Title       | String    | Optional    |
| notes      | Notes       | String    | Optional    |
| startDate  | Start date  | Long      | Optional    |
| endDate    | End date    | Long      | Optional    |
| repeatType | Repeat type | Integer   | Optional    |
| interval   | Interval    | Integer   | Optional    |

### DELETE /note-days/{id}

Deletes a note day.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Note Day ID | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /note-days/{id}/run

Runs a note day.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Note Day ID | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /note-days/{id}/recall

Recalls a note day.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Note Day ID | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

---

## 12. Payee API

Controller: `PayeeController`

### POST /payees

Adds a new payee.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`PayeeAddForm`)**

| Name       | Description       | Data type | Optionality |
|------------|-------------------|-----------|-------------|
| name       | Payee name        | String    | Mandatory   |
| notes      | Notes             | String    | Optional    |
| canExpense | Can be used for expense | Boolean | Mandatory   |
| canIncome  | Can be used for income | Boolean  | Mandatory   |
| sort       | Sort order        | Integer   | Optional    |

### GET /payees

Queries payees.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`PayeeQueryForm`)**

| Name       | Description       | Data type | Optionality |
|------------|-------------------|-----------|-------------|
| bookId     | Book ID           | Integer   | Optional    |
| name       | Payee name        | String    | Optional    |
| enable     | Is enabled        | Boolean   | Optional    |
| canExpense | Can be used for expense | Boolean | Optional    |
| canIncome  | Can be used for income | Boolean  | Optional    |
| page       | Page number       | Integer   | Optional    |
| size       | Page size         | Integer   | Optional    |
| sort       | Sort order        | String    | Optional    |

### PUT /payees/{id}

Updates a payee.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Payee ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`PayeeUpdateForm`)**

| Name       | Description       | Data type | Optionality |
|------------|-------------------|-----------|-------------|
| name       | Payee name        | String    | Optional    |
| notes      | Notes             | String    | Optional    |
| canExpense | Can be used for expense | Boolean | Optional    |
| canIncome  | Can be used for income | Boolean  | Optional    |
| sort       | Sort order        | Integer   | Optional    |

### GET /payees/all

Gets all payees.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`PayeeQueryForm`)**

Same as `GET /payees`.

### PATCH /payees/{id}/toggle

Toggles the enabled state of a payee.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Payee ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /payees/{id}/toggleCanExpense

Toggles the `canExpense` property of a payee.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Payee ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /payees/{id}/toggleCanIncome

Toggles the `canIncome` property of a payee.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Payee ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### DELETE /payees/{id}

Deletes a payee.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Payee ID    | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

---

## 13. Report API

Controller: `ReportController`

### GET /reports/expense-category

Gets a report of expense by category.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`CategoryReportQueryForm`)**

| Name       | Description      | Data type | Optionality |
|------------|------------------|-----------|-------------|
| book       | Book ID          | Integer   | Mandatory   |
| minTime    | Minimum time     | Long      | Optional    |
| maxTime    | Maximum time     | Long      | Optional    |
| title      | Title            | String    | Optional    |
| payees     | Set of payee IDs | Set       | Optional    |
| categories | Set of category IDs| Set       | Optional    |
| tags       | Set of tag IDs   | Set       | Optional    |
| account    | Account ID       | Integer   | Optional    |

### GET /reports/income-category

Gets a report of income by category.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`CategoryReportQueryForm`)**

Same as `GET /reports/expense-category`.

### GET /reports/expense-tag

Gets a report of expense by tag.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`CategoryReportQueryForm`)**

Same as `GET /reports/expense-category`.

### GET /reports/income-tag

Gets a report of income by tag.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`CategoryReportQueryForm`)**

Same as `GET /reports/expense-category`.

### GET /reports/expense-payee

Gets a report of expense by payee.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`BalanceFlowQueryForm`)**

Same as `GET /balance-flows`.

### GET /reports/income-payee

Gets a report of income by payee.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`BalanceFlowQueryForm`)**

Same as `GET /balance-flows`.

### GET /reports/balance

Gets a balance report.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

---

## 14. Tag API

Controller: `TagController`

### GET /tags

Queries tags.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`TagQueryForm`)**

| Name        | Description       | Data type | Optionality |
|-------------|-------------------|-----------|-------------|
| bookId      | Book ID           | Integer   | Optional    |
| name        | Tag name          | String    | Optional    |
| enable      | Is enabled        | Boolean   | Optional    |
| canExpense  | Can be used for expense | Boolean | Optional    |
| canIncome   | Can be used for income | Boolean  | Optional    |
| canTransfer | Can be used for transfer | Boolean| Optional    |
| page        | Page number       | Integer   | Optional    |
| size        | Page size         | Integer   | Optional    |
| sort        | Sort order        | String    | Optional    |

### GET /tags/all

Gets all tags.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Query Parameters (`TagQueryForm`)**

Same as `GET /tags`.

### POST /tags

Adds a new tag.

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`TagAddForm`)**

| Name        | Description       | Data type | Optionality |
|-------------|-------------------|-----------|-------------|
| name        | Tag name          | String    | Mandatory   |
| notes       | Notes             | String    | Optional    |
| pId         | Parent ID         | Integer   | Optional    |
| canExpense  | Can be used for expense | Boolean | Mandatory   |
| canIncome   | Can be used for income | Boolean  | Mandatory   |
| canTransfer | Can be used for transfer | Boolean| Mandatory   |
| sort        | Sort order        | Integer   | Optional    |

### PATCH /tags/{id}/toggle

Toggles the enabled state of a tag.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Tag ID      | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /tags/{id}/toggleCanExpense

Toggles the `canExpense` property of a tag.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Tag ID      | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /tags/{id}/toggleCanIncome

Toggles the `canIncome` property of a tag.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Tag ID      | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PATCH /tags/{id}/toggleCanTransfer

Toggles the `canTransfer` property of a tag.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Tag ID      | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

### PUT /tags/{id}

Updates a tag.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Tag ID      | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`TagUpdateForm`)**

| Name        | Description       | Data type | Optionality |
|-------------|-------------------|-----------|-------------|
| name        | Tag name          | String    | Optional    |
| notes       | Notes             | String    | Optional    |
| pId         | Parent ID         | Integer   | Optional    |
| canExpense  | Can be used for expense | Boolean | Optional    |
| canIncome   | Can be used for income | Boolean  | Optional    |
| canTransfer | Can be used for transfer | Boolean| Optional    |
| sort        | Sort order        | Integer   | Optional    |

### DELETE /tags/{id}

Deletes a tag.

**Request Path Parameters**

| Name | Description | Data type |
|------|-------------|-----------|
| id   | Tag ID      | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

---

## 15. Tag Relation API

Controller: `TagRelationController`

### PUT /tag-relations/{id}

Updates a tag relation.

**Request Path Parameters**

| Name | Description     | Data type |
|------|-----------------|-----------|
| id   | Tag Relation ID | Integer   |

**Request Headers**

| Name          | Description   | Data type | Optionality |
|---------------|---------------|-----------|-------------|
| Authorization | Bearer token  | String    | Mandatory   |

**Request Body (`TagRelationUpdateForm`)**

| Name            | Description      | Data type    | Optionality |
|-----------------|------------------|--------------|-------------|
| amount          | Amount           | BigDecimal   | Mandatory   |
| convertedAmount | Converted amount | BigDecimal   | Optional    |
