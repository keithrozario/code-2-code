Of course, I will start by analyzing the controllers to identify the API endpoints. Then, I will examine the request and response objects associated with each endpoint to provide a detailed breakdown of their parameters.

I will begin by searching for all files ending with the name `Controller.java` within the directory `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api`.Okay, I have the controller files. I'll read them to find API endpoints and their request/response objects, starting with `AccountController.java`.I have `AccountController.java`'s content. Now, I'll find and analyze the definitions of `AccountAddForm`, `AccountQueryForm`, `AccountUpdateForm`, `AdjustBalanceAddForm`, `AdjustBalanceUpdateForm`, `AccountUpdateNotesForm`, `AccountDetails`, `PageResponse`, `DataResponse`, and `BaseResponse` to understand their structure, starting with the `Form` objects. I'll begin by searching for their corresponding files.Okay, I have the file paths for the `Form` and `Details` objects. I'll now use `read_many_files` to read their contents and understand their structure. The files are: `AccountAddForm.java`, `AccountQueryForm.java`, `AccountUpdateForm.java`, `AccountUpdateNotesForm.java`, `AdjustBalanceAddForm.java`, `AdjustBalanceUpdateForm.java`, and `AccountDetails.java`, all located under `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/account/`.
I've analyzed the `AccountController` and its related objects, documenting each endpoint, request, and response in detail. Now, I'm moving on to the `BalanceFlowController.java`.I have `BalanceFlowController.java`'s content. I need to understand its request/response objects: `BalanceFlowAddForm`, `BalanceFlowQueryForm`, and `BalanceFlowDetails` (likely from `balanceFlowService.get(id)`). I'll start by reading the `Form` class files to analyze their fields.Okay, I have the file paths for the `Form` and `Details` objects. I'll use `read_many_files` to read the contents of `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/balanceflow/BalanceFlowAddForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/balanceflow/BalanceFlowQueryForm.java`, and `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/balanceflow/BalanceFlowDetails.java` to understand their structure.
I have analyzed the `BalanceFlowController` and its related objects.

Now, I will proceed with the next controller, `BookController.java`.I have `BookController.java`'s content and need to understand its request/response objects: `BookQueryForm`, `BookAddForm`, `BookUpdateForm`, `BookAddByTemplateForm`, `BookAddByBookForm`, and `BookDetails`. I'll start by finding and reading the `Form` class files to analyze their fields.Okay, I have the file paths for the `Form` and `Details` objects. I'll use `read_many_files` to read the contents of `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/book/BookAddByBookForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/book/BookAddByTemplateForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/book/BookAddForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/book/BookQueryForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/book/BookUpdateForm.java`, and `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/book/BookDetails.java` to understand their structure.
I have analyzed the `BookController` and its related objects.

Now, I will proceed with the next controller, `CategoryController.java`.I have `CategoryController.java`'s content. I need to understand its request/response objects: `CategoryQueryForm`, `CategoryAddForm`, `CategoryUpdateForm`, and `CategoryDetails`. I'll start by finding and reading the `Form` class files to analyze their fields.Okay, I have the file paths for the `Form` and `Details` objects. I'll use `read_many_files` to read the contents of `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/category/CategoryAddForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/category/CategoryQueryForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/category/CategoryUpdateForm.java`, and `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/category/CategoryDetails.java` to understand their structure.
I have analyzed the `CategoryController` and its related objects.

Now, I will proceed with the next controller, `CurrencyController.java`.I have `CurrencyController.java`'s content. I need to understand its request/response objects: `CurrencyQueryForm`, `ChangeRateForm`, and `CurrencyDetails`. I'll start by finding and reading the `Form` class files to analyze their fields.Okay, I have the file paths for the `Form` and `Details` objects. I'll use `read_many_files` to read the contents of `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/currency/ChangeRateForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/currency/CurrencyQueryForm.java`, and `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/currency/CurrencyDetails.java` to understand their structure.
I have analyzed the `CurrencyController` and its related objects.

Now, I will proceed with the next controller, `GroupController.java`.I have `GroupController.java`'s content. I need to understand its request/response objects: `GroupAddForm`, `GroupUpdateForm`, `InviteUserForm`, `RemoveUserForm`, `GroupDetails`, and `GroupUserDetails`. I'll start by finding and reading the `Form` class files to analyze their fields.Okay, I have the file paths for the `Form` and `Details` objects. I'll use `read_many_files` to read the contents of `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/group/GroupAddForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/group/GroupUpdateForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/group/InviteUserForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/group/RemoveUserForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/group/GroupDetails.java`, and `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/group/GroupUserDetails.java` to understand their structure.
I have analyzed the `GroupController` and its related objects.

Now, I will proceed with the next controller, `PayeeController.java`.I have `PayeeController.java`'s content. I need to understand its request/response objects: `PayeeAddForm`, `PayeeQueryForm`, `PayeeUpdateForm`, and `PayeeDetails`. I'll start by finding and reading the `Form` class files to analyze their fields.Okay, I have the file paths for the `Form` and `Details` objects. I'll use `read_many_files` to read the contents of `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/payee/PayeeAddForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/payee/PayeeQueryForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/payee/PayeeUpdateForm.java`, and `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/payee/PayeeDetails.java` to understand their structure.
I have analyzed the `PayeeController` and its related objects.

Now, I will proceed with the next controller, `TagController.java`.I have `TagController.java`'s content. I need to understand its request/response objects: `TagQueryForm`, `TagAddForm`, `TagUpdateForm`, and `TagDetails`. I'll start by finding and reading the `Form` class files to analyze their fields.Okay, I have the file paths for the `Form` and `Details` objects. I'll use `read_many_files` to read the contents of `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/tag/TagAddForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/tag/TagQueryForm.java`, `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/tag/TagUpdateForm.java`, and `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/tag/TagDetails.java` to understand their structure.
I have analyzed the `TagController` and its related objects.

Now, I will proceed with the next controller, `UserController.java`.I have `UserController.java`'s content. I need to understand its request/response objects: `LoginForm`, `RegisterForm`, `ChangePasswordRequest`, `LoginResult`, `InitState`, and `BookSelect`. I'll start by finding and reading the `Form` class files to analyze their fields.`LoginResult.java`, `InitState.java`, and `BookSelect.java` are missing. I'll check `UserService.java` for them. I'll also read `LoginForm.java`, `RegisterForm.java`, `ChangePasswordRequest.java`, and `UserService.java` using `read_many_files`.
I have analyzed the `UserController` and its related objects. I found the definitions of `LoginResponse` and `InitStateResponse` inside `UserService.java`.

I will now present the final analysis of all the controllers.

I've completed the analysis of all the controllers and their related request/response objects. Here is the detailed breakdown:

## Account API

This API manages financial accounts, allowing users to create, retrieve, update, and delete accounts. It also supports balance adjustments and provides an overview of account statistics.

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| POST | /accounts | Adds a new financial account. |
| GET | /accounts | Queries a paginated list of accounts based on specified criteria. |
| GET | /accounts/{id} | Retrieves the details of a specific account by its ID. |
| GET | /accounts/statistics | Retrieves statistical data for accounts matching the query criteria. |
| PUT | /accounts/{id} | Updates the details of an existing account. |
| DELETE | /accounts/{id} | Removes an account. |
| GET | /accounts/all | Retrieves all accounts matching the query criteria, without pagination. |
| PATCH | /accounts/{id}/toggle | Toggles the enabled/disabled state of an account. |
| PATCH | /accounts/{id}/toggleInclude | Toggles whether the account is included in financial summaries. |
| PATCH | /accounts/{id}/toggleCanExpense | Toggles whether the account can be used for expenses. |
| PATCH | /accounts/{id}/toggleCanIncome | Toggles whether the account can be used for income. |
| PATCH | /accounts/{id}/toggleCanTransferFrom | Toggles whether transfers can be made from this account. |
| PATCH | /accounts/{id}/toggleCanTransferTo | Toggles whether transfers can be made to this account. |
| POST | /accounts/{id}/adjust | Adjusts the balance of an account. |
| PUT | /accounts/{id}/adjust | Updates a previous balance adjustment. |
| GET | /accounts/overview | Provides an overview of all accounts. |
| PUT | /accounts/{id}/updateNotes | Updates the notes for a specific account. |

### Request Bodies

#### `AccountAddForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| type | AccountType | The type of account (e.g., DEBIT_CARD, CREDIT_CARD, CASH). | Mandatory |
| name | string | The name of the account. | Mandatory |
| no | string | The account number. | Optional |
| balance | BigDecimal | The initial balance of the account. | Mandatory |
| include | boolean | Whether to include this account in financial summaries. | Mandatory |
| canTransferFrom | boolean | Whether this account can be a source for transfers. | Mandatory |
| canTransferTo | boolean | Whether this account can be a destination for transfers. | Mandatory |
| canExpense | boolean | Whether this account can be used for recording expenses. | Mandatory |
| canIncome | boolean | Whether this account can be used for recording income. | Mandatory |
| notes | string | Additional notes about the account. | Optional |
| currencyCode | string | The currency code for the account (e.g., "USD", "EUR"). | Mandatory |
| creditLimit | BigDecimal | The credit limit for credit card accounts. | Optional |
| billDay | integer | The billing day of the month for credit card accounts. | Optional |
| apr | BigDecimal | The annual percentage rate for credit accounts. | Optional |
| sort | integer | A number used for sorting accounts. | Optional |

#### `AccountQueryForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| type | AccountType | Filter by account type. | Optional |
| enable | boolean | Filter by whether the account is enabled. | Optional |
| name | string | Filter by account name (contains). | Optional |
| minBalance | double | Filter by minimum account balance. | Optional |
| maxBalance | double | Filter by maximum account balance. | Optional |
| no | string | Filter by account number (contains). | Optional |
| include | boolean | Filter by whether the account is included in summaries. | Optional |
| canExpense | boolean | Filter by whether the account can be used for expenses. | Optional |
| canIncome | boolean | Filter by whether the account can be used for income. | Optional |
| canTransferFrom | boolean | Filter by whether transfers can be made from the account. | Optional |
| canTransferTo | boolean | Filter by whether transfers can be made to the account. | Optional |
| currencyCode | string | Filter by currency code. | Optional |

#### `AccountUpdateForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| name | string | The new name of the account. | Optional |
| no | string | The new account number. | Optional |
| notes | string | New notes for the account. | Optional |
| creditLimit | BigDecimal | The new credit limit. | Optional |
| billDay | integer | The new billing day. | Optional |
| include | boolean | New value for whether the account is included in summaries. | Optional |
| canTransferFrom | boolean | New value for whether transfers can be made from the account. | Optional |
| canTransferTo | boolean | New value for whether transfers can be made to the account. | Optional |
| canExpense | boolean | New value for whether the account can be used for expenses. | Optional |
| canIncome | boolean | New value for whether the account can be used for income. | Optional |
| apr | BigDecimal | The new annual percentage rate. | Optional |
| sort | integer | The new sort order. | Optional |

#### `AccountUpdateNotesForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| notes | string | The new notes for the account. | Optional |

#### `AdjustBalanceAddForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| book | integer | The ID of the book this adjustment belongs to. | Mandatory |
| createTime | long | The timestamp of when the adjustment was created. | Mandatory |
| title | string | A title for the adjustment. | Optional |
| notes | string | Additional notes for the adjustment. | Optional |
| balance | BigDecimal | The new balance after the adjustment. | Mandatory |

#### `AdjustBalanceUpdateForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| book | integer | The ID of the book this adjustment belongs to. | Optional |
| createTime | long | The new timestamp for the adjustment. | Mandatory |
| title | string | The new title for the adjustment. | Optional |
| notes | string | New notes for the adjustment. | Optional |

### Response Bodies

#### `AccountDetails`

| Name | Data Type | Description |
| --- | --- | --- |
| id | integer | The unique identifier for the account. |
| name | string | The name of the account. |
| type | AccountType | The type of the account. |
| typeName | string | The name of the account type. |
| no | string | The account number. |
| balance | BigDecimal | The current balance of the account. |
| convertedBalance | BigDecimal | The balance converted to the user's default currency. |
| rate | BigDecimal | The exchange rate used for conversion. |
| enable | boolean | Whether the account is currently active. |
| include | boolean | Whether the account is included in financial summaries. |
| canExpense | boolean | Whether the account can be used for expenses. |
| canIncome | boolean | Whether the account can be used for income. |
| canTransferFrom | boolean | Whether transfers can be made from this account. |
| canTransferTo | boolean | Whether transfers can be made to this account. |
| notes | string | Additional notes about the account. |
| currencyCode | string | The currency of the account. |
| creditLimit | BigDecimal | The credit limit for the account. |
| billDay | integer | The billing day of the month for the account. |
| apr | BigDecimal | The annual percentage rate for the account. |
| asOfDate | long | The timestamp of the last balance update. |
| sort | integer | The sort order of the account. |
| remainLimit | BigDecimal | The remaining credit limit. |
| label | string | The label for the account, which is the same as the name. |

## Balance Flow API

This API is responsible for managing the flow of money, including expenses, income, and transfers between accounts.

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| POST | /balance-flows | Adds a new balance flow record (expense, income, or transfer). |
| GET | /balance-flows | Queries a paginated list of balance flow records. |
| GET | /balance-flows/{id} | Retrieves the details of a specific balance flow record. |
| PUT | /balance-flows/{id} | Updates an existing balance flow record. |
| DELETE | /balance-flows/{id} | Deletes a balance flow record. |
| GET | /balance-flows/statistics | Retrieves statistics for balance flow records. |
| PATCH | /balance-flows/{id}/confirm | Confirms a balance flow record. |
| POST | /balance-flows/{id}/addFile | Attaches a file to a balance flow record. |
| GET | /balance-flows/{id}/files | Retrieves the files attached to a balance flow record. |

### Request Bodies

#### `BalanceFlowAddForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| book | integer | The ID of the book this flow belongs to. | Mandatory |
| type | FlowType | The type of flow (EXPENSE, INCOME, TRANSFER). | Mandatory |
| title | string | A title for the flow. | Optional |
| createTime | long | The timestamp of when the flow occurred. | Mandatory |
| account | integer | The ID of the source account. | Optional |
| categories | List<CategoryRelationForm> | A list of categories associated with the flow. | Optional |
| payee | integer | The ID of the payee. | Optional |
| tags | Set<integer> | A set of tag IDs associated with the flow. | Optional |
| to | integer | The ID of the destination account (for transfers). | Optional |
| amount | BigDecimal | The amount of the flow. | Optional |
| convertedAmount | BigDecimal | The amount converted to the book's default currency. | Optional |
| notes | string | Additional notes about the flow. | Optional |
| confirm | boolean | Whether the flow is confirmed. | Mandatory |
| include | boolean | Whether to include this flow in statistics. | Mandatory |

#### `BalanceFlowQueryForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| book | integer | Filter by book ID. | Optional |
| type | FlowType | Filter by flow type. | Optional |
| title | string | Filter by title (contains). | Optional |
| minAmount | double | Filter by minimum amount. | Optional |
| maxAmount | double | Filter by maximum amount. | Optional |
| minTime | long | Filter by minimum time. | Optional |
| maxTime | long | Filter by maximum time. | Optional |
| account | integer | Filter by source or destination account ID. | Optional |
| payees | Set<integer> | Filter by a set of payee IDs. | Optional |
| categories | Set<integer> | Filter by a set of category IDs. | Optional |
| tags | Set<integer> | Filter by a set of tag IDs. | Optional |
| confirm | boolean | Filter by confirmation status. | Optional |
| include | boolean | Filter by inclusion in statistics. | Optional |
| toId | integer | Filter by destination account ID. | Optional |
| notes | string | Filter by notes (contains). | Optional |
| hasFile | boolean | Filter by whether the flow has an attached file. | Optional |

### Response Bodies

#### `BalanceFlowDetails`

| Name | Data Type | Description |
| --- | --- | --- |
| book | BookForFlow | The book this flow belongs to. |
| type | FlowType | The type of flow. |
| typeName | string | The name of the flow type. |
| title | string | The title of the flow. |
| notes | string | Additional notes about the flow. |
| createTime | long | The timestamp of when the flow occurred. |
| amount | BigDecimal | The amount of the flow. |
| convertedAmount | BigDecimal | The amount converted to the book's default currency. |
| account | AccountForFlow | The source account of the flow. |
| confirm | boolean | Whether the flow is confirmed. |
| include | boolean | Whether this flow is included in statistics. |
| categories | List<CategoryRelationDetails> | The categories associated with the flow. |
| tags | List<TagRelationDetails> | The tags associated with the flow. |
| accountName | string | The name of the source account. |
| categoryName | string | The names of the categories, joined by commas. |
| to | AccountDetails | The destination account (for transfers). |
| payee | IdAndNameDetails | The payee of the flow. |
| listTitle | string | A generated title for display in lists. |
| tagsName | string | The names of the tags, joined by commas. |
| needConvert | boolean | Whether a currency conversion is needed. |
| convertCode | string | The currency code to convert to. |
| typeIndex | integer | The index of the flow type enum. |

## Book API

This API manages books, which are collections of financial records.

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | /books | Queries a paginated list of books. |
| GET | /books/{id} | Retrieves the details of a specific book. |
| POST | /books | Adds a new book. |
| GET | /books/all | Retrieves all books matching the query criteria. |
| PUT | /books/{id} | Updates an existing book. |
| DELETE | /books/{id} | Deletes a book. |
| PATCH | /books/{id}/toggle | Toggles the enabled/disabled state of a book. |
| POST | /books/template | Adds a new book from a template. |
| POST | /books/copy | Adds a new book by copying an existing one. |
| GET | /books/{id}/export | Exports the balance flows of a book to an Excel file. |

### Request Bodies

#### `BookAddForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| name | string | The name of the book. | Mandatory |
| defaultCurrencyCode | string | The default currency for the book. | Mandatory |
| defaultExpenseAccountId | integer | The ID of the default account for expenses. | Optional |
| defaultIncomeAccountId | integer | The ID of the default account for income. | Optional |
| defaultTransferFromAccountId | integer | The ID of the default source account for transfers. | Optional |
| defaultTransferToAccountId | integer | The ID of the default destination account for transfers. | Optional |
| notes | string | Additional notes about the book. | Optional |
| sort | integer | A number used for sorting books. | Optional |

#### `BookAddByBookForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| bookId | integer | The ID of the book to copy from. | Mandatory |
| book | BookAddForm | The details of the new book to create. | Mandatory |

#### `BookAddByTemplateForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| templateId | integer | The ID of the template to use. | Mandatory |
| book | BookAddForm | The details of the new book to create. | Mandatory |

#### `BookQueryForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| enable | boolean | Filter by whether the book is enabled. | Optional |
| name | string | Filter by book name (contains). | Optional |

#### `BookUpdateForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| name | string | The new name for the book. | Optional |
| defaultExpenseAccountId | integer | The new default expense account ID. | Optional |
| defaultIncomeAccountId | integer | The new default income account ID. | Optional |
| defaultTransferFromAccountId | integer | The new default transfer source account ID. | Optional |
| defaultTransferToAccountId | integer | The new default transfer destination account ID. | Optional |
| defaultExpenseCategoryId | integer | The new default expense category ID. | Optional |
| defaultIncomeCategoryId | integer | The new default income category ID. | Optional |
| notes | string | New notes for the book. | Optional |
| sort | integer | The new sort order. | Optional |

### Response Bodies

#### `BookDetails`

| Name | Data Type | Description |
| --- | --- | --- |
| id | integer | The unique identifier for the book. |
| name | string | The name of the book. |
| group | IdAndNameDetails | The group the book belongs to. |
| notes | string | Additional notes about the book. |
| enable | boolean | Whether the book is currently active. |
| defaultCurrencyCode | string | The default currency for the book. |
| defaultExpenseAccount | AccountDetails | The default account for expenses. |
| defaultIncomeAccount | AccountDetails | The default account for income. |
| defaultTransferFromAccount | AccountDetails | The default source account for transfers. |
| defaultTransferToAccount | AccountDetails | The default destination account for transfers. |
| defaultExpenseCategory | CategoryDetails | The default category for expenses. |
| defaultIncomeCategory | CategoryDetails | The default category for income. |
| current | boolean | Whether this is the user's current book. |
| groupDefault | boolean | Whether this is the group's default book. |
| sort | integer | The sort order of the book. |

## Category API

This API manages categories for organizing financial transactions.

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | /categories | Queries a paginated list of categories. |
| GET | /categories/all | Retrieves all categories matching the query criteria. |
| POST | /categories | Adds a new category. |
| PATCH | /categories/{id}/toggle | Toggles the enabled/disabled state of a category. |
| PUT | /categories/{id} | Updates an existing category. |
| DELETE | /categories/{id} | Deletes a category. |

### Request Bodies

#### `CategoryAddForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| type | CategoryType | The type of category (EXPENSE or INCOME). | Mandatory |
| name | string | The name of the category. | Mandatory |
| notes | string | Additional notes about the category. | Optional |
| pId | integer | The ID of the parent category, for creating subcategories. | Optional |
| sort | integer | A number used for sorting categories. | Optional |

#### `CategoryQueryForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| bookId | integer | Filter by book ID. | Optional |
| type | CategoryType | Filter by category type. | Optional |
| name | string | Filter by category name (contains). | Optional |
| enable | boolean | Filter by whether the category is enabled. | Optional |

#### `CategoryUpdateForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| name | string | The new name for the category. | Optional |
| notes | string | New notes for the category. | Optional |
| pId | integer | The new parent category ID. | Optional |
| sort | integer | The new sort order. | Optional |

### Response Bodies

#### `CategoryDetails`

| Name | Data Type | Description |
| --- | --- | --- |
| id | integer | The unique identifier for the category. |
| name | string | The name of the category. |
| type | CategoryType | The type of the category. |
| notes | string | Additional notes about the category. |
| enable | boolean | Whether the category is currently active. |
| canExpense | boolean | Whether this category can be used for expenses. |
| canIncome | boolean | Whether this category can be used for income. |
| level | integer | The depth of the category in the hierarchy. |
| sort | integer | The sort order of the category. |
| children | List<CategoryDetails> | A list of child categories. |

## Currency API

This API provides currency-related functionalities, including retrieving exchange rates and performing currency conversions.

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | /currencies/all | Retrieves a list of all available currencies. |
| GET | /currencies | Queries a paginated list of currencies. |
| POST | /currencies/refresh | Refreshes the currency exchange rates from an external source. |
| GET | /currencies/rate | Retrieves the exchange rate between two currencies. |
| GET | /currencies/calc | Calculates the converted amount between two currencies. |
| PUT | /currencies/{id}/rate | Updates the exchange rate for a specific currency. |

### Request Bodies

#### `ChangeRateForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| base | string | The base currency for the new rate. | Optional |
| rate | BigDecimal | The new exchange rate. | Optional |

#### `CurrencyQueryForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| base | string | The base currency to query rates against. | Optional |
| name | string | Filter by currency name (contains). | Optional |

### Response Bodies

#### `CurrencyDetails`

| Name | Data Type | Description |
| --- | --- | --- |
| id | integer | The unique identifier for the currency. |
| name | string | The name of the currency (e.g., "US Dollar"). |
| description | string | A description of the currency. |
| rate | double | The exchange rate of the currency against the base currency. |
| rate2 | double | An alternative exchange rate. |
| value | string | The currency code (e.g., "USD"). |
| label | string | The currency code. |
| title | string | The currency code. |

## Group API

This API manages groups, which are collections of users who share financial data.

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | /groups | Queries a paginated list of groups the user belongs to. |
| POST | /groups | Adds a new group. |
| PUT | /groups/{id} | Updates an existing group. |
| DELETE | /groups/{id} | Deletes a group. |
| POST | /groups/{id}/inviteUser | Invites a user to a group. |
| POST | /groups/{id}/removeUser | Removes a user from a group. |
| POST | /groups/{id}/agree | Accepts an invitation to join a group. |
| POST | /groups/{id}/reject | Rejects an invitation to join a group. |
| GET | /groups/{id}/users | Retrieves a list of users in a group. |

### Request Bodies

#### `GroupAddForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| name | string | The name of the group. | Mandatory |
| defaultCurrencyCode | string | The default currency for the group. | Mandatory |
| notes | string | Additional notes about the group. | Optional |
| templateId | integer | The ID of the book template to use for the group's default book. | Mandatory |

#### `GroupUpdateForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| name | string | The new name for the group. | Mandatory |
| notes | string | New notes for the group. | Optional |
| defaultCurrencyCode | string | The new default currency for the group. | Mandatory |
| defaultBookId | integer | The new default book ID for the group. | Mandatory |

#### `InviteUserForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| username | string | The username of the user to invite. | Mandatory |

#### `RemoveUserForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| userId | integer | The ID of the user to remove. | Mandatory |

### Response Bodies

#### `GroupDetails`

| Name | Data Type | Description |
| --- | --- | --- |
| id | integer | The unique identifier for the group. |
| name | string | The name of the group. |
| notes | string | Additional notes about the group. |
| enable | boolean | Whether the group is currently active. |
| defaultCurrencyCode | string | The default currency for the group. |
| role | string | The user's role in the group. |
| current | boolean | Whether this is the user's current group. |
| roleId | integer | The ID of the user's role. |
| defaultBook | IdAndNameDetails | The default book for the group. |

#### `GroupUserDetails`

| Name | Data Type | Description |
| --- | --- | --- |
| id | integer | The unique identifier for the user. |
| username | string | The username of the user. |
| nickName | string | The nickname of the user. |
| role | string | The user's role in the group. |
| roleId | integer | The ID of the user's role. |

## Payee API

This API manages payees, which are the recipients of financial transactions.

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| POST | /payees | Adds a new payee. |
| GET | /payees | Queries a paginated list of payees. |
| PUT | /payees/{id} | Updates an existing payee. |
| GET | /payees/all | Retrieves all payees matching the query criteria. |
| PATCH | /payees/{id}/toggle | Toggles the enabled/disabled state of a payee. |
| PATCH | /payees/{id}/toggleCanExpense | Toggles whether the payee can be used for expenses. |
| PATCH | /payees/{id}/toggleCanIncome | Toggles whether the payee can be used for income. |
| DELETE | /payees/{id} | Deletes a payee. |

### Request Bodies

#### `PayeeAddForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| name | string | The name of the payee. | Mandatory |
| notes | string | Additional notes about the payee. | Optional |
| canExpense | boolean | Whether this payee can be used for expenses. | Mandatory |
| canIncome | boolean | Whether this payee can be used for income. | Mandatory |
| sort | integer | A number used for sorting payees. | Optional |

#### `PayeeQueryForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| bookId | integer | Filter by book ID. | Optional |
| name | string | Filter by payee name (contains). | Optional |
| enable | boolean | Filter by whether the payee is enabled. | Optional |
| canExpense | boolean | Filter by whether the payee can be used for expenses. | Optional |
| canIncome | boolean | Filter by whether the payee can be used for income. | Optional |

#### `PayeeUpdateForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| name | string | The new name for the payee. | Optional |
| notes | string | New notes for the payee. | Optional |
| canExpense | boolean | New value for whether the payee can be used for expenses. | Optional |
| canIncome | boolean | New value for whether the payee can be used for income. | Optional |
| sort | integer | The new sort order. | Optional |

### Response Bodies

#### `PayeeDetails`

| Name | Data Type | Description |
| --- | --- | --- |
| id | integer | The unique identifier for the payee. |
| name | string | The name of the payee. |
| notes | string | Additional notes about the payee. |
| enable | boolean | Whether the payee is currently active. |
| canExpense | boolean | Whether this payee can be used for expenses. |
| canIncome | boolean | Whether this payee can be used for income. |
| sort | integer | The sort order of the payee. |

## Tag API

This API manages tags, which are used to label and categorize financial transactions.

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | /tags | Queries a paginated list of tags. |
| GET | /tags/all | Retrieves all tags matching the query criteria. |
| POST | /tags | Adds a new tag. |
| PATCH | /tags/{id}/toggle | Toggles the enabled/disabled state of a tag. |
| PATCH | /tags/{id}/toggleCanExpense | Toggles whether the tag can be used for expenses. |
| PATCH | /tags/{id}/toggleCanIncome | Toggles whether the tag can be used for income. |
| PATCH | /tags/{id}/toggleCanTransfer | Toggles whether the tag can be used for transfers. |
| PUT | /tags/{id} | Updates an existing tag. |
| DELETE | /tags/{id} | Deletes a tag. |

### Request Bodies

#### `TagAddForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| name | string | The name of the tag. | Mandatory |
| notes | string | Additional notes about the tag. | Optional |
| pId | integer | The ID of the parent tag, for creating sub-tags. | Optional |
| canExpense | boolean | Whether this tag can be used for expenses. | Mandatory |
| canIncome | boolean | Whether this tag can be used for income. | Mandatory |
| canTransfer | boolean | Whether this tag can be used for transfers. | Mandatory |
| sort | integer | A number used for sorting tags. | Optional |

#### `TagQueryForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| bookId | integer | Filter by book ID. | Optional |
| name | string | Filter by tag name (contains). | Optional |
| enable | boolean | Filter by whether the tag is enabled. | Optional |
| canExpense | boolean | Filter by whether the tag can be used for expenses. | Optional |
| canIncome | boolean | Filter by whether the tag can be used for income. | Optional |
| canTransfer | boolean | Filter by whether the tag can be used for transfers. | Optional |

#### `TagUpdateForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| name | string | The new name for the tag. | Optional |
| notes | string | New notes for the tag. | Optional |
| pId | integer | The new parent tag ID. | Optional |
| canExpense | boolean | New value for whether the tag can be used for expenses. | Optional |
| canIncome | boolean | New value for whether the tag can be used for income. | Optional |
| canTransfer | boolean | New value for whether the tag can be used for transfers. | Optional |
| sort | integer | The new sort order. | Optional |

### Response Bodies

#### `TagDetails`

| Name | Data Type | Description |
| --- | --- | --- |
| id | integer | The unique identifier for the tag. |
| name | string | The name of the tag. |
| notes | string | Additional notes about the tag. |
| enable | boolean | Whether the tag is currently active. |
| canExpense | boolean | Whether this tag can be used for expenses. |
| canIncome | boolean | Whether this tag can be used for income. |
| canTransfer | boolean | Whether this tag can be used for transfers. |
| level | integer | The depth of the tag in the hierarchy. |
| sort | integer | The sort order of the tag. |
| children | List<TagDetails> | A list of child tags. |

## User API

This API handles user authentication and management.

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| POST | /login | Authenticates a user and returns a JWT. |
| POST | /logout | Logs out the current user. |
| POST | /register | Registers a new user. |
| PUT | /bind | Binds a username and password to the current user. |
| GET | /initState | Retrieves the initial state for the application after a user logs in. |
| PATCH | /setDefaultBook/{id} | Sets the default book for the current user. |
| PATCH | /setDefaultGroup/{id} | Sets the default group for the current user. |
| PATCH | /changePassword | Changes the password for the current user. |
| GET | /bookSelect/all | Retrieves a list of all books available to the user, for use in a select/dropdown menu. |
| PATCH | /setDefaultGroupAndBook/{id} | Sets the default group and book for the current user. |

### Request Bodies

#### `LoginForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| username | string | The user's username. | Mandatory |
| password | string | The user's password. | Mandatory |
| remember | boolean | Whether to remember the user for 7 days. | Optional |

#### `RegisterForm`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| username | string | The desired username. | Mandatory |
| password | string | The desired password. | Mandatory |
| inviteCode | string | An invitation code required for registration. | Mandatory |

#### `ChangePasswordRequest`

| Name | Data Type | Description | Optionality |
| --- | --- | --- | --- |
| oldPassword | string | The user's current password. | Mandatory |
| newPassword | string | The user's new password. | Mandatory |

### Response Bodies

#### `LoginResponse`

| Name | Data Type | Description |
| --- | --- | --- |
| accessToken | string | The JWT for authenticating subsequent requests. |
| username | string | The username of the logged-in user. |
| remember | boolean | Whether the user should be remembered. |

#### `InitStateResponse`

| Name | Data Type | Description |
| --- | --- | --- |
| user | UserSessionVo | The session information for the current user. |
| book | BookSessionVo | The session information for the user's default book. |
| group | GroupSessionVo | The session information for the user's default group. |

#### `SelectVo`

| Name | Data Type | Description |
| --- | --- | --- |
| value | string | The value for the select option (e.g., "groupId-bookId"). |
| label | string | The display label for the select option. |
